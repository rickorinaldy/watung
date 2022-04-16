import pandas as pd
from flask import Flask, render_template, request, url_for, flash, redirect
from config import config
import psycopg2

def connect():
    params = config()
    conn = psycopg2.connect(**params)
    return conn, conn.cursor()

conn, cur = connect()

app = Flask(__name__)
app.config["SECRET_KEY"] = "f0e40714cf9777ff6fc427a4aae32c110f743bff688f6048"

@app.route("/",methods=("GET","POST"))
def open(conn=conn,cur=cur):
    if request.method == "POST":
        if "update" in request.form:
            update(
                request.form["ids"],
                request.form["nama"],
                request.form["harga"],
                request.form["modal"],
                request.form["ukuran"],
            )
        elif "delete" in request.form:
            delete(request.form["ids"])

        elif "add" in request.form:
            add(
                request.form["addnama"],
                request.form["addharga"],
                request.form["addmodal"],
                request.form["addukuran"],
            )
        
        # elif "import" in request.form:
        #     impor(request.form["file"])
    
    try:
        data = pd.read_sql_query("SELECT * FROM accounts", conn)
    except:
        conn, cur = connect()
        data = pd.read_sql_query("SELECT * FROM accounts", conn)
    finally:
        ln = len(data["nama"].to_list())
        return render_template(
            "index.html",
            ids = data["ids"].to_list(),
            nama = data["nama"].to_list(),
            harga = data["harga"].to_list(),
            modal = data["modal"].to_list(),
            ukuran = data["ukuran"].to_list(),
            ln=ln
        )

def add(brg,hrg,mdl,typ,cur=cur,conn=conn):
    try:
        cur.execute(
            f"INSERT INTO accounts (NAMA, HARGA, MODAL, UKURAN) VALUES ('{brg}',{hrg},{mdl},'{typ}')"
        )
    except:
        conn, cur = connect()
        cur.execute(
            f"INSERT INTO accounts (NAMA, HARGA, MODAL, UKURAN) VALUES ('{brg}',{hrg},{mdl},'{typ}')"
        )
    finally:
        conn.commit()

def delete(ids,cur=cur,conn=conn):
    try:
        cur.execute(
            f"DELETE FROM accounts WHERE ids={ids}"
        )
    except:
        conn, cur = connect()
        cur.execute(
            f"DELETE FROM accounts WHERE ids={ids}"
        )
    finally:
        conn.commit()

def update(ids,brg,hrg,mdl,typ,cur=cur,conn=conn):
    try:
        cur.execute(
            f"UPDATE accounts SET NAMA='{brg}', HARGA={hrg}, MODAL={mdl}, UKURAN='{typ}' WHERE IDs={ids}"
        )
    except:
        conn, cur = connect()
        cur.execute(
            f"UPDATE accounts SET NAMA='{brg}', HARGA={hrg}, MODAL={mdl}, UKURAN='{typ}' WHERE IDs={ids}"
        )
    finally:
        conn.commit()

app.run("0.0.0.0")
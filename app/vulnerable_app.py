# app/vulnerable_app.py
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

DATABASE = "example.db"

def query_db(sql):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(sql)   # intentionally vulnerable
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route("/search")
def search():
    # user input inserted directly into SQL string (vulnerable)
    q = request.args.get("q", "")
    sql = f"SELECT id, name FROM users WHERE name LIKE '%{q}%'"
    results = query_db(sql)
    return {"results": results}

@app.route("/show")
def show():
    name = request.args.get("name", "")
    # renders template using user input (vulnerable to reflected XSS if template not safe)
    return render_template("show.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "studentprojectkey"

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            role TEXT,
            date TEXT,
            status TEXT,
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    # Default user
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', '1234')")

    conn.commit()
    conn.close()

init_db()

# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# ---------- HOME ----------
@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    status_filter = request.args.get("status")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if status_filter:
        cursor.execute("SELECT * FROM jobs WHERE status=? ORDER BY id DESC", (status_filter,))
    else:
        cursor.execute("SELECT * FROM jobs ORDER BY id DESC")

    jobs = cursor.fetchall()
    conn.close()

    return render_template("index.html", jobs=jobs, status_filter=status_filter)

# ---------- ADD ----------
@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        date = request.form["date"]
        status = request.form["status"]
        notes = request.form["notes"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO jobs (company, role, date, status, notes) VALUES (?, ?, ?, ?, ?)",
                       (company, role, date, status, notes))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add.html")

# ---------- EDIT ---------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        date = request.form["date"]
        status = request.form["status"]
        notes = request.form["notes"]

        cursor.execute("""
            UPDATE jobs
            SET company=?, role=?, date=?, status=?, notes=?
            WHERE id=?
        """, (company, role, date, status, notes, id))

        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM jobs WHERE id=?", (id,))
    job = cursor.fetchone()
    conn.close()

    return render_template("edit.html", job=job)

# ---------- DELETE ----------
@app.route("/delete/<int:id>")
def delete(id):
    if "user" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
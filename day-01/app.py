from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts(
            acc_no TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Create Account
@app.route("/create", methods=["GET", "POST"])
def create():
    message = ""
    if request.method == "POST":
        acc_no = request.form["acc_no"]
        name = request.form["name"]
        balance = float(request.form["balance"])

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO accounts VALUES (?, ?, ?)",
                           (acc_no, name, balance))
            conn.commit()
            message = "Account created successfully!"
        except:
            message = "Account number already exists!"
        finally:
            conn.close()

    return render_template("create.html", message=message)

# Deposit
@app.route("/deposit", methods=["GET", "POST"])
def deposit():
    message = ""
    if request.method == "POST":
        acc_no = request.form["acc_no"]
        amount = float(request.form["amount"])

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM accounts WHERE acc_no=?", (acc_no,))
        account = cursor.fetchone()

        if account:
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE acc_no=?",
                           (amount, acc_no))
            conn.commit()
            message = "Deposit successful!"
        else:
            message = "Account not found!"

        conn.close()

    return render_template("deposit.html", message=message)

# Withdraw
@app.route("/withdraw", methods=["GET", "POST"])
def withdraw():
    message = ""
    if request.method == "POST":
        acc_no = request.form["acc_no"]
        amount = float(request.form["amount"])

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM accounts WHERE acc_no=?", (acc_no,))
        account = cursor.fetchone()

        if account:
            if account[0] >= amount:
                cursor.execute("UPDATE accounts SET balance = balance - ? WHERE acc_no=?",
                               (amount, acc_no))
                conn.commit()
                message = "Withdrawal successful!"
            else:
                message = "Insufficient balance!"
        else:
            message = "Account not found!"

        conn.close()

    return render_template("withdraw.html", message=message)

# Check Balance
@app.route("/balance", methods=["GET", "POST"])
def balance():
    message = ""
    balance = None

    if request.method == "POST":
        acc_no = request.form["acc_no"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT balance FROM accounts WHERE acc_no=?", (acc_no,))
        account = cursor.fetchone()

        if account:
            balance = account[0]
        else:
            message = "Account not found!"

        conn.close()

    return render_template("balance.html", balance=balance, message=message)

# Delete Account
@app.route("/delete", methods=["GET", "POST"])
def delete():
    message = ""
    if request.method == "POST":
        acc_no = request.form["acc_no"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM accounts WHERE acc_no=?", (acc_no,))
        account = cursor.fetchone()

        if account:
            cursor.execute("DELETE FROM accounts WHERE acc_no=?", (acc_no,))
            conn.commit()
            message = "Account deleted successfully!"
        else:
            message = "Account not found!"

        conn.close()

    return render_template("delete.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)

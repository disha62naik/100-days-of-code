from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

FILE_NAME = "expenses.txt"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        amount = request.form["amount"]

        try:
            amount = float(amount)
        except ValueError:
            return "Invalid amount"

        with open(FILE_NAME, "a") as file:
            file.write(f"{name},{amount}\n")

        return redirect("/")

    expenses = []
    total = 0

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            for line in file:
                name, amount = line.strip().split(",")
                amount = float(amount)
                expenses.append((name, amount))
                total += amount

    return render_template("index.html", expenses=expenses, total=total)


if __name__ == "__main__":
    app.run(debug=True)

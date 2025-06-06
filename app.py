from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from datetime import date,datetime,timedelta
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecret"

def update_user_data():
    import pprint
    import os

    if not os.path.exists("users.json"):
        print("⚠️ users.json not found.")
        return

    with open("users.json", "r") as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ users.json is not valid JSON.")
            return

    username = session.get("username")
    if not username:
        print("⚠️ No username in session.")
        return

    print(f"👤 Updating user: {username}")
    print("📂 Users before update:")
    pprint.pprint(users)

    user_found = False
    for i, user in enumerate(users):
        if user["username"] == username:
            users[i]["goal"] = session.get("goal", 2000)
            users[i]["total"] = session.get("total", 0)
            users[i]["last_log_date"] = session.get("last_log_date")
            users[i]["streak"] = session.get("streak", 0)
            user_found = True
            break

    if user_found:
        try:
            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)
            print("✅ USERS.JSON UPDATED. New content:")
            pprint.pprint(users)
            print("📁 Absolute path of saved file:", os.path.abspath("users.json"))
        except Exception as e:
            print(f"❌ Error writing to users.json: {e}")
    else:
        print(f"❌ User '{username}' not found.")



@app.route("/login", methods=["GET", "POST"])
def login():
    message = request.args.get("message")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []
        else:
            users = []


        for user in reversed(users):
            if user["username"] == username and check_password_hash(user["password"], password):
                print("✅ Loaded from users.json:", user)
                session["logged_in"] = True
                session["username"] = username
                session["goal"] = max(user.get("goal", 2000), 1)
                session["total"] = user.get("total", 0)
                session["last_log_date"] = user.get("last_log_date")
                session["streak"] = user.get("streak", 0)
                return redirect(url_for("home"))

        return redirect(url_for("login", message="Incorrect"))

    return render_template("login.html", message=message)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []
        else:
            users = []

        for user in users:
            if user["username"] == username:
                return redirect(url_for("register", message="❌ Username already exists!"))

        users.append({
            "username" : username,
            "password" : generate_password_hash(password),
            "goal" : 2000,
            "total" : 0,
            "last_log_date" : None,
            "streak" : 0
        })

        with open("users.json", "w") as f:
            json.dump(users, f)

        return redirect(url_for("login", message ="account_created"))

    return render_template("register.html")


@app.route("/",methods=["GET"])
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    progress = int((session["total"] / session["goal"]) * 100) if session["goal"] > 0 else 0
    message = request.args.get("message")
    return render_template("index.html",goal = session["goal"], total = session["total"], progress = progress, username = session["username"], message = message, streak = session.get("streak", 0))

@app.route("/set_goal",methods=["POST"])
def set_goal():
    goal_input = request.form.get("goal")

    if not goal_input:
        return redirect(url_for("home", message ="⚠️ No goal provided!"))

    try:
        goal = int(goal_input)
        if goal <= 0:
            return redirect(url_for("home", message="❌ Goal must be a positive number!"))
        session["goal"] = int(goal_input)
        update_user_data()
        return redirect(url_for("home", message = f"Goal set to {session['goal']} ml per day!"))
    except ValueError:
        return redirect(url_for("home", message = "❌ Goal must be a number!"))


@app.route("/log",methods=["POST"])
def log_water():
    try:
        amount = int(request.form.get("amount"))
        if amount <= 0:
            return redirect(url_for("home", message="❌ Amount must be a positive number."))
    except (ValueError, TypeError):
        return redirect(url_for("home", message = "❌ Invalid water amount."))

    today = date.today().isoformat()
    last_log_date = session.get("last_log_date")

    if last_log_date != today:
        session["total"] = 0
        if last_log_date == (date.today() - timedelta(days = 1)).isoformat():
            session["streak"] = session.get("streak", 0) + 1
        else:
            session["streak"] = 1
        session["last_log_date"] = today

    session["total"] += amount
    update_user_data()
    return redirect(url_for("home",message =f"You logged {amount} ml!"))

@app.route("/subtract", methods=["POST"])
def subtract_water():
    try:
        amount = int(request.form.get("amount"))
    except(ValueError,TypeError):
        return redirect(url_for("home", message="❌ Invalid water amount."))

    if amount < 0:
        return redirect(url_for("home",message="❌ Amount must be positive."))

    session["total"] = max(0,session["total"] - amount)

    update_user_data()
    return redirect(url_for("home",message=f"💧 Subtracted {amount} ml from your total."))

@app.route("/logout")
def logout():
    if session.get("logged_in"):
        update_user_data()
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date,timedelta
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique= True, nullable= False)
    password = db.Column(db.String(200), nullable= False)
    goal = db.Column(db.Integer, default= 2000)
    total = db.Column(db.Integer, default= 0)
    last_log_date = db.Column(db.String(20))
    streak = db.Column(db.Integer, default= 0)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_pw = generate_password_hash(password)

        if User.query.filter_by(username=username).first():
            return redirect(url_for("register", message="exist"))

        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login", message="account_created"))

    message = request.args.get("message")
    return render_template("register.html", message=message)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = request.args.get("message")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user=User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
                session["logged_in"] = True
                session["username"] = user.username
                session["goal"] = user.goal
                session["total"] = user.total
                session["last_log_date"] = user.last_log_date
                session["streak"] = user.streak
                return redirect(url_for("home"))

        return redirect(url_for("login", message="Incorrect"))

    return render_template("login.html", message=message)


@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    progress = int((session["total"] / session["goal"]) * 100) if session["goal"] > 0 else 0
    message = request.args.get("message")
    return render_template("index.html",goal = session["goal"], total = session["total"], progress = progress, username = session["username"], message = message, streak = session.get("streak", 0))

@app.route("/set_goal",methods=["POST"])
def set_goal():
    goal_input = request.form.get("goal")

    try:
        goal = int(goal_input)
        if goal <= 0:
            raise ValueError
        session["goal"] = int(goal_input)

        user = User.query.filter_by(username=session["username"]).first()
        user.goal = goal
        db.session.commit()

        return redirect(url_for("home", message = f"Goal set to {session['goal']} ml per day!"))
    except ValueError:
        return redirect(url_for("home", message = "❌ Goal must be a number!"))


@app.route("/log",methods=["POST"])
def log_water():
    try:
        amount = int(request.form.get("amount"))
        if amount <= 0:
            raise ValueError
    except ValueError:
        return redirect(url_for("home", message = "❌ Invalid water amount."))

    today = date.today().isoformat()
    last_log_date = session.get("last_log_date")

    user = User.query.filter_by(username=session["username"]).first()

    if last_log_date != today:
        session["total"] = 0
        if last_log_date == (date.today() - timedelta(days = 1)).isoformat():
            session["streak"] = session.get("streak", 0) + 1
        else:
            session["streak"] = 1
        session["last_log_date"] = today

    session["total"] += amount
    user.total = session["total"]
    user.last_log_date = session["last_log_date"]
    user.streak = session["streak"]
    db.session.commit()

    return redirect(url_for("home",message =f"You logged {amount} ml!"))

@app.route("/subtract", methods=["POST"])
def subtract_water():
    try:
        amount = int(request.form.get("amount"))
        if amount < 0:
            raise ValueError
    except ValueError:
        return redirect(url_for("home", message="❌ Invalid water amount."))

    session["total"] = max(0,session["total"] - amount)

    user = User.query.filter_by(username=session["username"]).first()
    user.total = session["total"]
    db.session.commit()

    return redirect(url_for("home",message=f"💧 Subtracted {amount} ml from your total."))

@app.route("/logout")
def logout():
    if session.get("logged_in"):
        user = User.query.filter_by(username=session["username"]).first()
        user.goal = session["goal"]
        user.total = session["total"]
        user.last_log_date = session["last_log_date"]
        user.streak = session["streak"]
        db.session.commit()

    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0")


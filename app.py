from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import subprocess
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Secret Key for Sessions
app.secret_key = "AI_NAVIGATION_SECRET_KEY"


# ==========================
# HOME
# ==========================

@app.route("/")
def home():
    return render_template("home.html")


# ==========================
# REGISTER
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:

            cursor.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                 (name, email, hashed_password)
                )

            conn.commit()

        except sqlite3.IntegrityError:

            conn.close()

            flash("Email already exists!", "error")
            return redirect("/register")

        conn.close()

        flash("Registration Successful! Please login.", "success")
        return redirect("/login")

    return render_template("register.html")


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
             "SELECT name,password FROM users WHERE email=?",
             (email,)
            )
        

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[1], password):

            session["user"] = email
            session["name"] = user[0]

            return redirect("/dashboard")

        flash("Invalid Email or Password", "error")
        return redirect("/login")

    return render_template("login.html")


# ==========================
# DASHBOARD
# ==========================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    detections = []

    try:
        with open("detections.txt", "r") as file:

            lines = file.readlines()[-10:]   # Last 10 detections

            for line in reversed(lines):

                data = line.strip().split("|")

                if len(data) == 5:

                    detections.append({
                        "time": data[0].strip(),
                        "object": data[1].strip(),
                        "direction": data[2].strip(),
                        "distance": data[3].strip(),
                        "confidence": data[4].strip()
                    })

    except FileNotFoundError:
        pass

    return render_template(
        "dashboard.html",
        name=session["name"],
        email=session["user"],
        detections=detections
    )

# ==========================
# START NAVIGATION
# ==========================

@app.route("/start_navigation")
def start_navigation():

    if "user" not in session:

        return redirect("/login")

    subprocess.Popen(["python", "navigation.py"])

    return "Navigation Started Successfully!"


# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(debug=True)
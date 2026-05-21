from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from database.db import create_user, get_db, get_user_by_email, init_db, seed_db
app = Flask(__name__)
app.secret_key = "dev-secret-key-for-spendly"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not all([name, email, password, confirm_password]):
            flash("All fields are required.", "danger")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        try:
            create_user(name, email, password)
            flash("Your account has been created. You can now sign in.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            # Specifically handling IntegrityError would be better, but we check the error type from db.py
            import sqlite3
            if isinstance(e, sqlite3.IntegrityError):
                flash("Email already registered.", "danger")
            else:
                flash(f"An unexpected error occurred: {e}", "danger")
            return render_template("register.html")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    # Hardcoded mock data for UI design phase
    user = {
        "name": "Demo User",
        "email": "demo@spendly.com",
        "member_since": "May 2026"
    }
    stats = {
        "total_spent": "₹12,450.00",
        "transaction_count": 42,
        "top_category": "Food"
    }
    transactions = [
        {"date": "2026-05-20", "description": "Grocery Store", "category": "Food", "amount": "₹1,200.00"},
        {"date": "2026-05-19", "description": "Fuel Station", "category": "Transport", "amount": "₹3,500.00"},
        {"date": "2026-05-18", "description": "Internet Bill", "category": "Bills", "amount": "₹999.00"},
        {"date": "2026-05-17", "description": "Cinema", "category": "Entertainment", "amount": "₹450.00"},
        {"date": "2026-05-16", "description": "Pharmacy", "category": "Health", "amount": "₹200.00"},
    ]
    categories = [
        {"name": "Food", "amount": "₹4,500.00", "percentage": 36},
        {"name": "Transport", "amount": "₹3,200.00", "percentage": 25},
        {"name": "Bills", "amount": "₹2,100.00", "percentage": 17},
        {"name": "Entertainment", "amount": "₹1,500.00", "percentage": 12},
        {"name": "Health", "amount": "₹1,150.00", "percentage": 10},
    ]

    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories
    )



@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)

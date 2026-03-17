from flask import Blueprint, request, render_template, redirect, session, url_for
from database.db import users
from models.user_model import User
from bson import ObjectId

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = users.find_one({"email": email, "password": password})
        if user:
            session["user_id"] = str(user["_id"])
            session["user_name"] = user["name"]
            session["user_role"] = user.get("role", "learner")
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")
    
    return render_template("login.html")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        
        if users.find_one({"email": email}):
            return render_template("signup.html", error="Email already exists")
            
        new_user = User(name, email, password, role)
        result = users.insert_one(new_user.to_dict())
        
        session["user_id"] = str(result.inserted_id)
        session["user_name"] = name
        session["user_role"] = role
        
        return redirect(url_for("dashboard"))
        
    return render_template("signup.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))

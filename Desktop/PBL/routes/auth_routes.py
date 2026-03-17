from flask import Blueprint, request, jsonify, render_template

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle login logic here
        return jsonify({"message": "Login logic to be implemented"}), 200
    
    return render_template("login.html")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Handle signup logic here
        return jsonify({"message": "Signup logic to be implemented"}), 201
        
    return render_template("signup.html")

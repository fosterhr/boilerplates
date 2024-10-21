from flask import Flask, render_template, request, redirect, url_for
import flask_login
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize Flask-Login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Load the secret key from a file for session management
with open("secret.key", "r") as file:
    app.config["SECRET_KEY"] = file.read().strip()

# User class for Flask-Login
class User(flask_login.UserMixin):
    def __init__(self, username, created_at):
        self.username = username
        self.created_at = created_at  # Store created_at as a timestamp

    def get_id(self):
        return self.username
    
    def formatted_created_at(self):
        # Convert the stored timestamp to a formatted string
        dt_object = datetime.fromtimestamp(self.created_at)
        return dt_object.strftime("%m/%d/%Y at %I:%M %p UTC")

# User loader for Flask-Login
@login_manager.user_loader
def load_user(username):
    return User(username, None)  # Placeholder, will be populated later

# Class to handle user database operations
class UserDatabase:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.init_db()  # Initialize the database when the class is instantiated

    def init_db(self):
        # Create the users table with a created_at column of type INTEGER
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    created_at INTEGER NOT NULL
                )
            """)
            conn.commit()

    def execute_query(self, query, params=(), fetchone=False):
        # Execute a database query and return results if needed
        with sqlite3.connect(self.db_name) as conn:
            c = conn.cursor()
            c.execute(query, params)
            if fetchone:
                return c.fetchone()  # Return a single result
            conn.commit()  # Commit changes for non-select queries

    def authenticate(self, username):
        # Authenticate user by fetching the stored password
        result = self.execute_query("SELECT password FROM users WHERE username = ?", (username,), fetchone=True)
        return result[0] if result else None

    def username_exists(self, username):
        # Check if a username already exists in the database
        result = self.execute_query("SELECT username FROM users WHERE username = ?", (username,), fetchone=True)
        return result is not None

    def add_user(self, username, password):
        # Add a new user to the database with the current timestamp
        created_at = int(datetime.utcnow().timestamp())  # Store current time as an integer timestamp
        self.execute_query("INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)", (username, password, created_at))

    def get_user(self, username):
        # Fetch user details, including created_at
        return self.execute_query("SELECT username, created_at FROM users WHERE username = ?", (username,), fetchone=True)

# Create an instance of UserDatabase
db = UserDatabase()

@app.route("/", methods=["GET"])
def home():
    # Render the home page
    return render_template("home.html")

@app.route("/account", methods=["GET"])
@flask_login.login_required
def account():
    # Fetch user details
    if flask_login.current_user:
        user_data = db.get_user(flask_login.current_user.get_id())
        user = User(user_data[0], user_data[1])  # Create User object with created_at as a timestamp
        return render_template("account.html", user=user)  # Pass user object to the template
    else:
        # Redirect to the login page
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        stored_password = db.authenticate(username)  # Authenticate the user
        
        if stored_password and password == stored_password:
            user_data = db.get_user(username)  # Fetch user data
            user = User(user_data[0], user_data[1])
            flask_login.login_user(user)  # Log in the user
            return redirect(url_for("account"))
        return render_template("login.html", error_message="Error: Invalid username or password.")
    
    # Render the login page
    return render_template("login.html")

@app.route("/logout")
def logout():
    # Log out the user and redirect to login page
    flask_login.logout_user()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Validate input fields
        if username and password and confirm_password:
            if password == confirm_password:
                if db.username_exists(username):
                    return render_template("register.html", error_message="Error: Username is already in use.")
                db.add_user(username, password)  # Add new user to the database
                user_data = db.get_user(username)  # Fetch user data after registration
                user = User(user_data[0], user_data[1])
                flask_login.login_user(user)  # Log in the new user
                return redirect(url_for("account"))
            return render_template("register.html", error_message="Error: Passwords do not match.")
        return render_template("register.html", error_message="Error: Missing a required field.")
    
    # Render the registration page
    return render_template("register.html")

if __name__ == "__main__":
    app.run(port=80, debug=True)
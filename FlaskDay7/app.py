# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)

# # Configuration
# app.secret_key = 'your-secret-key-here'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///c:/Users/ASUS/PYTHON TRAINING/FlaskDay7/instance/project.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize SQLAlchemy
# db = SQLAlchemy(app)

# # User model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

# # Create database tables
# with app.app_context():
#     db.create_all()
#     # Create a test user if not exists
#     if not User.query.filter_by(username='admin').first():
#         test_user = User(username='admin', password='password123')
#         db.session.add(test_user)
#         db.session.commit()

# # Route for home page
# @app.route("/")
# def home():
#     if 'user_id' in session:
#         return redirect(url_for('dashboard'))
#     return render_template('index.html')

# # Route for dashboard
# @app.route("/dashboard")
# def dashboard():
#     if 'user_id' not in session:
#         flash('Please log in first', 'error')
#         return redirect(url_for('home'))
    
#     user = User.query.get(session['user_id'])
#     return render_template('dashboard.html', user=user)

# # Route for login
# @app.route("/login", methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')
    
#     user = User.query.filter_by(username=username, password=password).first()
    
#     if user:
#         session['user_id'] = user.id
#         session['username'] = user.username
#         flash('Login successful!', 'success')
#         return redirect(url_for('dashboard'))
#     else:
#         flash('Invalid username or password', 'error')
#         return redirect(url_for('home'))

# # Route for logout
# @app.route("/logout")
# def logout():
#     # Clear session
#     session.pop('user_id', None)
#     session.pop('username', None)
#     flash('You have been logged out successfully', 'success')
#     return redirect(url_for('home'))

# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

# Dummy users
users = {
    "admin": "1234",
    "manish": "abcd"
}

posts = []


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/view_post")
def view_post():
    return render_template("view_post.html", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/create_post")
        else:
            return "Invalid Credentials "

    return render_template("login.html")


@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        post = request.form["post"]
        posts.append(post)
        return redirect("/view_post")

    return render_template("create_post.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)



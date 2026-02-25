from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///student.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(100))
    enrollment = db.Column(db.String(50))
    role = db.Column(db.String(20), default="student")   # NEW FIELD

    def __repr__(self):
        return f"<Student {self.email}>"

    def __repr__(self):
        return f"<Student {self.email}>"


@app.route("/")
def home():
    if "student_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        department = request.form["department"]
        enrollment = request.form["enrollment"]
        role = request.form["role"]   # GET ROLE

        existing_user = Student.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        new_student = Student(
            name=name,
            email=email,
            password=password,
            department=department,
            enrollment=enrollment,
            role=role
        )

        db.session.add(new_student)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        student = Student.query.filter_by(email=email).first()

        if student and student.password == password:
            session["student_id"] = student.id
            session["role"] = student.role

            flash("Login successful!", "success")

            if student.role == "admin":
                return redirect(url_for("admin_dashboard"))
            else:
                return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "student_id" not in session:
        flash("Please login first!", "danger")
        return redirect(url_for("login"))

    student = Student.query.get(session["student_id"])
    return render_template("dashboard.html", student=student)


@app.route("/admin")
def admin_dashboard():
    if "student_id" not in session or session.get("role") != "admin":
        flash("Access denied!", "danger")
        return redirect(url_for("login"))

    students = Student.query.all()
    return render_template("admin_dashboard.html", students=students)



@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "student_id" not in session:
        return redirect(url_for("login"))

    student = Student.query.get(session["student_id"])

    if request.method == "POST":
        student.name = request.form["name"]
        student.department = request.form["department"]
        student.enrollment = request.form["enrollment"]

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("profile.html", student=student)


@app.route("/logout")
def logout():
    session.pop("student_id", None)
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

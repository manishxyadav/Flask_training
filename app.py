from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/add')
def add():
    yadav = User(name="Manish",role="admin")
    db.session.add(yadav)
    db.session.commit()
    return "Data added"

@app.route('/show')
def show():
    users = User.query.all()
    for user in users:
        print(f"{user.name} - {user.role}")
    print(User)
    return "<p>data fetching!</p>"

@app.route('/update')
def update():
    user = User.query.get(1)
    user.name = "Manish Yadav"
    db.session.commit()
    return f"Updated user: {user.name}"

@app.route("/delete")
def delete():
    user= User.query.get(2) 
    db.session.delete(user) 
    db.session.commit() 
    return f"<p>{user.name} is removed with {user.id}</p>"



@app.route("/show_all")
def show_all():
    users= User.query.all() 
    
    return render_template("index.html",users = users)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
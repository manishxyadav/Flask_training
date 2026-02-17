from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    



class Post(db.Model):
    id=db.Column(db.Integer, primary_key = True) 
    title=db.Column(db.String(200)) 
    content = db.Column(db.Text)
    user_id= db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable = False

 )

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
    #users= User.query.all()
    #order by desc
    users= User.query.order_by(desc(User.id)).all() 
    
    return render_template("index.html",users = users)

@app.route("/show_f")
def show_f():
    users=User.query.filter(User.email.like("%gmail.com")).all()
    return render_template("index.html", users = users)


@app.route("/show_user")
def show_user():
    users= User.query.filter(User.name.like("A%")).all() 
    
    return render_template("index.html",users = users)



@app.route("/post")
def post():
    user = User(name = "Alice", email = 'alice@xy.com', role = 24)
    db.session.add(user)
    db.session.commit()
    post = Post(title = "News post",
                content = "here is breaking news",
                user_id=user.id)

    db.session.add(post)
    db.session.commit()

    return f"{post.title}, {post.user_id}"


@app.route("/post_by/<name>")
def post_by(name):
    user = User.query.filter_by(name = name).first()

    if user:
        post = Post(title = "User post",
                content = f"this post created by {user.name}",
                user_id = user.id)
        db.session.add(post)
        db.session.commit()
        return f"{post.title}, {post.content}"
    
    return "no user found"

@app.route('/show_post')
def show_post():
    # Join User and Post tables correctly
    results = db.session.query(User, Post)\
        .join(Post, User.id == Post.user_id)\
        .all()

    # Print for debugging
    for u, p in results:
        print(f"{p.title} by {u.name}")

    return render_template("post.html", posts=results)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)




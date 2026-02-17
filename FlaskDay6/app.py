from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>That is Registration // go in url and type /registration</h1>"

@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get("Password")
        return f"Registration Successful! <br> Name: {name} <br> Email: {email}"
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
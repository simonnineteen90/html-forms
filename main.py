from flask import Flask, render_template, request, redirect, url_for
import smtplib
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
# DB SETUP
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food-blog.db'
db = SQLAlchemy(app)

# CREATE DB TABLE
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)


db.create_all()    


# CONTACT FORM EMAIL
def send_email(name, email, message):
    my_email = "appdunntest@gmail.com"
    password = "password goes here"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user= my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=my_email,
                            msg=f"Subject: Contact form \n\n Name: {name} \n Email: {email} \n Message: {message}")

# @app.route('/contact')
# def contact():
#     return render_template('index.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post')
def post():
    return render_template('post.html')    

@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        name = request.form["contact_name"]
        email = request.form["contact_email"]
        message = request.form["contact_message"]
        send_email(name, email, message)
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


# ADD NEW POST TO DB
@app.route('/add_post', methods=['POST', 'GET'])
def add_post():
    if request.method == "POST":
        new_post = Post(
            heading=request.form["heading"],
            content=request.form["content"],
            ingredients=request.form["ingredients"],
            difficulty=request.form["difficulty"]

        )
        db.session.add(new_post)
        db.session.commit()
        print([new_post.heading, new_post.content,new_post.ingredients,new_post.difficulty])
        return redirect(url_for('add_post'))

    return render_template('add_post.html')    


if __name__ == "__main__":
    app.run(debug=True)
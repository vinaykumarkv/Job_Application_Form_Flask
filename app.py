from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAIL_USERNAME'] = os.getenv("MAIL")
app.config['MAIL_PASSWORD'] = os.getenv("PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL")
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
mail = Mail(app)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date_of_application = db.Column(db.Date)
    occupation = db.Column(db.String(80))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        date_of_application = request.form['date']
        date = datetime.strptime(date_of_application,"%Y-%m-%d") #conversion of date to fix bug
        occupation = request.form['occupation']
        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date_of_application=date,
                    occupation=occupation)
        db.session.add(form)
        db.session.commit()


        message_body = (f"Thank you for your submission, {first_name} {last_name}!\n"+
                        f"Submitted as on {date} \n"+
                        "Thank You")
        message = Message(subject='Application Submitted',sender=app.config['MAIL_USERNAME'],recipients=[email], body=message_body)

        mail.send(message)

        flash(f'Submitted. Thank you for your application! - {first_name}', "success")

    return render_template("index.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)


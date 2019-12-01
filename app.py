from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import smtplib
#import twilio
#from twilio.rest import Client 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitors.sqlite3'
app.config['SECRET_KEY'] = "random string"

MY_ADDRESS = "demoankit639@gmail.com"
PASSWORD = "toolazy@69"
user = "ankit4471@gmail.com"
db = SQLAlchemy(app)

class visitors(db.Model):
	id = db.Column('visitor_id', db.Integer, primary_key = True)
	v_name = db.Column(db.String(100))
	v_email = db.Column(db.String(100), unique=True)
	v_phone = db.Column(db.String(12), unique=True) 
	v_cIn = db.Column(db.String(100))
	v_cOut = db.Column(db.String(100))
	h_name = db.Column(db.String(100))
	h_email = db.Column(db.String(100), unique=True)
	h_phone = db.Column(db.String(12), unique=True)
	address = db.Column(db.String(200))

def __init__(self, v_name, v_email, v_phone, v_cIn, v_cOut, h_name, h_email, h_phone, address):
	self.v_name = v_name
	self.v_email = v_email
	self.v_phone = v_phone
	self.v_cIn = v_cIn
	self.v_cOut = v_cOut
	self.h_name = h_name
	self.h_email = h_email
	self.h_phone = h_phone
	self.address = address
   

@app.route('/')
def show_all():
   return render_template('show_all.html', visitors = visitors.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
	if request.method == 'POST':
		if not request.form['v_name'] or not request.form['v_email'] or not request.form['v_phone'] or not request.form['v_cIn'] or not request.form['v_cOut']or not request.form['h_name']or not request.form['h_email']or not request.form['h_phone']:
			flash('Please enter all the fields', 'error')
		else:
			visitor = visitors(v_name = request.form['v_name'],v_email = request.form['v_email'],v_phone = request.form['v_phone'],v_cIn = request.form['v_cIn'], v_cOut = request.form['v_cOut'],h_name = request.form['h_name'],h_email = request.form['h_email'], h_phone = request.form['h_phone'],address = request.form['address']) 
			#send_time = dt.datetime(2018,8,26,3,0,0) # set your sending time in UTC
			#time.sleep(send_time.timestamp() - time.time())

			s = smtplib.SMTP('smtp.gmail.com', 587) 
  
			# start TLS for security 
			s.starttls() 
  
			# Authentication 
			s.login(MY_ADDRESS, PASSWORD) 
	  
			# message to be sent 
			message = "Message_you_need_to_send"
  	
			# sending the mail 
			s.sendmail(MY_ADDRESS, user, message) 
  
			# terminating the session 
			s.quit() 

			db.session.add(visitor)
			db.session.commit()
			flash('Record was successfully added')
	return render_template('new.html')

if __name__ == '__main__':
	db.create_all()

	app.run(debug = True)
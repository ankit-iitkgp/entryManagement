from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import smtplib
import twilio
from twilio.rest import Client 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitors.sqlite3'
app.config['SECRET_KEY'] = "random String"

MY_ADDRESS = "demoankit639@gmail.com"
PASSWORD = "XXXXXXXX"
MY_NUMBER = "+xxxxxxxxxxx"

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
	self.h_name = h_name
	self.h_email = h_email
	self.h_phone = h_phone
	self.address = address
   

@app.route('/')
def show_all():
	return render_template('show_all.html', visitors = visitors.query.all() )

@app.route('/exit', methods = ['GET', 'POST'])
def exit():
	if request.method == 'POST' :
		if not request.form['id']: 
			flash("Please enter your unique ID")
		else:
			datetime_object = datetime.now()
			datetime_object = datetime_object.strftime("%d-%b-%Y (%H:%M:%S.%f)")
			result = visitors.query.filter_by(id = request.form['id']).all()
			for entity in result:
				v_mail = entity.v_email
				v_num = entity.v_phone
				sms = ('Visit Details\nName: '+entity.v_name+'\nEmail: '+ entity.v_email + '\nPhone: '+ entity.v_phone +'\nCheck In: '+ entity.v_cIn +'\nCheck Out: '+ datetime_object)
				db.session.delete(entity)
				flash('Record was successfully deleted')	

			s = smtplib.SMTP('smtp.gmail.com', 587)   
				# start TLS for security 
			s.starttls() 
				# Authentication 
			s.login(MY_ADDRESS, PASSWORD) 	
				# sending the mail  
			s.sendmail(MY_ADDRESS, v_mail, sms) 
			# terminating the session 
			s.quit() 

			account_sid = 'Your_SID' 
			#Your own account sid on twilio
			auth_token = 'Your_auth_token' 
			#Your own auth_token on twilio
			client = Client(account_sid, auth_token) 
			message = client.messages.create(from_=MY_NUMBER, body = sms, to = v_num) 

	return render_template('exit.html')


@app.route('/new', methods = ['GET', 'POST'])
def new():
	if request.method == 'POST':
		if not request.form['v_name'] or not request.form['v_email'] or not request.form['v_phone'] or not request.form['h_name']or not request.form['h_email']or not request.form['h_phone'] or not request.form['address']:
			flash('Please enter all the fields', 'error')
		else:
			datetime_object = datetime.now()
			datetime_object = datetime_object.strftime("%d-%b-%Y (%H:%M:%S.%f)")
			visitor = visitors(v_name = request.form['v_name'],v_email = request.form['v_email'],v_phone = request.form['v_phone'],v_cIn = datetime_object, h_name = request.form['h_name'],h_email = request.form['h_email'], h_phone = request.form['h_phone'],address = request.form['address']) 
			db.session.add(visitor)
			db.session.commit()
			flash('Record was successfully added')	

			s = smtplib.SMTP('smtp.gmail.com', 587)   
			# start TLS for security 
			s.starttls() 
			# Authentication 
			s.login(MY_ADDRESS, PASSWORD) 
			# message to be sent 
			message = ('Visitors Details\nName: '+request.form['v_name']+'\nEmail: '+ request.form['v_email'] + '\nPhone: '+ request.form['v_phone'] +'\nCheck In: '+ datetime_object)
			# sending the mail 
			user = request.form['h_email']
			userNo = request.form['h_phone']
			s.sendmail(MY_ADDRESS, user, message) 
			# terminating the session 
			s.quit() 

			account_sid = 'YourSID' 
			#Your own account sid on twilio
			auth_token = 'your_auth_token' 
			#Your own auth_token on twilio
			client = Client(account_sid, auth_token) 
			message = client.messages.create(from_= MY_NUMBER, body = message, to = userNo) 

	return render_template('new.html')

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)

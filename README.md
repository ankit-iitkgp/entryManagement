# entryManagement
Entry management software using flask, SQLAlchemy, smtp and twilio.

To run the program
1) Activete virtua environment
source venv/bin/activate
2) python3 app.py
3) Go to Browser and open 
http://127.0.0.1:5000/

Now, there are 3 functionalities
1) Display the database(show_all.html)
2) Add vsitors and hosts details(new.html). In this as soon as visitor enter the data, an email and a text sms is sent to host with all visitors details.
3) CheckOut visitor(exit.html) - 
  In this visitor enters his unique id from the database. As soon as he submits he gets all the details of the visit on sms and email.
  
NOTE-- For messaging use only those numbers which are registered on Twilio.  

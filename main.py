from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
#import base64
#import struct


with open('config.json', 'r') as c:
    params = json.load(c) ["params"]

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass@localhost/shivesh'
db = SQLAlchemy(app)
class Contact(db.Model):
    contactID = db.Column(db.Integer, primary_key=True)
    contactName = db.Column(db.String(50), nullable=False)
    contactEmail = db.Column(db.String(80), nullable=False,unique=True)
    contactPhoneNo = db.Column(db.String(15), nullable=False, unique=True)
    contactMessage = db.Column(db.String(80), nullable=False)

@app.route('/',methods = ['GET', 'POST'])
def webInterface():   
    #contactInfo = Contact.query.filter_by(contactID=8).all() 
    contactInfo = Contact.query.all() 
    contactResult = [
        {
            "contactID": row.contactID,
            #"contactURL": "/contact-details/"+str(base64.b64encode(bytes([row.contactID]))),
            "contactName": row.contactName,
            "contactEmail": row.contactEmail,
            "contactPhoneNo": row.contactPhoneNo,
            "contactMessage": row.contactMessage,
            # Add other columns as per your table structure
        } for row in contactInfo
    ]

    if(request.method=='POST'):
        contactName = request.form.get('contactName')
        contactEmail = request.form.get('contactEmail') 
        contactPhoneNo = request.form.get('contactPhoneNo') 
        contactMessage = request.form.get('contactMessage')         
        
        entry = Contact(contactName=contactName,contactEmail=contactEmail,contactPhoneNo=contactPhoneNo,contactMessage=contactMessage)       
        db.session.add(entry)
        db.session.commit()     

    return render_template('index.py',params = params, contactResult=contactResult)


@app.route('/contact-details/<string:contactID>',methods = ['GET'])
def contact_detail(contactID):  
   
    #print(contactID)
    #byte_value = base64.b64decode(contactID)
    #print(byte_value)
    #integer_value = int.from_bytes(byte_value, byteorder='big')   
    #print(integer_value) 
    #contactResult = Contact.query.filter_by(contactID=integer_value).first()   

    contactResult = Contact.query.filter_by(contactID=contactID).first()   
   
    return render_template('contact-details.py', contactResult=contactResult)


   


 
 
 
app.run(debug= True)




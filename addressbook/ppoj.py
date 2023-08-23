from flask import Flask, render_template, render_template_string, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DataError, IntegrityError
import sqlite3

app = Flask(__name__)
db = sqlite3.connect('/Users/sushmabollepally/Desktop/project/project.db')
cur = db.cursor()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/sushmabollepally/Desktop/project/project.db'
db = SQLAlchemy(app)

## create model for the app
class Contact(db.Model):
    # columns to be added in the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.CHAR(100), nullable=False)
    phone = db.Column(db.CHAR(20), nullable=False)
    email = db.Column(db.CHAR(120), nullable=False, unique_key=True)
    def __repr__(self):
        return "<Contact {}: {}>".format(self.id,self.name )


# create above mentioned columns with the Table
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload')
def contacts():
    return render_template("upload.html")

@app.route('/retrieve')
def retrive():
    return render_template("retrieve.html")

# @app.route('/retrieve?')
# def retrive_data():
#     return render_template("retrieve_data.html")

#### Get all contacts list ####
@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    # db.session.execute()
    return jsonify([{'id': contact.id, 'name': contact.name, 'phone': contact.phone, 'email': contact.email} for contact in contacts])

##### Add a contact in the table
@app.route('/contacts', methods=['POST'])

def add_contact():
    #data = json.load(open('address_book.json', encoding='utf-8'))
    # data = request.get_json()
    try:
        phone = len(10)
        try:
            phone = int(phone)
        except:
            print("enter only digits")
        
    except:
        print("Contact number should not exceed 10 digits")
    
    data = str(request.data)
    data= data.replace("\\r", "")
    data= data.replace("\\n", " ")
    data = data.replace("'", "")
    data= data.strip()
    data = data.split(" ")

    data= [i.split("=")[1] for i in data]

    print("data ******** : \n", data)
    contact = Contact(name=data[0], phone=data[1], email=data[2])

    
    db.session.add(contact)
    db.session.commit()
    # try:
    #     phone = len(10)
    #     try:
    #         phone = int(phone)
    #     except:
    #         print("enter only digits")
        
    # except:
    #     print("Contact number should not exceed 10 digits")
        
    return {'id': contact.id, 'name': contact.name, 'phone': contact.phone, 'email': contact.email}

    
    
###### Modify a Record in the Table
@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.get_json()
    contact = Contact.query.get_or_404(id)
    contact.name = data['name']
    contact.phone = data['phone']
    contact.email = data['email']
    try:
        contact.phone is len(10)
        
    except:
        print("Contact number should not exceed 10 digits")

    db.session.commit()
    return {'id': contact.id, 'name': contact.name, 'phone': contact.phone, 'email': contact.email}

###### Delete a record in the Table
@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return {'message': 'Contact deleted'}

if __name__ == '__main__':
   app.run(debug=True)


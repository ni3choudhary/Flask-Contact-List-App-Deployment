from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 


# Creating class for our Contact database
class Contact(db.Model):
    sr = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String(250))
    relationship = db.Column(db.String(250))
    email = db.Column(db.String(254))
    phone_number = db.Column(db.String(20))
    address = db.Column(db.String(1000))

    def __repr__(self) -> str:
        return self.full_name


@app.route('/')
def index():
    contacts = Contact.query.all()
    search_input = request.args.get('search-area')
    if search_input:
        contacts = Contact.query.filter(Contact.full_name.contains(search_input)).all()
    else:
        contacts = Contact.query.all()
        search_input = ''
    return render_template('index.html',contacts=contacts,search_input=search_input)

@app.route('/add', methods=['GET', 'POST'])
def addContact():
    if request.method == 'POST':
        new_contact = Contact(
            full_name = request.form['fullname'],
            relationship = request.form['relationship'],
            email = request.form['email'],
            phone_number = request.form['phone-number'],
            address = request.form['address'],
            )
        db.session.add(new_contact)
        db.session.commit()
 
        return redirect(url_for('index'))
    
    return render_template('new-contact.html')

@app.route('/edit-contact/<string:id>/', methods=['GET', 'POST'])
def editContact(id):
    contact = Contact.query.get(id)
    if request.method == 'POST':
        contact.full_name = request.form['fullname']
        contact.relationship = request.form['relationship']
        contact.email = request.form['email']
        contact.phone_number = request.form['phone-number']
        contact.address = request.form['address']

        db.session.commit()
        return redirect('/profile/'+str(contact.sr))
    return render_template('edit-contact.html', contact = contact)


@app.route('/delete-contact/<string:id>/', methods=['GET', 'POST'])
def deleteContact(id):
    contact = Contact.query.get(id)
    if request.method == 'POST':
        db.session.delete(contact)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('delete-contact.html',contact = contact)

@app.route('/profile/<string:id>/', methods=['GET', 'POST'])
def contactProfile(id):
    contact = Contact.query.get(id)
    return render_template('contact-profile.html', contact=contact)

if __name__ == '__main__':
    app.run(debug=True)
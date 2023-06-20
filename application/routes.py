from flask import render_template, url_for, flash, redirect
from application import app, db, bcrypt
from application.models import User, Invoice, Entry
from application.forms import RegistrationForm, LoginForm

invoices = [
    {
        'author': 'Bartosz Rodowicz',
        'name': 'Faktura 1',
        'content': 'First post content',
        'amount': '1000.00',
        'date_posted': 'June 20, 2023'
    },
    {
        'author': 'Jan Kowalski',
        'name': 'Faktura 2',
        'content': 'Second post content',
        'amount': '1540.20',
        'date_posted': 'June 21, 2023'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', invoices=invoices)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        #reading password from the registration form and hashing it
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #creating a new user with the data from the registration form
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        #displaying a flash message after successful registration
        flash(f'Successfully created an account!', 'success')
        #redirecting to login page after successful registration
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Unsuccessful login. Check your email and password and try again.', 'danger')
    return render_template('login.html', title='Login', form=form)
from flask import render_template, url_for, flash, redirect, request, abort
from application import app, db, bcrypt
from application.models import User, Invoice, Entry
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, InvoiceForm, UploadInvoiceForm
from application.reader import get_invoice_data, convert_entries_to_string
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os

@app.route('/')
@app.route('/home')
def home():
    invoices = Invoice.query.all()
    return render_template('home.html', invoices=invoices)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    #if user is already logged in, redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
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
    #if user is already logged in, redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #if user exists and password is correct, log the user in
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unsuccessful login. Check your email and password and try again.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_new_picture(form_picture):
    #randomizing the name of the picture so it doesn't collide with other pictures in pictures folder
    random_hex = secrets.token_hex(12)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/pictures', picture_fn)
    
    form_picture.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_new_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        #filling the form with current user data
        form.username.data = current_user.username
        form.email.data = current_user.email    
    image_file = url_for('static', filename='pictures/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route('/invoice/new', methods=['GET', 'POST'])
@login_required
def new_invoice():
    form = InvoiceForm()
    if form.validate_on_submit():
        #TODO HERE IS THE CONFLICT WITH CONTENT AND ENTRIES
        invoice = Invoice(name=form.name.data, content=form.entries.data, amount=form.amount.data, author=current_user)
        db.session.add(invoice)
        db.session.commit()
        flash('Created a new invoice!', 'success')
        return redirect(url_for('home'))
    return render_template('create_invoice.html', title='New Invoice', form=form, legend='New Invoice')

@app.route('/invoice/upload', methods=['GET', 'POST'])
@login_required
def upload_invoice():
    form = UploadInvoiceForm()
    if form.validate_on_submit():
        #TODO HERE IS THE CONFLICT WITH CONTENT AND ENTRIES
        picture_fn = form.invoice_file.data.filename
        picture_path = os.path.join(app.root_path,'static/pdf_files', picture_fn)
        extracted_data = get_invoice_data(picture_path)
        invoice = Invoice(name=extracted_data['name'], content=convert_entries_to_string(extracted_data['entries']), 
                          amount=extracted_data['total_amount'], author=current_user)
        db.session.add(invoice)
        db.session.commit()
        flash('Created a new invoice!', 'success')
        return redirect(url_for('home'))
    return render_template('upload_invoice.html', title='Upload Invoice', form=form, legend='Upload Invoice')

@app.route('/invoice/<int:invoice_id>')
def invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template('invoice.html', title=invoice.name, invoice=invoice)

@app.route('/invoice/<int:invoice_id>/update', methods=['GET', 'POST'])
@login_required
def update_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    #only the author of the invoice can update it
    if invoice.author != current_user:
        abort(403)
    form = InvoiceForm()
    if form.validate_on_submit():
        invoice.name = form.name.data
        invoice.content = form.entries.data
        invoice.amount = form.amount.data
        db.session.commit()
        flash('Updated the invoice successfully!', 'success')
        return redirect(url_for('invoice', invoice_id=invoice.id))
    elif request.method == 'GET':
        form.name.data = invoice.name
        form.entries.data = invoice.content
        form.amount.data = invoice.amount
    return render_template('create_invoice.html', title='Update Invoice', form=form, legend='Update Invoice')

@app.route('/invoice/<int:invoice_id>/delete', methods=['POST'])
@login_required
def delete_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    #only the author of the invoice can update it
    if invoice.author != current_user:
        abort(403)
        
    #cascade delete all entries related to the invoice being deleted
    Entry.query.filter_by(invoice_id=invoice.id).delete()
    #deleting invoice
    db.session.delete(invoice)
    db.session.commit()
    flash('Invoice has been deleted!', 'success')
    return redirect(url_for('home'))
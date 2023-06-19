from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

#randomly generated 16 byte secret key (by running secrets.token_hex in terminal)
app.config['SECRET_KEY'] = 'cd427c1e4b942503f56b028cea251a64'

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
    
    #displaying a flash message after successful registration
    if form.validate_on_submit():
        flash(f'Successfully created an account!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)
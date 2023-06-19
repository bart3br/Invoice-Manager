from flask import Flask, render_template, url_for
app = Flask(__name__)

intakes = [
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
    return render_template('home.html', intakes=intakes)

@app.route('/about')
def about():
    return render_template('about.html', title='abcd')

#windows powershell
#$env:FLASK_APP = "main.py"
#flask run
#to work in debug mode (so we don't have to shut down and restart the server every time we make a change):
#$env:FLASK_DEBUG=1
#when we have the if name == main statement, we can run the app with python main.py

if __name__ == '__main__':
    app.run(debug=True)
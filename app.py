from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.static_url_path = '/static'
app.static_folder = 'static'

@app.get('/')
def root():
    return render_template('landing_page.html')

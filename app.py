from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.static_url_path = '/static'
app.static_folder = 'static'

@app.get('/')
def render_landing_page():
    return render_template('landing_page.html')

@app.get('/scrape')
def render_scrape():
    return render_template('scrape.html')

@app.get('/help')
def render_help():
    return render_template('help.html')

@app.get('/about')
def render_about():
    return render_template('about.html')


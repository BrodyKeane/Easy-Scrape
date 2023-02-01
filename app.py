from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

app.static_url_path = '/static'
app.static_folder = 'static'

@app.get('/')
def render_landing_page():
    return render_template('landing_page.html')


@app.get('/scrape/')
def render_scrape():
    column_count = get_column_count()
    print(column_count)
    return render_template('scrape.html', column_count=column_count)

def get_column_count():
    column_count = request.args.get('column_count', default=2, type=int)
    return column_count

@app.post('/scrape/update_form_table')
def update_form_table():
    return redirect(url_for('render_scrape'))

@app.get('/help')
def render_help():
    return render_template('help.html')

@app.get('/about')
def render_about():
    return render_template('about.html')


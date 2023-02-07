from flask import Flask, render_template, url_for, redirect, request
from flask_caching import Cache

from source.verify_url import URLPermissionChecker
from source.scrape import CorrelatedDataScraper, VerifyContainer

app = Flask(__name__)
config = {
    'SECRET_KEY': 'mysecretkey',
    'SEND_FILE_MAX_AGE_DEFAULT': 0,
    "DEBUG": True,        
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 1800,
    "CACHE_THRESHOLD": 10000
}
app.config.from_mapping(config)
cache = Cache(app)

app.static_url_path = '/static'
app.static_folder = 'static'

@app.get('/')
def render_landing_page():
    return render_template('landing_page.html')


@app.get('/url_form')
def render_url_form():
    return render_template('url_form.html', error=None)

@app.post('/scrape_form/submit_url')
def submit_url():
    url = request.form.get('url')
    cache.set("url", url)
    url_checker = URLPermissionChecker(url)
    url_verify = url_checker.can_scrape()
    if url_verify:
        return redirect(url_for('render_container_form'))
    else:
        error = url_checker.error
        return render_template('url_form.html', error=error)
    

@app.get('/container_form')
def render_container_form(error=None):
    return render_template('container_form.html', error=error)

@app.post('/scrape_form/submit_container')
def submit_container():
    container = request.form.get('container')
    cache.set("container", container)
    url = cache.get("url")
    container_verifier = VerifyContainer(url, container)
    if container_verifier.container_found():
        return redirect(url_for('render_scrape_form'))
    else:
        error = 'container could not be found'
        return redirect(url_for('render_container_form', error=error))


@app.get('/scrape_form/')
def render_scrape_form():
    url = cache.get("url") or ''
    container = cache.get("containre") or ''
    column_data = cache.get("column_data") or []
    return render_template('scrape_form.html', url=url, container=container, column_data=column_data)

@app.post('/scrape_form/save_column')
def save_column():
    column_name = request.form.get('column_name', default='value not set')
    html_selector = request.form.get('html_selector', default='value not set')
    column_data = cache.get("column_data") or []
    column_data.append({'column_name': column_name, 'html_selector': html_selector})
    cache.set("column_data", column_data)
    return redirect(url_for('render_scrape_form'))

@app.post('/scrap_form/delete_column')
def delete_column():
    column_index = request.form.get('column_index')
    column_index = int(column_index)
    column_data = cache.get("column_data")
    del column_data[column_index]
    cache.set("column_data", column_data)
    return redirect(url_for('render_scrape_form'))

@app.post('/scrape_form/reset_form')
def reset_form():
    cache.clear()
    return redirect(url_for('render_scrape_form'))

@app.post('/scrape_form/scrape')
def scrape():
    return redirect(url_for('render_scrape_form'))


@app.get('/help')
def render_help():
    return render_template('help.html')

@app.get('/about')
def render_about():
    return render_template('about.html')


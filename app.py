from flask import Flask, render_template, request, session, redirect, url_for, make_response
import os
import re
from datetime import datetime
from flask import send_from_directory
from modules.translations import translations

PRICE_SEPARATOR_RE = re.compile(r'\s[–-]\s')

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-only-for-local')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year caching

MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

STYLE_CSS_PATH = os.path.join(app.root_path, 'static', 'css', 'style.css')


def get_css_version():
    """Mtime of style.css, used as a cache-busting query param so the 1-year
    static file cache doesn't serve stale CSS after a deploy."""
    try:
        return int(os.path.getmtime(STYLE_CSS_PATH))
    except OSError:
        return 0


@app.context_processor
def inject_google_maps_api():
    return dict(google_maps_api_key=MAPS_API_KEY)


def get_locale():
    return session.get('language', 'pl')


def get_translation(key):
    locale = get_locale()
    return translations.get(locale, {}).get(key, key)


def service_item(key):
    """Split a translated 'Name – Price' string into separate parts for display."""
    text = get_translation(key)
    match = None
    for match in PRICE_SEPARATOR_RE.finditer(text):
        pass
    if match:
        return {'name': text[:match.start()].strip(), 'price': text[match.end():].strip()}
    return {'name': text.strip(), 'price': ''}


# Make translation function available in templates
app.jinja_env.globals.update(_=get_translation)
app.jinja_env.globals.update(get_locale=get_locale)
app.jinja_env.globals.update(current_year=datetime.now().year)
app.jinja_env.globals.update(service_item=service_item)
app.jinja_env.globals.update(css_version=get_css_version)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/set_language/<language>')
def set_language(language):
    if language in ['pl', 'en', 'uk']:
        session['language'] = language
    return redirect(request.referrer or '/')


@app.route('/sitemap.xml')
def sitemap():
    pages = []
    languages = ['pl', 'en', 'uk']
    for lang in languages:
        pages.append({
            'loc': url_for('index', _external=True, lang=lang),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'priority': '1.0'
        })

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')


@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


@app.errorhandler(404)
def page_not_found(e):
    # Not existing page template
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

import os
from flask import Flask, Response

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
APP_DIR = os.path.dirname(CUR_DIR)


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return get_file_contents('index.html', content_type='text/html')

@app.route('/main.js', methods=['GET'])
def main_js():
    return get_file_contents('main.js', content_type='text/javascript')

@app.route('/three.js', methods=['GET'])
def three1_js():
    return get_file_contents('three.js', content_type='text/javascript')

@app.route('/three1.js', methods=['GET'])
def three_js():
    return get_file_contents('three1.js', content_type='text/javascript')
@app.route('/manifest.manifest', methods=['GET'])
def manifest():
    return get_file_contents('manifest.manifest', content_type='application/manifest+json')

@app.route('/favicon.ico', methods=['GET'])
def favicon_ico():
    return get_file_contents('favicon.ico', content_type='image/x-icon')

@app.route('/favicon_png', methods=['GET'])
def favicon_png():
    return get_file_contents('favicon96.png', content_type='image/png')

@app.route('/api/latest.json', methods=['GET', 'POST'])
def latest_tle():
    return get_file_contents('api/latest.json', content_type='application/json')


def get_file_contents(filename, content_type=''):
    try:
        filename = os.path.join(APP_DIR, 'pub', filename)
        if os.path.exists(filename):
            with open(filename, mode='rb') as f:
                return Response(f.read(), mimetype=content_type, status=200)
        else:
            return Response('Not found', mimetype='text/plain', status=404)
    except Exception:
        return Response('Fatal error', mimetype='text/plain', status=500)


if __name__ == '__main__':
    app.run('0.0.0.0', port=80, debug=True)

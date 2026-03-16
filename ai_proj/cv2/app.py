from flask import Flask, render_template
import os

app = Flask(__name__)
app.template_folder = os.path.abspath('.')

@app.route('/')
def cv_page():
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    if not os.path.exists('static/css'):
        os.makedirs('static/css')
    if not os.path.exists('static/js'):
        os.makedirs('static/js')
    if not os.path.exists('assets'):
        os.makedirs('assets')
    app.run(debug=True)
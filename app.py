from flask import Flask, render_template
import sys
import pip
import flask

app = Flask(__name__)

@app.route('/')
def index():
    context = {
        'python_version': sys.version.split()[0],  # Берем только номер версии
        'flask_version': flask.__version__,
        'pip_version': pip.__version__
    }
    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run(debug=True)
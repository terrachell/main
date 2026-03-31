from flask import Flask, render_template, request, session, redirect
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

@app.route('/test', methods = ['GET', 'GET'])
def test():
    if request.method == "POST":
        return render_template('index.html')
    else:
        redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
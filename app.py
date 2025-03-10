from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/python')
def python():
    return render_template('python.html')

@app.route('/cpp')
def cpp():
    return render_template('cpp.html')

@app.route('/c')
def c():
    return render_template('c.html')

@app.route('/java')
def java():
    return render_template('java.html')

if __name__ == '__main__':
    app.run(debug=True)
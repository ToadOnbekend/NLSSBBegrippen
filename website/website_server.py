from flask import Flask, render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/begrippenkader')
def begrippenkader():
    return render_template('begrippenkader.html')

@app.route('/begrip')
def begrip():
    return render_template('begrippagina.html')

@app.route('/zoeken')
def zoeken():
    return render_template('zoeken.html')

@app.route('/begripaanmaken')
def aanmakenbegrip():
    return render_template('begripaanmaken.html')

@app.route('/begrippenkaderaanmaken')
def aanmakenbegrippenkader():
    return render_template('begrippenkaderaanmaken.html')


if __name__ == '__main__':
    app.run(debug=True, port=3500)




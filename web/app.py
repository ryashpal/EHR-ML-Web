from flask import Flask
from flask import render_template

import logging

app = Flask(__name__)

logging.basicConfig(filename='logs/flask.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# @app.route('/', methods=['GET'])
# def hello():
#     return('Welcome to EHR-ML-Web app!!')

@app.route('/')
def index():
    return render_template('index.html', pairs=[], the_title="Presidents Index")

if __name__ == "__main__":
    app.run(debug=True)

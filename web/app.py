from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import redirect

import logging

app = Flask(__name__)

logging.basicConfig(filename='logs/flask.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

from UploadCsvUseCase import uploadCsv


@app.route('/')
def index():
    return render_template('index.html', pairs=[], the_title="EHR-ML")


@app.route('/start')
def start():
    return render_template('start.html', pairs=[], the_title="EHR-ML: Start")


@app.route('/download_data')
def download_data():
    return send_from_directory('static', 'data_matrix.csv')


@app.route('/upload_data', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      uid = uploadCsv(request)
      return render_template('uploaded.html', pairs=[], token_text=uid)
   if request.method == 'GET':
       return redirect("/start")


@app.route('/data_window_analysis')
def data_window_analysis():
    return render_template('data_window_analysis.html', pairs=[], the_title="EHR-ML: Data Window Analysis")


@app.route('/class_ratio_analysis')
def class_ratio_analysis():
    return render_template('class_ratio_analysis.html', pairs=[], the_title="EHR-ML: Class Ratio Analysis")


@app.route('/sample_size_analysis')
def sample_size_analysis():
    return render_template('sample_size_analysis.html', pairs=[], the_title="EHR-ML: Sample Size Analysis")


@app.route('/build_model')
def build_model():
    return render_template('build_model.html', pairs=[], the_title="EHR-ML: Build Model")


@app.route('/predict_outcome')
def predict_outcome():
    return render_template('predict_outcome.html', pairs=[], the_title="EHR-ML: Predict Outcome")


if __name__ == "__main__":
    app.run(debug=True)

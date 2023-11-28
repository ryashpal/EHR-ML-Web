from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import redirect

import logging
logging.basicConfig(filename='logs/flask.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
log = logging.getLogger('EHR-ML')

app = Flask(__name__)


from UploadCsvUseCase import uploadCsv


@app.route('/')
def index():
    return render_template('index.html', the_title="EHR-ML")


@app.route('/start')
def start():
    return render_template('start.html', the_title="EHR-ML: Start")


@app.route('/download_data')
def download_data():
    return send_from_directory('static', 'data_matrix.csv')


@app.route('/upload_data', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      uid = uploadCsv(request)
      return render_template('uploaded.html', token_text=uid)
   if request.method == 'GET':
       return redirect("/start")


@app.route('/data_window_analysis')
def data_window_analysis():
    return render_template('data_window_analysis.html', the_title="EHR-ML: Data Window Analysis")


@app.route('/class_ratio_analysis')
def class_ratio_analysis():
    return render_template('class_ratio_analysis.html', the_title="EHR-ML: Class Ratio Analysis")


@app.route('/sample_size_analysis')
def sample_size_analysis():
    return render_template('sample_size_analysis.html', the_title="EHR-ML: Sample Size Analysis")


@app.route('/build_model', methods = ['GET', 'POST'])
def build_model():
    if request.method == 'POST':
        return redirect("/build_model/" + request.form.get('token_input'))
    elif request.method == 'GET':
        return render_template('build_model.html', the_title="EHR-ML: Build Model")


@app.route('/build_model/<token>')
def build_model_main(token):
    return render_template('build_model_main.html', the_title="EHR-ML: Build Model", token=token)


@app.route('/predict_outcome')
def predict_outcome():
    return render_template('predict_outcome.html', the_title="EHR-ML: Predict Outcome")


if __name__ == "__main__":
    app.run(debug=True)

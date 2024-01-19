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
from BuildModelUseCase import getModelConfigList, buildModel


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


@app.route('/standardisation_analysis')
def standardisation_analysis():
    return render_template('standardisation_analysis.html', the_title="EHR-ML: Standardisation Analysis")


@app.route('/build', methods = ['GET', 'POST'])
def build():
    if request.method == 'POST':
        return redirect("/build/" + request.form.get('token'))
    elif request.method == 'GET':
        return render_template('build.html', the_title="EHR-ML: Build")


@app.route('/build/<token>', methods = ['GET', 'POST'])
def build_form(token):
    if request.method == 'POST':
        buildModel(
            uid=token,
            windowBefore=request.form.get('window_before'),
            windowAfter=request.form.get('window_after'),
            idColumns=request.form.get('id_columns'),
            targetColumn=request.form.get('target_column'),
            measurementDateColumn=request.form.get('measurement_date_column'),
            anchorDateColumn=request.form.get('anchor_date_column'),
            )
    modelConfigList = getModelConfigList(token)
    return render_template('build_form.html', the_title="EHR-ML: Build", token=token, builtModelsList=modelConfigList)


@app.route('/evaluate')
def evaluate():
    return render_template('evaluate.html', the_title="EHR-ML: Evaluate")


@app.route('/predict')
def predict():
    return render_template('predict.html', the_title="EHR-ML: Predict")


if __name__ == "__main__":
    app.run(debug=True)

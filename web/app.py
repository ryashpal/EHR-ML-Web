import shutil

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
from EvaluateModelUseCase import getEvaluationsConfigList, evaluateModel
from PredictionUseCase import getPredictionsList
from PredictionUseCase import predict as predictOutcomes
from StandardisationAnalysisUseCase import analyse as standardisationAnalysis
from StandardisationAnalysisUseCase import getAnalysisConfigList as getStandardisationAnalysisConfigList
from SampleSizeAnalysisUseCase import analyse as sampleSizeAnalysis
from SampleSizeAnalysisUseCase import getAnalysisConfigList as getSampleSizeAnalysisConfigList
from ClassRatioAnalysisUseCase import analyse as classRatioAnalysis
from ClassRatioAnalysisUseCase import getAnalysisConfigList as getClassRatioAnalysisConfigList
from DataWindowAnalysisUseCase import analyse as dataWindowAnalysis
from DataWindowAnalysisUseCase import getAnalysisConfigList as getDataWindowAnalysisConfigList


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


@app.route('/download/build/<data_token>/<model_token>', methods = ['GET'])
def build_download(data_token, model_token):
    return send_from_directory('data/' + data_token + '/models/' + model_token, 'model.pkl')


@app.route('/evaluate', methods = ['GET', 'POST'])
def evaluate():
    if request.method == 'POST':
        return redirect("/evaluate/" + request.form.get('token'))
    elif request.method == 'GET':
        return render_template('evaluate.html', the_title="EHR-ML: Evaluate")


@app.route('/evaluate/<token>', methods = ['GET', 'POST'])
def evaluate_form(token):
    if request.method == 'POST':
        evaluateModel(
            uid=token,
            windowBefore=request.form.get('window_before'),
            windowAfter=request.form.get('window_after'),
            idColumns=request.form.get('id_columns'),
            targetColumn=request.form.get('target_column'),
            measurementDateColumn=request.form.get('measurement_date_column'),
            anchorDateColumn=request.form.get('anchor_date_column'),
            )
    modelConfigList = getEvaluationsConfigList(token)
    return render_template('evaluate_form.html', the_title="EHR-ML: Evaluate", token=token, evaluateModelsList=modelConfigList)


@app.route('/download/evaluate/<token>/<evaluate_token>', methods = ['GET'])
def evaluate_download(token, evaluate_token):
    return send_from_directory('data/' + token + '/evaluations/' + evaluate_token, 'cv_scores.json', as_attachment=True)


@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    if request.method == 'POST':
        return redirect("/predict/" + request.form.get('test_data_token') + "/" + request.form.get('train_data_token') + "/" + request.form.get('model_token'))
    elif request.method == 'GET':
        return render_template('predict.html', the_title="EHR-ML: Predict")


@app.route('/predict/<test_data_token>/<train_data_token>/<model_token>', methods = ['GET', 'POST'])
def predict_form(test_data_token, train_data_token, model_token):
    if request.method == 'POST':
        predictOutcomes(
            testDataToken=test_data_token,
            trainDataToken=train_data_token,
            modelToken=model_token,
            windowBefore=request.form.get('window_before'),
            windowAfter=request.form.get('window_after'),
            idColumns=request.form.get('id_columns'),
            targetColumn=request.form.get('target_column'),
            measurementDateColumn=request.form.get('measurement_date_column'),
            anchorDateColumn=request.form.get('anchor_date_column'),
            )
    predictionConfigList = getPredictionsList(trainDataToken=train_data_token, modelToken=model_token)
    return render_template(
        'predict_form.html',
        the_title="EHR-ML: Predict",
        test_data_token=test_data_token,
        train_data_token=train_data_token,
        model_token=model_token,
        predictionConfigList=predictionConfigList
        )


@app.route('/download/predict/<train_data_token>/<model_token>/<prediction_token>', methods = ['GET'])
def predict_download(train_data_token, model_token, prediction_token):
    return send_from_directory('data/' + train_data_token + '/models/' + model_token + '/predictions/' + prediction_token, 'preds.csv')


@app.route('/standardisation_analysis', methods = ['GET', 'POST'])
def standardisation_analysis():
    if request.method == 'POST':
        return redirect("/standardisation_analysis/" + request.form.get('token'))
    elif request.method == 'GET':
        return render_template('standardisation_analysis.html', the_title="EHR-ML: Standardisation Analysis")


@app.route('/standardisation_analysis/<token>', methods = ['GET', 'POST'])
def standardisation_analysis_form(token):
    if request.method == 'POST':
        standardisationAnalysis(
            uid=token,
            windowBefore=request.form.get('window_before'),
            windowAfter=request.form.get('window_after'),
            idColumns=request.form.get('id_columns'),
            targetColumn=request.form.get('target_column'),
            measurementDateColumn=request.form.get('measurement_date_column'),
            anchorDateColumn=request.form.get('anchor_date_column'),
            ensembleModel=(True if (request.form.get('ensemble_model') == 'on') else False),
            )
    analysisConfigList = getStandardisationAnalysisConfigList(uid=token)
    return render_template(
        'standardisation_analysis_form.html',
        the_title="EHR-ML: Standardisation Analysis",
        token=token,
        analysisConfigList=analysisConfigList
        )


@app.route('/download/standardisation_analysis/<data_token>/<analysis_token>', methods = ['GET'])
def standardisation_analysis_download(data_token, analysis_token):
    shutil.make_archive('data/' + data_token + '/standardisation_analysis/' + analysis_token, 'zip', 'data/' + data_token + '/standardisation_analysis/' + analysis_token)
    return send_from_directory('data/' + data_token + '/standardisation_analysis', analysis_token + '.zip', as_attachment=True)


@app.route('/sample_size_analysis', methods = ['GET', 'POST'])
def sample_size_analysis():
    if request.method == 'POST':
        return redirect("/sample_size_analysis/" + request.form.get('token'))
    elif request.method == 'GET':
        return render_template('sample_size_analysis.html', the_title="EHR-ML: Sample Size Analysis")


@app.route('/sample_size_analysis/<token>', methods = ['GET', 'POST'])
def sample_size_analysis_form(token):
    if request.method == 'POST':
        sampleSizeAnalysis(
            uid=token,
            windowBefore=request.form.get('window_before'),
            windowAfter=request.form.get('window_after'),
            idColumns=request.form.get('id_columns'),
            targetColumn=request.form.get('target_column'),
            measurementDateColumn=request.form.get('measurement_date_column'),
            anchorDateColumn=request.form.get('anchor_date_column'),
            ensembleModel=(True if (request.form.get('ensemble_model') == 'on') else False),
            sampleSizeList= [int(sampleSize) for sampleSize in request.form.get('sample_size_list').split(' ')]
            )
    analysisConfigList = getSampleSizeAnalysisConfigList(uid=token)
    return render_template(
        'sample_size_analysis_form.html',
        the_title="EHR-ML: Sample Size Analysis",
        token=token,
        analysisConfigList=analysisConfigList
        )


@app.route('/download/sample_size_analysis/<data_token>/<analysis_token>', methods = ['GET'])
def sample_size_analysis_download(data_token, analysis_token):
    shutil.make_archive('data/' + data_token + '/sample_size_analysis/' + analysis_token, 'zip', 'data/' + data_token + '/sample_size_analysis/' + analysis_token)
    return send_from_directory('data/' + data_token + '/sample_size_analysis', analysis_token + '.zip', as_attachment=True)


@app.route('/class_ratio_analysis', methods = ['GET', 'POST'])
def class_ratio_analysis():
    if request.method == 'POST':
        return redirect("/class_ratio_analysis/" + request.form.get('token'))
    elif request.method == 'GET':
        return render_template('class_ratio_analysis.html', the_title="EHR-ML: Class Ratio Analysis")


@app.route('/class_ratio_analysis/<token>', methods = ['GET', 'POST'])
def class_ratio_analysis_form(token):
    if request.method == 'POST':
        classRatioAnalysis(
            uid=token,
            windowBefore=request.form.get('window_before'),
            windowAfter=request.form.get('window_after'),
            idColumns=request.form.get('id_columns'),
            targetColumn=request.form.get('target_column'),
            measurementDateColumn=request.form.get('measurement_date_column'),
            anchorDateColumn=request.form.get('anchor_date_column'),
            ensembleModel=(True if (request.form.get('ensemble_model') == 'on') else False),
            pcpList= [int(pcp) for pcp in request.form.get('pcp_list').split(' ')]
            )
    analysisConfigList = getClassRatioAnalysisConfigList(uid=token)
    return render_template(
        'class_ratio_analysis_form.html',
        the_title="EHR-ML: Class Ratio Analysis",
        token=token,
        analysisConfigList=analysisConfigList
        )


@app.route('/download/class_ratio_analysis/<data_token>/<analysis_token>', methods = ['GET'])
def class_ratio_analysis_download(data_token, analysis_token):
    shutil.make_archive('data/' + data_token + '/class_ratio_analysis/' + analysis_token, 'zip', 'data/' + data_token + '/class_ratio_analysis/' + analysis_token)
    return send_from_directory('data/' + data_token + '/class_ratio_analysis', analysis_token + '.zip', as_attachment=True)


@app.route('/data_window_analysis', methods = ['GET', 'POST'])
def data_window_analysis():
    if request.method == 'POST':
        return redirect("/data_window_analysis/" + request.form.get('token'))
    elif request.method == 'GET':
        return render_template('data_window_analysis.html', the_title="EHR-ML: Data Window Analysis")


@app.route('/data_window_analysis/<token>', methods = ['GET', 'POST'])
def data_window_analysis_form(token):
    if request.method == 'POST':
        dataWindowAnalysis(
            uid=token,
            windowBeforeList=[int(windowBefore) for windowBefore in request.form.get('window_before_list').split(' ')],
            windowAfterList=[int(windowBefore) for windowBefore in request.form.get('window_after_list').split(' ')],
            idColumns=request.form.get('id_columns'),
            targetColumn=request.form.get('target_column'),
            measurementDateColumn=request.form.get('measurement_date_column'),
            anchorDateColumn=request.form.get('anchor_date_column'),
            ensembleModel=(True if (request.form.get('ensemble_model') == 'on') else False),
            )
    analysisConfigList = getDataWindowAnalysisConfigList(uid=token)
    return render_template(
        'data_window_analysis_form.html',
        the_title="EHR-ML: Data Window Analysis",
        token=token,
        analysisConfigList=analysisConfigList
        )


@app.route('/download/data_window_analysis/<data_token>/<analysis_token>', methods = ['GET'])
def data_window_analysis_download(data_token, analysis_token):
    shutil.make_archive('data/' + data_token + '/data_window_analysis/' + analysis_token, 'zip', 'data/' + data_token + '/data_window_analysis/' + analysis_token)
    return send_from_directory('data/' + data_token + '/data_window_analysis', analysis_token + '.zip', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

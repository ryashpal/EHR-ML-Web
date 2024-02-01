import logging

log = logging.getLogger('EHR-ML')


def getPredictionsList(trainDataToken, modelToken):
    import os
    import json
    from pathlib import Path

    predictionsList = []
    modelsPath = Path('data', trainDataToken, 'models')
    if os.path.exists(modelsPath):
        predictionsDirPath = Path(modelsPath, modelToken, 'predictions')
        if os.path.exists(predictionsDirPath):
            predictionsDirList = os.listdir(predictionsDirPath)
            for predictionDir in predictionsDirList:
                configFile = Path(predictionsDirPath, predictionDir, 'config.json')
                log.info('configFile: ' + str(configFile))
                if os.path.exists(configFile):
                    with open(configFile) as f:
                        predictionsConfig = json.load(f)
                        predictionsList.append(predictionsConfig)
    return predictionsList


def predict(testDataToken, trainDataToken, modelToken, windowBefore, windowAfter, idColumns, targetColumn, measurementDateColumn, anchorDateColumn):

    import os
    import json
    import uuid

    from datetime import datetime
    from pathlib import Path

    testDataDir = Path('data', testDataToken)
    trainDataDir = Path('data', trainDataToken)
    modelDir = Path(trainDataDir, 'models', modelToken)
    modelPath = Path(modelDir, 'model.pkl')
    predictionsPath = Path(modelDir, 'predictions')
    if not os.path.exists(predictionsPath):
        os.makedirs(predictionsPath)

    predictionsUid = str(uuid.uuid4())
    predictionsDir = Path(predictionsPath, predictionsUid)
    if not os.path.exists(predictionsDir):
        os.makedirs(predictionsDir)

    config = {}
    config['uid'] = predictionsUid
    config['window_before'] = windowBefore
    config['window_after'] = windowAfter
    config['id_columns'] = idColumns
    config['target_column'] = targetColumn
    config['measurement_date_column'] = measurementDateColumn
    config['anchor_date_column'] = anchorDateColumn
    config['date_created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log.info('NewConfig: ' + str(config))

    configPath = Path(predictionsDir, 'config.json')
    log.info('configPath: ' + str(configPath))

    with open(configPath, 'w') as f:
        json.dump(config, f)

    import sys
    sys.path.append('EHR-ML')
    from ehrml.ensemble.Predict import run
    from multiprocessing import Process

    predictionsPath = Path(predictionsDir, 'preds.csv')
    datamatrixPath=Path(testDataDir, 'data_matrix.csv')

    log.info('Starting the process!!')

    p = Process(
        target=run,
        args=(
                datamatrixPath,
                [col.strip() for col in idColumns.split(',')],
                targetColumn,
                measurementDateColumn,
                anchorDateColumn,
                int(windowBefore),
                int(windowAfter),
                modelPath,
                predictionsPath
            )
        )
    p.start()

    log.info('Started the process successfully!!')

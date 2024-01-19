import logging

log = logging.getLogger('EHR-ML')


def getModelConfigList(uid):
    import os
    import json
    from pathlib import Path

    modelConfigList = []
    modelsPath = Path('data', uid, 'models')
    if os.path.exists(modelsPath):
        modelDirList = os.listdir(modelsPath)
        for modelDir in modelDirList:
            configFile = Path(modelsPath, modelDir, 'config.json')
            log.info('configFile: ' + str(configFile))
            if os.path.exists(configFile):
                with open(configFile) as f:
                    modelConfig = json.load(f)
                    modelConfigList.append(modelConfig)
    return modelConfigList


def buildModel(uid, windowBefore, windowAfter, idColumns, targetColumn, measurementDateColumn, anchorDateColumn):

    import os
    import json
    import uuid

    from datetime import datetime
    from pathlib import Path

    dataDir = Path('data', uid)
    modelsPath = Path(dataDir, 'models')
    if not os.path.exists(modelsPath):
        os.makedirs(modelsPath)

    config = {}
    config['uid'] = uid
    config['window_before'] = windowBefore
    config['window_after'] = windowAfter
    config['id_columns'] = idColumns
    config['target_column'] = targetColumn
    config['measurement_date_column'] = measurementDateColumn
    config['anchor_date_column'] = anchorDateColumn
    config['date_created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log.debug('config: ' + str(config))

    uid = str(uuid.uuid4())
    modelDir = Path(modelsPath, uid)
    if not os.path.exists(modelDir):
        os.makedirs(modelDir)

    # os.system(
    # 'cd ' + os.environ['EHR_ML_BASE'] + ';'
    # +
    # '''.venv/bin/python -m ehrml.ensemble.Build ''' + dataDir + '''/data_matrix.csv -tc "''' + targetColumn + '''" -ic ''' + '"person_id" "visit_occurrence_id" -mdc "measurement_date" -adc "visit_start_date_adm" -wb ''' + str(0) + ''' -wa ''' + str(4) + ''' -sp ''' + os.environ['EICU_EHR_PIPELINE_BASE'] + '''/data/experiments/05_predict_length_of_stay/model/model_los_gt_seven_days.pkl;'''
    # )

    # log.info('''python3 -m ehrml.ensemble.Build ''' + str(dataDir) + '''/data_matrix.csv -tc "''' + targetColumn + '''" -ic ''' + '"person_id" "visit_occurrence_id" -mdc "measurement_date" -adc "visit_start_date_adm" -wb ''' + str(0) + ''' -wa ''' + str(4) + ''' -sp ''' + '''/data/experiments/05_predict_length_of_stay/model/model_los_gt_seven_days.pkl;''')

    import sys
    sys.path.append('EHR-ML')
    from ehrml.ensemble.Build import run

    modelPath = Path(modelDir, 'model.pkl')
    dirPath=Path(dataDir, 'data_matrix.csv')

    run(
    dirPath=dirPath,
    idColumns=[col.strip() for col in idColumns.split(',')],
    targetColumn=targetColumn,
    measurementDateColumn=measurementDateColumn,
    anchorDateColumn=anchorDateColumn,
    windowStart=int(windowBefore),
    windowEnd=int(windowAfter),
    savePath=modelPath
    )

    configPath = Path(modelDir, 'config.json')
    with open(configPath, 'w') as f:
        json.dump(config, f)


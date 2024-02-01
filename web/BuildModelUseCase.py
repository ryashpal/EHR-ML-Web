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

    modelUid = str(uuid.uuid4())
    modelDir = Path(modelsPath, modelUid)
    if not os.path.exists(modelDir):
        os.makedirs(modelDir)

    config = {}
    config['uid'] = modelUid
    config['window_before'] = windowBefore
    config['window_after'] = windowAfter
    config['id_columns'] = idColumns
    config['target_column'] = targetColumn
    config['measurement_date_column'] = measurementDateColumn
    config['anchor_date_column'] = anchorDateColumn
    config['date_created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log.info('NewConfig: ' + str(config))

    configPath = Path(modelDir, 'config.json')
    with open(configPath, 'w') as f:
        json.dump(config, f)

    import sys
    sys.path.append('EHR-ML')
    from ehrml.ensemble.Build import run
    from multiprocessing import Process

    modelPath = Path(modelDir, 'model.pkl')
    dirPath=Path(dataDir, 'data_matrix.csv')

    p = Process(
        target=run,
        args=(
                dirPath,
                [col.strip() for col in idColumns.split(',')],
                targetColumn,
                measurementDateColumn,
                anchorDateColumn,
                int(windowBefore),
                int(windowAfter),
                modelPath
            )
        )
    p.start()


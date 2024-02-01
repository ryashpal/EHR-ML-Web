import logging

log = logging.getLogger('EHR-ML')


def getEvaluationsConfigList(uid):
    import os
    import json
    from pathlib import Path

    evaluationsConfigList = []
    evaluationsPath = Path('data', uid, 'evaluations')
    if os.path.exists(evaluationsPath):
        evaluationsDirList = os.listdir(evaluationsPath)
        for evaluationsDir in evaluationsDirList:
            configFile = Path(evaluationsPath, evaluationsDir, 'config.json')
            log.info('configFile: ' + str(configFile))
            if os.path.exists(configFile):
                with open(configFile) as f:
                    evaluationsConfig = json.load(f)
                    evaluationsConfigList.append(evaluationsConfig)
    return evaluationsConfigList


def evaluateModel(uid, windowBefore, windowAfter, idColumns, targetColumn, measurementDateColumn, anchorDateColumn):

    import os
    import json
    import uuid

    from datetime import datetime
    from pathlib import Path

    dataDir = Path('data', uid)
    evaluationsPath = Path(dataDir, 'evaluations')
    if not os.path.exists(evaluationsPath):
        os.makedirs(evaluationsPath)

    evaluationsUid = str(uuid.uuid4())
    evaluationsDir = Path(evaluationsPath, evaluationsUid)
    if not os.path.exists(evaluationsDir):
        os.makedirs(evaluationsDir)

    config = {}
    config['uid'] = evaluationsUid
    config['window_before'] = windowBefore
    config['window_after'] = windowAfter
    config['id_columns'] = idColumns
    config['target_column'] = targetColumn
    config['measurement_date_column'] = measurementDateColumn
    config['anchor_date_column'] = anchorDateColumn
    config['date_created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log.info('NewConfig: ' + str(config))

    configPath = Path(evaluationsDir, 'config.json')
    with open(configPath, 'w') as f:
        json.dump(config, f)

    import sys
    sys.path.append('EHR-ML')
    from ehrml.ensemble.Evaluate import run
    from multiprocessing import Process

    evaluationsPath = Path(evaluationsDir, 'cv_scores.json')
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
                evaluationsPath
            )
        )
    p.start()


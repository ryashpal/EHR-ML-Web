import logging

log = logging.getLogger('EHR-ML')


def getAnalysisConfigList(uid):
    import os
    import json
    from pathlib import Path

    analysisConfigList = []
    analysisPath = Path('data', uid, 'data_window_analysis')
    if os.path.exists(analysisPath):
        analysisDirList = os.listdir(analysisPath)
        for analysisDir in analysisDirList:
            configFile = Path(analysisPath, analysisDir, 'config.json')
            log.info('configFile: ' + str(configFile))
            if os.path.exists(configFile):
                with open(configFile) as f:
                    analysisConfig = json.load(f)
                    analysisConfigList.append(analysisConfig)
    return analysisConfigList


def analyse(uid, windowBeforeList, windowAfterList, idColumns, targetColumn, measurementDateColumn, anchorDateColumn, ensembleModel):

    import os
    import json
    import uuid

    from datetime import datetime
    from pathlib import Path

    dataDir = Path('data', uid)
    analysisPath = Path(dataDir, 'data_window_analysis')
    if not os.path.exists(analysisPath):
        os.makedirs(analysisPath)

    analysisUid = str(uuid.uuid4())
    analysisDir = Path(analysisPath, analysisUid)
    if not os.path.exists(analysisDir):
        os.makedirs(analysisDir)

    config = {}
    config['uid'] = analysisUid
    config['window_before_list'] = windowBeforeList
    config['window_after_list'] = windowAfterList
    config['id_columns'] = idColumns
    config['target_column'] = targetColumn
    config['measurement_date_column'] = measurementDateColumn
    config['anchor_date_column'] = anchorDateColumn
    config['ensemble_model'] = ensembleModel
    config['date_created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log.info('NewConfig: ' + str(config))

    configPath = Path(analysisDir, 'config.json')
    with open(configPath, 'w') as f:
        json.dump(config, f)

    import sys
    sys.path.append('EHR-ML')
    from ehrml.analysis.TimeWindowAnalysis import run
    from multiprocessing import Process

    analysisPath = str(analysisDir)
    datamatrixPath=Path(dataDir, 'data_matrix.csv')

    p = Process(
        target=run,
        args=(
                datamatrixPath,
                [col.strip() for col in idColumns.split(',')],
                targetColumn,
                measurementDateColumn,
                anchorDateColumn,
                windowBeforeList,
                windowAfterList,
                ensembleModel,
                analysisPath
            )
        )
    p.start()

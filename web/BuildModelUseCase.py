import os

from pathlib import Path

import logging

log = logging.getLogger('EHR-ML')


def listModels(uid):
    modelsDir = Path('data', uid, 'models')
    if not os.path.exists(modelsDir):
        return []
    return [f for f in os.listdir(modelsDir) if (os.path.isfile(os.path.join(modelsDir, f)))]


def buildModel(uid, idColumns, targetColumn, measurementDateColumn, windowStart, windowEnd):
    modelsDir = Path('data', uid, 'models')
    if not os.path.exists(modelsDir):
        os.makedirs(modelsDir)
    log.debug('idColumns: ' + idColumns)
    log.debug('targetColumn: ' + targetColumn)
    log.debug('measurementDateColumn: ' + measurementDateColumn)
    log.debug('windowStart: ' + windowStart)
    log.debug('windowEnd: ' + windowEnd)

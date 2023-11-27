import os
import uuid
from pathlib import Path


def uploadCsv(request):
    uid = str(uuid.uuid4())
    f = request.files['file']
    dataDir = Path('data', uid)
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)
    f.save(Path(dataDir, 'data_matrix.csv'))
    return uid

from __future__ import unicode_literals

import model_class
from UploadToPostgres import *

model = model_class.ModelInstance()

print('Upload Result Start...')
UploadToPostgres()

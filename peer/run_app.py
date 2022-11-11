from environment import *
import os
import app

if os.path.isdir(DATA_FOLDER_PATH) == False:
    os.mkdir(DATA_FOLDER_PATH)

app.main.init()

app.app.run(host = '0.0.0.0', port = int(API_PORT))

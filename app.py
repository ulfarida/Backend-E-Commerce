from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import json, logging, sys
from logging.handlers import RotatingFileHandler
from blueprints import app, manager
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()

api = Api(app, catch_all_404s = True)

if __name__=='__main__':
    try:
        if sys.argv[1] =='db':
            manager.run()
    except:
        logging.getLogger().setLevel('INFO')
        formatter = logging.Formatter("[%(asctime)s]{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        log_handler = RotatingFileHandler("%s/%s" %(app.root_path, '../storage/log/app.log'),
        maxBytes = 100000, backupCount = 10)
        # log_handler.setLevel(logging.DEBUG)
        log_handler.setFormatter(formatter)
        app.logger.addHandler(log_handler)
        app.run(debug = True , host = '0.0.0.0', port = 5000)
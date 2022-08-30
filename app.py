import imp
from flask import Flask
from configs.dbcon import dbcon

app = Flask(__name__)
dbcon = dbcon()
cursor = dbcon.connect()

try:
    from controllers import *
except Exception as e:
    print(e)



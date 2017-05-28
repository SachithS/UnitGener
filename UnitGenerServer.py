"""
  UnitGenerCore.py - Server of the UnitGener
  This file is responsible for creating the routes and the server of the UnitGener core module. 
  Will create all the needed routes with params and initiate the server.

  @author      Sachith Senarathne
  @version     1.0
  @maintainer  Sachith Senarathne
  @copyright   Copyright 2017, The UnitGener Project
  @license     MIT
  @version     1.0
  @email       sachith.senarathnes@gmail.com
  @status      Development
"""

from flask import Flask, Response
from flask import request
from pystruct.learners import FrankWolfeSSVM
from pystruct.models import GraphCRF

from tokenizer import FunctionTokenizer as fT
from crfmodels import CRFPredictor as crf


app = Flask(__name__)
tokenizer = fT.FunctionTokenizer()
crfpredictor = crf.CRFPredictor()
model = GraphCRF(directed=True, inference_method="max-product")
ssvm = FrankWolfeSSVM(model=model, C=.1, max_iter=10)


@app.route('/status')
def unitgener_status():
    print ssvm
    return "Hello form UnitGener"


@app.route('/generate', methods=['POST'])
def get_unit_generated():
    _js_function = request.data
    print(_js_function)
    response = Response("99This is a plain text"
                        "kjskshjh"
                        "slkcslc"
                        "skldksl;")
    response.headers["content-type"] = "text/plain"
    return response


if __name__ == '__main__':

    result = tokenizer.read_process_file()
    train_sets = crfpredictor.generate_type1_prediction(result)
    ssvm.fit(train_sets[0], train_sets[1])
    print ssvm.predict(train_sets[0][0:1])
    app.run()

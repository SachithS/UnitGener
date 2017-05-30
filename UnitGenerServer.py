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
import urllib

from tokenizer import FunctionTokenizer as fT
from crfmodels import CRFPredictor as crf
from crfmodels import AssertionPredictor as ap


app = Flask(__name__)
tokenizer = fT.FunctionTokenizer()
crfpredictor = crf.CRFPredictor()
assert_pre = ap.AssertionPredictor()
model = GraphCRF(directed=True, inference_method="max-product")
ssvm = FrankWolfeSSVM(model=model, C=.1, max_iter=10)


@app.route('/status')
def unitgener_status():
    print ssvm
    return "Hello form UnitGener"


@app.route('/generate', methods=['POST'])
def get_unit_generated():

    print request.data
    _js_function = urllib.unquote_plus(urllib.unquote_plus(request.data))
    print _js_function
    # processed_function = process_function(_js_function)
    line_f = _js_function.replace('/n', " ")
    raw_tokens = tokenizer.init_processing_function(line_f)
    tr_sets = crfpredictor.generate_type1_prediction(raw_tokens)
    r_assert = ssvm.predict(tr_sets[0][0:1])
    unit_test = assert_pre.unit_test_assembler(r_assert, raw_tokens, 2)

    response = Response(str(unit_test))
    response.headers["content-type"] = "text/plain"
    return response


if __name__ == '__main__':

    result = tokenizer.read_process_file()
    train_sets = crfpredictor.generate_type1_prediction(result)
    ssvm.fit(train_sets[0], train_sets[1])
    result_assert = ssvm.predict(train_sets[0][0:1])
    test = assert_pre.unit_test_assembler(result_assert, result, 2)
    for f in test:
        print f

    print result_assert

    app.run()


def process_function(_js_function):
    pass

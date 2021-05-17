import subprocess
from flask import Flask, request

from model_provider import ModelProvider

app = Flask(__name__)

model_provider = ModelProvider()


@app.route('/')
def hello():
    command = "`echo hostname`"
    hostname = subprocess.check_output(['bash', '-c', command])
    return f'hello from docker container {hostname}'


@app.route('/api/model', methods=['POST'])
def set_model():
    if not request.data:
        return 'Empty content', 400
    if model_provider.save_model(str(request.data, 'utf-8')):
        return 'Model was received', 200
    return 'Error while submitting model', 500


@app.route('/api/prediction', methods=['POST'])
def prediction():
    log_dic = request.get_json()
    data = log_dic.get('log', None)
    if not data:
        return 'Invalid parameter', 400
    res = model_provider.get_prediction(data)
    if not res:
        return 'Prediction was failed, try submit a valid model', 500
    return {'result': res}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


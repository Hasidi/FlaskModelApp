import os
import subprocess
import uuid

MODEL_OUTPUT_FOLDER = 'model_output'
MODEL_FOLDER = 'model'
MODEL_FILE_PATH = f'{MODEL_FOLDER}/test_model.py'


class ModelProvider(object):
    def __init__(self):
        if not os.path.exists(MODEL_OUTPUT_FOLDER):
            os.makedirs(MODEL_OUTPUT_FOLDER)

    @staticmethod
    def save_model(model: str) -> bool:
        """
        :param string model: code as string
        :return bool: if succeeded
        """
        try:
            with open(MODEL_FILE_PATH, 'w') as f:
                f.write(model)
            return True
        except:
            return False

    @staticmethod
    def get_prediction(data: str) -> str:
        """"
        :param str data: script content
        :return: script output
        :rtype: str
        """
        output_path = f'{MODEL_OUTPUT_FOLDER}/{str(uuid.uuid4())}.txt'
        exit_code = subprocess.call(['python', MODEL_FILE_PATH, output_path, data])
        if exit_code != 0:
            return ''
        with open(output_path, 'r') as f:
            r = f.read()
        return r

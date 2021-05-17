import os
import subprocess
import uuid
from functools import lru_cache

from readerwriterlock import rwlock

MODEL_OUTPUT_FOLDER = 'model_output'
MODEL_FOLDER = 'model'
MODEL_FILE_PATH = f'{MODEL_FOLDER}/test_model.py'
LOCK_TIMEOUT_SEC = 3


class ModelProvider(object):
    def __init__(self):
        if not os.path.exists(MODEL_OUTPUT_FOLDER):
            os.makedirs(MODEL_OUTPUT_FOLDER)
        self._lock = rwlock.RWLockFairD()

    def save_model(self, model: str) -> bool:
        """
        :param string model: code as string
        :return bool: if succeeded
        """
        w_lock = self._lock.gen_wlock()
        if w_lock.acquire(timeout=LOCK_TIMEOUT_SEC):
            try:
                with open(MODEL_FILE_PATH, 'w') as f:
                    f.write(model)
                return True
            except:
                return False
            finally:
                self.get_prediction.cache_clear()
                w_lock.release()
        return False

    @lru_cache(maxsize=1000)
    def get_prediction(self, data: str) -> str:
        """"
        :param str data: script content
        :return: script output
        :rtype: str
        """
        r_lock = self._lock.gen_rlock()
        if r_lock.acquire(timeout=LOCK_TIMEOUT_SEC):
            output_path = f'{MODEL_OUTPUT_FOLDER}/{str(uuid.uuid4())}.txt'
            try:
                exit_code = subprocess.call(['python', MODEL_FILE_PATH, output_path, data], timeout=15)
            except:
                exit_code = 1
            finally:
                r_lock.release()
            if exit_code != 0:
                return ''
            with open(output_path, 'r') as f:
                return f.read()
        return ''


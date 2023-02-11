import os
import traceback
import yaml

import logging.config

from flask import Flask, request
from flask_cors import CORS
# from logger import logger

from src.json_flask import JsonFlask
from src.json_response import JsonResponse

app = JsonFlask(__name__)
CORS(app, supports_credentials=True)


@app.errorhandler(Exception)
def error_handler(e):
    return JsonResponse.error(msg=str(e))


@app.route('/cmpt/run/<path:subpath>')
def cmpt_run(subpath):
    filename = subpath.split('/')[-1]
    try:
        cmpt = __import__("cmpt." + subpath.replace('//', '/.'))
    except ModuleNotFoundError as e:
        logging.error(traceback.format_exc())
        return JsonResponse.error(msg=str("can not find service in this path: {}".format(e)))

    if hasattr(cmpt, filename):
        fun_class = getattr(cmpt, filename)
    else:
        return JsonResponse.error(msg=str("error, can not find service, maybe lost."))

    if hasattr(fun_class, "main"):
        func_proc = getattr(fun_class, "main")
        try:
            data = func_proc(fun_class)
            return {"value": data}
        except BaseException as e:
            logging.error(traceback.format_exc())
            return JsonResponse.error(msg=str("failed, process exec failed: {}".format(e)))
    else:
        return JsonResponse.error(msg=str("error, can not find main function in service."))


@app.route("/cmpt/upload", methods=["POST", "GET"])
def cmpt_upload():
    file = request.files.get("filename")
    if file is None:
        return JsonResponse.error(msg=str("failed, file upload failed."))
    file_name = file.filename.replace(" ", "")
    file.save(os.path.dirname(__file__) + '/cmpt/' + file_name)
    return {"api-url": 'http://127.0.0.1:8089/cmpt/run/' + file_name}


def setup_logging(default_path="logging.yaml", default_level=logging.INFO, env_key="LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == '__main__':
    setup_logging(default_path="config/logging.yaml")
    app.run(host='0.0.0.0', port=8089, debug=True)



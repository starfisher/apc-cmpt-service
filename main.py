import traceback
from loguru import logger
from flask import request
from flask_cors import CORS
from src.common.json_flask import JsonFlask
from src.common.json_response import JsonResponse
from src.common.system import System
from src.component.upload import upload
from src.component.run import run

app = JsonFlask(__name__)
CORS(app, supports_credentials=True)


@app.errorhandler(Exception)
def error_handler(e):
    logger.error(traceback.format_exc())
    return JsonResponse.error(msg=str(e))


@app.route('/cmpt/run/<path:subpath>')
def cmpt_run(subpath):
    input_data = request.get_json()
    module = subpath.replace('//', '/.')
    res = run(module, input_data)
    return res


@app.route("/cmpt/upload", methods=["POST", "GET"])
def cmpt_upload():
    file = request.files.get("filename")
    return upload(file)


if __name__ == '__main__':
    System.log_init()
    System.read_config(System.get_root_path()+"/config/config.ini")
    logger.info("程序启动...............")
    app.run(host=System.conf.get("flask", "host"),
            port=System.conf.getint("flask", "port"),
            debug=False)




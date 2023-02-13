import traceback
from loguru import logger
from flask import request
from flask_cors import CORS
from src.common.json_flask import JsonFlask
from src.common.json_response import JsonResponse
from src.common import system
from src.component.upload import upload

app = JsonFlask(__name__)
CORS(app, supports_credentials=True)


@app.errorhandler(Exception)
def error_handler(e):
    return JsonResponse.error(msg=str(e))


@app.route('/cmpt/run/<path:subpath>')
def cmpt_run(subpath):
    input_data = request.get_json()

    filename = subpath.split('/')[-1]
    try:
        cmpt = __import__("cmpt." + subpath.replace('//', '/.'))
    except ModuleNotFoundError as e:
        print(e)
        logger.error(traceback.format_exc())
        return JsonResponse.error(msg=str("can not find service in this path: {}".format(e)))

    if hasattr(cmpt, filename):
        fun_class = getattr(cmpt, filename)
    else:
        return JsonResponse.error(msg=str("error, can not find service, maybe lost."))

    if hasattr(fun_class, "main"):
        func_proc = getattr(fun_class, "main")
        try:
            data = func_proc(input_data, {})
            return JsonResponse.success(data=data)
        except BaseException as e:
            logger.error(traceback.format_exc())
            return JsonResponse.error(msg=str("failed, process exec failed: {}".format(e)))
    else:
        return JsonResponse.error(msg=str("error, can not find main function in service."))




@app.route("/cmpt/upload", methods=["POST", "GET"])
def cmpt_upload():
    file = request.files.get("filename")
    return upload(file)


if __name__ == '__main__':
    system.log_init()
    logger.info("程序启动...............")
    app.run(host='0.0.0.0', port=8089, debug=False)




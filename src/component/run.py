import traceback
from loguru import logger
from src.common.json_response import JsonResponse
from src.common.system import System


def run(module, input_data):
    filename = module.split('.')[-1]
    try:
        cmpt = __import__("cmpt." + module)
    except ModuleNotFoundError as e:
        logger.error(traceback.format_exc())
        return JsonResponse.error(msg=str("can not find service in this path: {}".format(e)))

    if hasattr(cmpt, filename):
        fun_class = getattr(cmpt, filename)
    else:
        return JsonResponse.error(msg=str("error, can not find service, maybe lost."))

    if hasattr(fun_class, "main"):
        func_proc = getattr(fun_class, "main")
        try:
            data = func_proc(input_data, System.get_context())
            return JsonResponse.success(data=data)
        except BaseException as e:
            logger.error(traceback.format_exc())
            return JsonResponse.error(msg=str("failed, process exec failed: {}".format(e)))
    else:
        return JsonResponse.error(msg=str("error, can not find main function in service."))
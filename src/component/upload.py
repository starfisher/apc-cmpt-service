import asyncio
import os
import re

from src.common.json_response import JsonResponse
from src.common.system import System


def download_dependence(dependence):
    if System.conf.has_option("pip", "image"):
        pip_image = ' -i ' + System.conf.get("pip", "image")
    else:
        pip_image = ''
    cmd = 'pip install {} {}'.format(dependence, pip_image)
    print(cmd)
    os.system(cmd)


def parse_import(import_str):
    depend_str = re.findall(r'#(.+)', import_str)
    if depend_str:
        depend_arr = depend_str[0].split(',')
        module_arr = re.findall(r'from\s+(.+)\s+import', import_str)
        if not module_arr:
            module_str = re.findall(r'import\s+(.+)\s+#', import_str)
            if module_str:
                module_arr = module_str[0].split(',')
        if module_arr:
            print(module_arr)
            for module in module_arr:
                try:
                    __import__(module.strip())
                except ModuleNotFoundError as e:
                    for dep in depend_arr:
                        download_dependence(dep.strip())
                    __import__(module.strip())


def check_file(file_name):
    import_start_index = -1
    code_start_index = -1
    main_func_index = -1
    code_end_index = -1
    index = 0
    with open(file_name, "r", encoding='UTF-8') as f:
        for line in f.readlines():
            line = line.strip()
            index = index + 1
            if line == '#import start':
                import_start_index = index
            if line == '### customer code start':
                code_start_index = index
            if line == 'def main(input_data, context):':
                main_func_index = index
            if line == '### customer code end':
                code_end_index = index

            if index > import_start_index and code_start_index == -1:
                parse_import(line)

    if not (code_end_index > main_func_index > code_start_index > import_start_index > 0):
        return JsonResponse.error(msg="Format validation error")

    return JsonResponse.success(msg="check succeed")


def upload(file):
    if file is None:
        return JsonResponse.error(msg=str("failed, file upload failed."))

    file_name = file.filename.replace(" ", "")
    file_save_path = System.get_root_path() + 'cmpt/' + file_name
    file.save(file_save_path)

    res = check_file(file_save_path)
    if res.code != 0:
        return res

    return {"api-url": "http://{}:{}/cmpt/run/{}".format(System.get_local_ip(), System.conf.get("flask", "port"), file_name.split('.')[0])}

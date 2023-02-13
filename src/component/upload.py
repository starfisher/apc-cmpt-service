import asyncio
import os
import re

from src.common.json_response import JsonResponse
from src.common.system import get_root_path


async def download_dependence(dependence):
    cmd = 'pip install {} -i https://pypi.tuna.tsinghua.edu.cn/simple'.format(dependence)
    print(cmd)
    os.system(cmd)


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
                module = re.findall(r'#(.+)', line)
                if module:
                    module_arr = module[0].split(',')
                    for str in module_arr:
                        asyncio.run(download_dependence(str.strip()))
                        # cmd = 'pip install {} -i https://pypi.tuna.tsinghua.edu.cn/simple'.format(str.strip())
                        # print(cmd)
                        # os.system(cmd)

    if not (code_end_index > main_func_index > code_start_index > import_start_index > 0):
        return JsonResponse.error(msg="Format validation error")

    return JsonResponse.success(msg="check succeed")


def upload(file):
    if file is None:
        return JsonResponse.error(msg=str("failed, file upload failed."))

    file_name = file.filename.replace(" ", "")
    file_name = get_root_path() + 'cmpt/' + file_name
    file.save(file_name)

    res = check_file(file_name)
    if res.code != 0:
        return res
    return {"api-url": 'http://127.0.0.1:8089/cmpt/run/' + file_name[len(get_root_path()): file_name.find('.')]}

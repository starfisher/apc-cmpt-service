import re

if __name__ == '__main__':
    module = re.findall(r'#(.+)', '# numpy, #sel')
    module[0].split(',')
    print(module)


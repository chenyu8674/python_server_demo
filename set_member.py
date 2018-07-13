import argparse
import urllib.parse
import file_tools

#设置id-姓名列表
try:
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--id', type = int, default = -1)
    parser.add_argument('--name', type = str, default = None)
    args = parser.parse_args()
    if args.id < 0:
        print('{"result":"False","msg":"invalid id"}')
    else:
        id = str(args.id)
        name = args.name
        name = urllib.parse.unquote(name, "utf-8")
        file_tools.write_line('data_member.txt', id, name)
        print('{"result":"True"}')
except BaseException as e:
    print('{"result":"False","msg":"%s"}' %str(e))

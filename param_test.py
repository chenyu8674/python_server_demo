import argparse

try:
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--id', type = int, default = -1)
    parser.add_argument('--name', type = str, default = None)
    args = parser.parse_args()
    if args.id < 0:
        print('{"result":"False","msg":"invalid id"}')
    else:
        id = args.id
        name = args.name
        name = name.encode(encoding = "utf-8")
        print('{"result":"True","id":"%d","name":"%s"}' %(id, name))
except BaseException as e:
    print('{"result":"False","msg":"%s"}' %str(e))

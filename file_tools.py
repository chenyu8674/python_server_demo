def write_line(fileName, flag, string):
    data = ""
    with open(fileName, 'r+') as f:
        for line in f.readlines():
            if(line.find(flag + "-") == 0):
                continue
            else:
                data += line
    with open(fileName, 'r+') as f:
        f.truncate()
        f.writelines(data)
        f.write("%s-%s\n" %(flag, string))

def read_line(fileName, flag):
    with open(fileName, 'r+') as f:
        for line in f.readlines():
            if(line.find(flag + "-") == 0):
                line = line.split("-")
                line = line[1]
                if(line.endswith("\n")):
                    line = line[0 : len(line) - 1]
                return line

def write_all(fileName, string):
    with open(fileName, 'r+') as f:
        f.truncate()
        f.write(string)

def read_all(fileName):
    with open(fileName, 'r+') as f:
        return f.read()

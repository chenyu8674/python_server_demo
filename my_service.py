# -*- coding: utf-8 -*-
import http.server as hs
import os, subprocess

#服务器内部错误
class ServerException(Exception):
    pass

#输入路径不存在时的处理
class case_no_path(object):
    def test(self, handler):
        #判断时排除?后面附带的参数
        path = handler.full_path.split("?")
        return not os.path.exists(path[0])
    def act(self, handler):
        raise ServerException("{0} not found".format(handler.path))

#输入路径是一个脚本时的处理
class case_CGI_file(object):
    def test(self, handler):
        path = handler.full_path.split("?")
        return os.path.isfile(path[0]) and path[0].find('.py') >= 0
    def act(self, handler):
        handler.run_cgi(handler.full_path)

#输入路径是一个文件时的处理
class case_is_file(object):
    def test(self, handler):
        path = handler.full_path.split("?")
        return os.path.isfile(path[0])
    def act(self, handler):
        handler.handle_file(handler.full_path)

#所有情况都不符合时的处理
class case_allother_fail(object):
    def test(self, handler):
        return True
    def act(self, handler):
        raise ServerException("Unknown object {0}".format(handler.full_path))

class RequestHandler(hs.BaseHTTPRequestHandler):
    #请求路径合法则返回相应处理，否则返回错误页面
    full_path = ""
    #条件类的优先顺序不同，对于文件的捕捉能力也不同，越是针对某种特例的条件类，越应该放在前面。
    cases = [case_no_path(), case_CGI_file(), case_is_file(), case_allother_fail()]
    #错误页面html
    Error_Page = """
        <html>
        <meta http-equiv="content-type" content="text/html;charset=UTF-8" />
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """

    def run_cgi(self, fullpath):
        #运行脚本并得到格式化的输出
        #参数以url?param1=1&param2=2……的方式传递，处理方式见param_test.py
        path = fullpath.split("?")
        if len(path) > 1:
            params = path[1]
            params = params.split("&")
            shell = []
            shell.append("python")
            shell.append(path[0])
            for param in params:
                shell.append("--" + param)
            data = subprocess.check_output(shell)
        else:
            data = subprocess.check_output(["python", path[0]])
        self.send_content(page = str(data, encoding = 'utf-8'))

    #结果输出方法
    def send_content(self, page, status = 200):
        self.send_response(status)
        self.send_header("Content-type", 'text/html')
        self.end_headers()
        self.wfile.write(bytes(page, encoding = 'utf-8'))

    #服务收到的GET请求会自动调用次方法，需手动实现处理逻辑
    def do_GET(self):
        #这里要处理两个异常，一个是读入路径时可能出现的异常，一个是读入路径后若不是文件，要作为异常处理
        try:
            #获取文件路径
            self.full_path = os.getcwd() + self.path
            #判断路径对应的类型并执行相应处理
            for case in self.cases:
                if case.test(self):
                    case.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)

    def handle_file(self, full_path):
        try:
            #处理过程中需先截掉参数，否则会判断为文件不存在
            full_path = full_path.split("?")
            full_path = full_path[0]
            #判断文件类型以设置mimetype
            mimetype = ""
            if self.path.endswith(".html"):
                mimetype='text/html'
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
            if self.path.endswith(".png"):
                mimetype='image/png'
            if self.path.endswith(".gif"):
                mimetype='image/gif'
            if self.path.endswith(".js"):
                mimetype='application/javascript'
            if self.path.endswith(".css"):
                mimetype='text/css'
            if self.path.endswith(".apk"):
                mimetype='application/vnd.android.package-archive'
            self.send_response(200)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            with open(full_path, 'rb') as f:
                self.wfile.write(f.read())
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, 404)

#启动服务
httpAddress = ('', 8000)
httpd = hs.HTTPServer(httpAddress, RequestHandler)
httpd.serve_forever()
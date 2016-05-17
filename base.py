#coding=utf-8
import os

import tornado.web

__author__ = 'zyf'

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("glxt_user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)
    @property
    def db(self):
        return self.application.db

    url_pattern = None

def route(url_pattern):
    """
    路由装饰器, 只能装饰 RequestHandler 子类
    """

    def handler_wapper(cls):
        assert (issubclass(cls, BaseHandler))
        cls.url_pattern = url_pattern
        return cls

    return handler_wapper
def find_handles(path='/module',handles_file='service.py'):
    abs_path = os.getcwd() + path
    files = os.listdir(abs_path)
    handle_list = []
    for f in files:
        if f == handles_file:
            handle_list.append(path[1:] + '.' + f[:-3])
        if os.path.isdir(abs_path + '/' + f):
            f_files = os.listdir(abs_path + '/' + f)
            for ff in f_files:
                if ff == handles_file:
                    handle_list.append(path[1:] + '.' + f + '.' + ff[:-3])
    dir_handle_list=[]
    for handle in handle_list:
        exec ('import %s' % handle)
        dir_handle = eval(handle)
        dir_handle_list.append(dir_handle)
    return dir_handle_list
if __name__=="__main__":
    print find_handles('/module')
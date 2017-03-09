# coding:utf8
import tornado.web
import re
import functools

is_output_no_login_visit = True
is_output_no_permission_visit = True


class RestfulHandler(tornado.web.RequestHandler):
    @property
    def db_session(self):
        if not hasattr(self, "_db_session") or getattr(self, "_db_session") == None:
            self._db_session = self.application.database.get_session()
        return self._db_session

    def get_new_db_session(self):
        return self.application.database.get_session()

    def close_db_session(self):
        if hasattr(self, "_db_session") and getattr(self, "_db_session") != None:
            self._db_session.close()
    def on_finish(self):
        if hasattr(self, "_db_session"):
            self._db_session.close()

    def get_current_user(self):
        '''session_id = self.get_secure_cookie("session_id")
        if session_id == None:
            return None
        db_session=self.db_session
        user_session=get_user_session(db_session,session_id)
        if user_session == None or user_session.is_login == False:
            return None
        now_t=datetime.datetime.now()
        elapse=(now_t-user_session.last_visit_time).total_seconds()
        if elapse > session_valid_time:
            return None
        user_session.last_visit_time=now_t
        db_session.commit()
        return user_session.user'''
        session_id = self.get_secure_cookie("session_id")
        if session_id == None:
            return None
        return get_user_by_session_id(self.db_session, session_id)


def permission_check(current_path, uri, request, method, *args, **kwargs):
    if request.current_user is None:
        if is_output_no_login_visit:
            print ("权限控制:未登陆注册用户访问 path=%s uri=%s" % (current_path, uri))
        return False
    url_count = request.current_user.session.url_handles.filter_by(path=uri, action_type=method).count()
    if url_count == 0:
        if is_output_no_permission_visit:
            print ("权限控制:用户访问未授权网址 user_email=%s path=%s uri=%s" % (request.current_user.email, current_path, uri))
        return False
    return True


def login_required(current_path, uri, request, method, *args, **kwargs):
    if request.current_user is None:
        return False
    return True


class HttpUri(object):
    POST = 2
    GET = 1
    PUT = 3
    DELETE = 4
    HEAD = 5
    OPTIONS = 6
    PATCH = 7

    def __init__(self, base_uri, base_cls):
        self._base_uri = base_uri
        self._dispatcher = {}
        self.base_cls = base_cls
        self.record_cls = None

    def _get_dispatcher_class(self, key):
        class FunctionDispatcher(self.base_cls):
            _dispatcher_get = []
            _dispatcher_post = []
            _dispatcher_put = []
            _dispatcher_delete = []
            _dispatcher_head = []
            _dispatcher_options = []
            _dispatcher_patch = []

            def _dispatch(self, dispatcher, method):
                # self.set_header("Content-Type","application/json")
                self.set_header("Server", "")
                for k in dispatcher:
                    match = k[0].match(self.request.path)
                    if match:
                        aa=match.groups()
                        path_args = [tornado.web._unquote_or_none(s)
                                     for s in match.groups()]
                        return k[1](self.request.path, k[0].pattern, self, method, *path_args)
                raise tornado.web.HTTPError(404)

            def head(self):
                self._dispatch(self._dispatcher_head, HttpUri.HEAD)

            def get(self):
                self._dispatch(self._dispatcher_get, HttpUri.GET)

            def post(self):
                self._dispatch(self._dispatcher_post, HttpUri.POST)

            def delete(self):
                self._dispatch(self._dispatcher_delete, HttpUri.DELETE)

            def patch(self):
                self._dispatch(self._dispatcher_patch, HttpUri.PATCH)

            def put(self):
                self._dispatch(self._dispatcher_put, HttpUri.PUT)

            def options(self):
                self._dispatch(self._dispatcher_options, HttpUri.OPTIONS)

            @classmethod
            def add_path(cls, method, uri, func):
                if method == HttpUri.GET:
                    cls._dispatcher_get.append((uri, func))
                    return True
                elif method == HttpUri.POST:
                    cls._dispatcher_post.append((uri, func))
                    return True
                elif method == HttpUri.PUT:
                    cls._dispatcher_put.append((uri, func))
                    return True
                elif method == HttpUri.DELETE:
                    cls._dispatcher_delete.append((uri, func))
                    return True
                elif method == HttpUri.HEAD:
                    cls._dispatcher_head.append((uri, func))
                    return True
                elif method == HttpUri.OPTIONS:
                    cls._dispatcher_options.append((uri, func))
                    return True
                elif method == HttpUri.PATCH:
                    cls._dispatcher_patch.append((uri, func))
                    return True
                return False

        return FunctionDispatcher


    def route(self, method, resource_name, path, uri_name, permission_func=permission_check, is_record=True,
              is_async=False):
        def _deco(func):
            @functools.wraps(func)
            def wrapper(current_path, uri, handle, method, *args, **kwargs):
                user_id = 0
                content = current_path
                if handle.current_user:
                    user_id = handle.current_user.id
                if is_async:
                    pass
                return
                raise tornado.web.HTTPError(403)

            func.affect = uri_name
            handle_cls = self._get_dispatcher(resource_name)
            if handle_cls == None:
                handle_cls = self._get_dispatcher_class(resource_name)
                self._add_dispatcher(resource_name, handle_cls)
            uri = self._base_uri + resource_name + path + '$'
            uri = re.compile(uri)
            handle_cls.add_path(method, uri, wrapper)
            handle_cls.func_name = func.func_name
            return wrapper

        return _deco

    def _get_dispatcher(self, key):
        if self._dispatcher.has_key(key):
            return self._dispatcher[key]
        return None

    def _add_dispatcher(self, key, handle):
        self._dispatcher[key] = handle

    def build_handle(self):
        handlers = []
        for key in self._dispatcher:
            uri = r"%s%s/.*" % (self._base_uri, key)
            handlers.append((uri, self._dispatcher[key]))
        return handlers


class DispatchApplication(tornado.web.Application):
    def __init__(self, handlers):
        tornado.web.Application.__init__(self, handlers, cookie_secret="123456", )


def main():
    v1_uri = HttpUri("/service/v1/", RestfulHandler)
    v2_uri = HttpUri("/service/v2/", RestfulHandler)

    @v1_uri.route(HttpUri.GET, "adb", "/aaa/", "ddsdf")
    def compute(handle):
        handle.write("hello world id role")

    @v2_uri.route(HttpUri.GET, "burst_project", "/current_user/([0-9a-z]+)", "更新本单位工程")
    def get_user_role_by_id(handle, id):
        handle.write("hello world id role")

    import logging
    from tornado.ioloop import IOLoop
    from tornado.httpserver import HTTPServer
    from tornado.options import define, options, parse_command_line

    define("port", default=8888, help="Run on the given port", type=int)
    parse_command_line()
    logging.info(
        "Test Server Listening on http://0.0.0.0:%s/" % options.port
    )
    handle = []
    handle += v1_uri.build_handle()
    handle += v2_uri.build_handle()
    http_server = HTTPServer(DispatchApplication(handle))
    http_server.listen(options.port)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()


# coding=utf-8
"""
@version: ??
@author: zhayufeng
@describe:
@contact: zyfjfj@163.com
@software: PyCharm
@file: t
@time: 2016/12/7 15:02
"""


class Foo(object):
    price = 100

    @classmethod
    def how_much_of_book(cls, n):
        return cls.price * n

    @property
    def x(self):
        return self.myx

    @x.setter
    def x(self, myx):
        self.myx = myx

foo = Foo()
foo.x = 100
print foo.x
print dir(foo)


class Author(type):
    """
    Metaclass for all models.
    """
    def __new__(cls, name, bases, attrs):
        if "name" in attrs:
            attrs["author"] = attrs["name"]
        return super(Author, cls).__new__(cls, name, bases, attrs)


class MyApp(object):
    """
    new class
    """
    __metaclass__ = Author

    def __init__(self):
        self.func_map = {}
        self.name = "zyf"

    def register(self, name):
        """
        register
        """
        def func_wrapper(func):
            """
            func
            """
            self.func_map[name] = func

            def _inner(*arg, **kw):
                print func.__name__
                return func(*arg, **kw)
            return _inner
        return func_wrapper

    def call_method(self, name=None):
        func = self.func_map.get(name, None)
        if func is None:
            raise Exception("No function registered against - " + str(name))
        return func()


class MyAppTwo(MyApp):
    __metaclass__ = Author
    pass


def register(name):
    def func_wrapper(func):
        def _inner(*arg, **kw):
            print "%s is running" % func.__name__
            return func(*arg, **kw)
        return _inner
    return func_wrapper
app = MyApp()


def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                print "%s is running" % func.__name__
            return func(*args, **kwargs)
        return wrapper

    return decorator


@app.register('/next_page')
def next_page_func():
    return "This is the next page."


# print app.func_map
# next_page_func()
print dir(MyApp)
print hasattr(app, "name")

# a = [x * x for x in range(0, 100) if x % 9 == 0]
# print a
# a = MyAppTwo()

from functools import wraps
def logged(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print func.__name__ + " was called"
        return func(*args, **kwargs)
    return with_logging

@logged
def test(x):
    return x + x * x
test=logged(test)

def get_large(a):
    for i in range(a):
        yield i-10
for i in get_large(100):
    print i
import tornado.ioloop
from controller import *


def main():
    controller = router()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

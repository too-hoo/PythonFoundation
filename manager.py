#!/usr/bin/env python3
# -*-encoding:UTF-8-*-

from flask_script import Manager
from hello import app

manager = Manager(app)


@manager.option('-n', '--name', dest='name', default='toohoo')
def hello(name):
    'say hello'
    print('hello', name)


@manager.command
def init_database():
    '初始化数据库'
    print('init database...')


if __name__ == '__main__':
    manager.run()

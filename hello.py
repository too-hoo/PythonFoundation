from flask import Flask
from flask import render_template
from flask import request, make_response, redirect
from flask import flash, get_flashed_messages
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
# 进行jinja2 的行语法表达式的时候需要加上这个声明
app.jinja_env.line_statement_prefix = '#'
# 在进行flash显示的时候要先设置一个secretkey保证统一
app.secret_key = 'toohoo'


@app.route('/index/')
@app.route('/')
def index():
    res = ''
    for msg, category in get_flashed_messages(with_categories=True):
        res = res + category + msg + '<br>haha'
    res += 'hello'
    return res


@app.route('/profile/<int:uid>', methods=['GET', 'post'])
def profile(uid):
    colors = ('red', 'green', 'red', 'green')
    infos = {'toohoo': 'abc', 'zhihu': 'def'}
    return render_template('profile.html', uid=uid, colors=colors, infos=infos)


@app.route('/request')
def request_demo():
    key = request.args.get('key', 'defaultkey')
    res = request.args.get('key', 'defaultkey') + '<br>'
    res = res + request.url + '++' + request.path + '<br>'
    for property in dir(request):  # 遍历request里面的方法使用haha字符串连接起来
        res = res + str(property) + '<br>haha' + str(eval('request.' + property)) + '<br>haha'
    response = make_response(res)
    response.set_cookie('toohooid', key)  # 这是名字为toohooid的键为默认的值defaultkey的cookie
    response.status = '404'  # 使用F12 开发者工具可以查看状态
    response.headers['toohoo'] = 'hello~~'  # 在头部添加一个键值对
    return response


@app.route('/newpath')
def newpath():
    return 'newpath'  # 解析路径并返回路径


@app.route('/re/<int:code>')  # 重定向例子
def redirect_demo(code):
    return redirect('/newpath', code=code)


# 对出错页面和404页面进行统一的处理
@app.errorhandler(400)
def exception_page(e):
    response = make_response('出错啦！')
    return response


@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html', url=request.url), 404


@app.route('/admin')
def admin():
    if request.args['key'] == 'admin':
        return 'hello admin'
    else:
        raise Exception()


# flash处理
@app.route('/login')
def login():
    app.logger.info('login success')
    flash('登录成功', 'info')
    return 'ok'
    # return redirect('/')  # 跳转到首页


@app.route('/log/<level>/<msg>/')
def log(level, msg):
    dict = {'info': logging.INFO, 'warn': logging.WARN, 'error': logging.ERROR}
    print(level in dict.keys())
    if level in dict.keys():
        print(dict[level])
        app.logger.log(dict[level], msg)
    return 'logged:' + msg


def set_logger():
    logging.basicConfig(level=logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(lineno)d %(message)s')

    info_log_handler = RotatingFileHandler(filename='./logs/info.txt', maxBytes=1024*1024, backupCount=10)
    info_log_handler.setLevel(logging.INFO)
    info_log_handler.setFormatter(formatter)
    app.logger.addHandler(info_log_handler)

    warn_log_handler = RotatingFileHandler(filename='./logs/warn.txt', maxBytes=1024 * 1024, backupCount=10)
    warn_log_handler.setLevel(logging.WARN)
    warn_log_handler.setFormatter(formatter)
    app.logger.addHandler(warn_log_handler)

    error_log_handler = RotatingFileHandler(filename='./logs/error.txt', maxBytes=1024 * 1024, backupCount=10)
    error_log_handler.setLevel(logging.ERROR)
    error_log_handler.setFormatter(formatter)
    app.logger.addHandler(error_log_handler)

    # logging.getLogger().addHandler(file_log_handler)

# def set_logger():
#     logging.basicConfig(level=logging.DEBUG)
#
#     info_file_handler = RotatingFileHandler('./logs/info.txt')
#     info_file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(info_file_handler)
#
#     warn_file_handler = RotatingFileHandler('./logs/warn.txt')
#     warn_file_handler.setLevel(logging.WARN)
#     app.logger.addHandler(warn_file_handler)
#
#     error_file_handler = RotatingFileHandler('./logs/error.txt')
#     error_file_handler.setLevel(logging.ERROR)
#     app.logger.addHandler(error_file_handler)



if __name__ == '__main__':
    set_logger()
    app.run(debug=True)

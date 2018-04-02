from flask import Flask
app = Flask(__name__)

#装饰器@开头 在函数上面,这个的作用是url和view的映射
#http://lib.csdn.net/article/python/62942
#< 函数+实参高阶函数+返回值高阶函数+嵌套函数+语法糖 = 装饰器 >
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

if __name__=='__main__':
    app.run(debug = True)

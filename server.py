#coding=utf-8
import tornado.ioloop
import tornado.web
import time
import os
global models

#TODO 修改命名取值
composer_list = ['mozart']

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html',composers=composer_list)

class GetMidiHandler(tornado.web.RequestHandler):
    def post(self):
        composer = self.get_argument("composer","error");

        if composer == 'error' or composer not in composer_list:
            self.write("Error!")
        else:

            #真实路径
            filepath = "tmp_music/%s_%s.mid"%(composer,''.join(('%f'%time.time()).split('.')))
            #调试路径
            filepath = "tmp_music/%s.mid"%composer
            #TODO 调用model生成midi,保存到filepath

            #读取Midi,以HTTP格式传输
            buffer_size = 4096
            self.set_header ('Content-Type', 'audio/mid')
            self.set_header ('Content-Disposition', 'attachment; filename=' + composer+".mid")
            with open(os.path.join(os.path.dirname(__file__),filepath),'rb') as f:
                while True:
                    data = f.read(buffer_size)
                    if not data:
                        break
                    self.write(data)
            try:
                os.remove(filepath)
            except OSError:
                print "OS_ERROR"
        self.finish()



settings = {
    "xsrf_cookies": False
}

def make_app():
    return tornado.web.Application(
        handlers=[
            (r"/", MainHandler),
            (r"/music.mid", GetMidiHandler),
        ],
        template_path=os.path.join(os.path.dirname(__file__), "template"),
        **settings
    )

if __name__ == "__main__":
    models = []
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
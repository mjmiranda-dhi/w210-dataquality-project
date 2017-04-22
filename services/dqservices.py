import tornado.ioloop
import tornado.web
import os,uuid

__UPLOADS__ = "/Users/mjmiranda/Documents/mids/spring2017/w210/project/w210-dataquality-project/web/tmp/"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, World!")

class ModelHandler(tornado.web.RequestHandler):
    def post(self):
        print("ModelHandler::post")
        #data = tornado.escape.json_decode(self.request.body)
        #print(data)
        filename = self.get_argument("filename")
        print("ModelHandler::post:filename=",filename)

        userfile = self.request.files["userfile"][0]
        print("userfile is", userfile)
        fname = userfile['filename']
        print("ModelHandler::userfile:filename:",fname)
        extn = os.path.splitext(fname)[1]
        print("ModelHandler::userfile:extension:",extn)
        cname = str(uuid.uuid4()) + extn
        print("ModelHandler::userfile:cname:",cname)
        with open(__UPLOADS__+cname, 'wb') as fh:
            fh.write(userfile['body'])

        self.finish(cname + " is uploaded! Check %s folder" % (__UPLOADS__))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/model", ModelHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen("8765")
    tornado.ioloop.IOLoop.current().start()

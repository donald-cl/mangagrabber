import tornado.web
from cookie import COOKIE_NAME

class BaseHandler(tornado.web.RequestHandler):

    debug = True

    def success(self, success_msg):
        if self.debug:
            print "[SUCCESS] : %s" %success_msg

    def failure(self, error_msg):
        self.set_status(400)
        self.write(error_msg)

        if self.debug:
            print "[ERROR] : %s" % error_msg

class BaseAuthHandler(BaseHandler):

    def get_current_user(self):
        return self.get_secure_cookie(COOKIE_NAME)

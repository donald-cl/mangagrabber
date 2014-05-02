import tornado.web
from cookie import COOKIE_NAME
from base import BaseHandler

class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        email = self.get_argument("email", default="", strip=True)
        passw = self.get_argument("passw", default="", strip=True)

        if not email:
            self.failure("Invalid login")
            return
        if not passw:
            self.failure("Invalid login")
            return

        email = email.lower()

        '''
        u = User.objects(email=email)
        if not u:
            self.failure("Invalid login")
            return

        u = u[0]

        if u.passw is not None and u.passw == passw:
            self.write("Login successful")
            self.success("Login successful with %s" % email)
            self.set_secure_cookie(COOKIE_NAME, email)
            self.redirect("/", permanent = True)
        else:
            self.failure("Invalid login")
        '''

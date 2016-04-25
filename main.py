import webapp2
from google.appengine.api import oauth

app = webapp2.WSGIApplication([
	('/user', 'user.User'),
], debug=True)
app.router.add(webapp2.Route(r'/user/<id:[0-9]+><:/?>', 'user.User'))
app.router.add(webapp2.Route(r'/user/<uid:[0-9]+><:/?>/list/<lid:[0-9]+><:/?>', 'user.UserList'))
app.router.add(webapp2.Route(r'/user/search', 'user.UserSearch'))
app.router.add(webapp2.Route(r'/list', 'list.List'))
app.router.add(webapp2.Route(r'/list/<lid:[0-9]+><:/?>', 'list.List'))
app.router.add(webapp2.Route(r'/list/<lid:[0-9]+>/user/<uid:[0-9]+><:/?>', 'list.ListUsers'))

import webapp2
from google.appengine.ext import ndb
import db_models
import json

class User(webapp2.RequestHandler):
	def post(self):
		"""Creates a User entity
		
		POST Body Variables:
		username - Required. Username
		email - Required. Email
		name - Real name
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
			return
		new_user = db_models.User()
		username = self.request.get('username', default_value=None)
		email = self.request.get('email', default_value=None)
		name = self.request.get('name', default_value=None)
		if username:
			new_user.username = username
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, username is Required"
		if email:
			new_user.email = email
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request, email is Required"
		if name:
			new_user.name = name
		key = new_user.put()
		out = new_user.to_dict()
		self.response.write(json.dumps(out))
		return
	
	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
			return
		if 'id' in kwargs:
			out = ndb.Key(db_models.User, int(kwargs['id'])).get().to_dict()
			self.response.write(json.dumps(out))
		else:
			q = db_models.User.query()
			keys = q.fetch(keys_only=True)
			results = { 'keys' : [x.id() for x in keys]}
			self.response.write(json.dumps(results))	

class UserUpdate(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
			return
		if 'id' in kwargs:
			username = self.request.get('username', default_value=None)
			email = self.request.get('email', default_value=None)
			name = self.request.get('name', default_value=None)
			# find user to update
			q = db_models.User.query()
			q = q.filter(db_models.User.username == username)
			print q
			
			#out = ndb.Key(db_models.User, int(kwargs['id'])).get().to_dict()
			#self.response.write(json.dumps(out))

class UserDelete(webapp2.RequestHandler):
	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
			return
		if 'id' in kwargs:
			user = User()
			userDict = ndb.Key(db_models.User, int(kwargs['id'])).get().to_dict()
			user.key = userDict['key']
			self.response.write(user)
		else:
			q = db_models.User.query()
			keys = q.fetch(keys_only=True)
			results = { 'keys' : [x.id() for x in keys]}
			#self.response.write(json.dumps(results))
		
class UserSearch(webapp2.RequestHandler):
	def post(self):
		'''
		Search for users
		
		POST Body Variables:
		username = String. Username
		email - String. Email address
		'''
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
			return
		q = db_models.User.query()
		if self.request.get('username',None):
			q = q.filter(db_models.User.username == self.request.get('username'))
		if self.request.get('email',None):
			q = q.filter(db_models.User.email == self.request.get('email'))
		keys = q.fetch(keys_only=True)
		results = { 'keys' : [x.id() for x in keys]}
		self.response.write(json.dumps(results))
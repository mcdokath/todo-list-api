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
		lists[] - Lists user has authored
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
			return
		new_user = db_models.User()
		username = self.request.get('username', default_value=None)
		email = self.request.get('email', default_value=None)
		name = self.request.get('name', default_value=None)
		lists = self.request.get_all('lists[]', default_value=None)
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
		if lists:
			for list in lists:
				new_user.lists.append(ndb.Key(db_models.List, int(list)))
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
			
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
			return
		if 'id' in kwargs:
			user = ndb.Key(db_models.User, int(kwargs['id'])).get()
			if not user:
				self.response.status = 404
				self.response.status_message = "User Not Found"
				return
			username = self.request.get('username', default_value=None)
			if username:
				user.username = username
			email = self.request.get('email', default_value=None)
			if email:
				user.email = email
			name = self.request.get('name', default_value=None)
			if name:
				user.name = name
			lists = self.request.get_all('lists[]', default_value=None)
			if lists:
				for list in lists:
					if list not in user.lists:
						user.lists.append(ndb.Key(db_models.List, int(list)))
						user.put()
		self.response.write(json.dumps(user.to_dict()))
		return
		
	def delete(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
			return
		if 'id' in kwargs:
			self.response.write("User exists")
			out = ndb.Key(db_models.User, int(kwargs['id'])).get()
			# delete all lists that user authored
			userLists = db_models.User.query(db_models.List.author == out.key).fetch(keys_only=True)
			ndb.delete_multi(userLists)
			# delete user
			out.key.delete()
			self.response.write("User deleted")
		else:
			self.response.status = 404
			self.response.status_message = "Error, user not found"
			return

class UserList(webapp2.RequestHandler):
	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
		if 'uid' in kwargs:
			user = ndb.Key(db_models.User, int(kwargs['uid']))
			if not user:
				self.response.status = 404
				self.response.status_message = "User Not Found"
				return
		if 'lid' in kwargs:
			list = ndb.Key(db_models.List, int(kwargs['lid'])).get()
			if not list:
				self.response.status = 404
				self.response.status_message = "List Not Found"
				return
		if list not in user.lists:
			user.lists.append(list)
		self.response.write(json.dumps(list.to_dict()))
		
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
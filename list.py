import webapp2
from google.appengine.ext import ndb
import db_models
import json

class List(webapp2.RequestHandler):
	def post(self):
		"""Creates a List entity
		
		POST Body Variables:
		name - Required. List name
		author - Required. User who authored the list
		users[] - Array of user ids
		items[] - Array of list items
		"""
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
			return
		new_list = db_models.List()
		name = self.request.get('name', default_value=None)
		author = self.request.get('author', default_value=None)
		users = self.request.get_all('users[]', default_value=None)
		items = self.request.get_all('items[]', default_value=None)
		if name:
			new_list.name = name
		else:
			self.response.status = 400
			self.response.status_message = "Invalid request"
		if author:
			new_list.author = ndb.Key(db_models.User, int(author))
		if users:
			for user in users:
				new_list.users.append(ndb.Key(db_models.User, int(user)))
		if items:
			new_list.items = items
		for item in new_list.items:
			print item
		key = new_list.put()
		out = new_list.to_dict()
		self.response.write(json.dumps(out))
		return

	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
			return
		if 'id' in kwargs:
			out = ndb.Key(db_models.List, int(kwargs['id'])).get().to_dict()
			self.response.write(json.dumps(out))
		else:
			q = db_models.List.query()
			keys = q.fetch(keys_only=True)
			results = { 'keys' : [x.id() for x in keys]}
			self.response.write(json.dumps(results))

class ListUsers(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
			return
		if 'lid' in kwargs:
			list = ndb.Key(db_models.List, int(kwargs['lid'])).get()
			if not list:
				self.response.status = 404
				self.response.status_message = "List Not Found"
				return
		if 'uid' in kwargs:
			user = ndb.Key(db_models.User, int(kwargs['uid']))
			if not user:
				self.response.status = 404
				self.response.status_message = "User Not Found"
				return
		if user not in list.users:
			list.users.append(user)
			list.put()
		self.response.write(json.dumps(list.to_dict()))
		return
		
	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status = 406
			self.response.status_message = "Not Acceptable, API only supports application/json MIME type"
		if 'lid' in kwargs:
			list = ndb.Key(db_models.List, int(kwargs['lid'])).get()
			if not list:
				self.response.status = 404
				self.response.status_message = "List Not Found"
				return
		if 'uid' in kwargs:
			user = ndb.Key(db_models.User, int(kwargs['uid']))
			if not user:
				self.response.status = 404
				self.response.status_message = "User Not Found"
				return
		if user not in list.users:
			self.response.status = 404
			self.response.status_message = "User Not Associated With This List"
		self.response.write(json.dumps(list.to_dict()))
from google.appengine.ext import ndb

class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class Update(Model):
	date_time = ndb.DateTimeProperty(required=True)
	user_count = ndb.IntegerProperty(required=True)
	message_count = ndb.IntegerProperty(required=True)

class List(Model):
	name = ndb.StringProperty(required=True)
	author = ndb.KeyProperty(required=True)
	items = ndb.StringProperty(repeated=True)
	users = ndb.KeyProperty(repeated=True)
	updates = ndb.StructuredProperty(Update, repeated=True)

	def to_dict(self):
		d = super(List,self).to_dict()
		d['users'] = [m.id() for m in d['users']]
		return d

class User(Model):
	username = ndb.StringProperty(required=True)
	email = ndb.StringProperty(required=True)
	name = ndb.StringProperty()
	lists = ndb.KeyProperty(repeated=True)

	def to_dict(self):
		d = super(User,self).to_dict()
		d['lists'] = [m.id() for m in d['lists']]
		return d
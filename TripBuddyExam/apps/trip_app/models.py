from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
import datetime

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class UserManager(models.Manager):
	def validateRegistration(self, postData):
		errors = []
		if len(postData['first_name']) < 1:
			errors.append("First name must be at least 1 character")
		if len(postData['last_name']) < 1:
			errors.append("Last name must be at least 1 character")
		if len(postData['email']) < 5:
			errors.append("email is too short")
		if not EMAIL_REGEX.match(postData['email']):
			errors.append("Please enter a valid email")
		if len(postData['pw']) < 8:
			errors.append("Password must be at least 8 characters")
		if postData['pw'] != postData['cw']:
			errors.append("Passwords don't match")
		if len(errors):
			return errors
		me = User.objects.create(
				first_name=postData['first_name'],
				last_name=postData['last_name'],
				email=postData['email'],
				password= bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt())
			)
		return me

	def validateLogin(self, postData):
		errors = []
		existing_user_list = User.objects.filter(email=postData['email'])
		if len(existing_user_list):
			if bcrypt.checkpw(postData['pw'].encode(), existing_user_list[0].password.encode()):
				return existing_user_list[0]
		return 'invalid email / password combination'

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class TripManager(models.Manager):
	def validateTrip(self, postData, user_id):
		errors = []
		user = User.objects.get(id = user_id)
		print(postData)
		if len(postData['description']) < 1:
			errors.append('Must have an entry')
		if len(postData['plan']) < 1:
			errors.append('Must have an entry for description!')
		if postData['start_date'] < str(datetime.datetime.now()):
			errors.append('Start date must be in the future')
		if postData['start_date'] > postData['end_date']:
			errors.append('End date must be after start date')
		if len(errors) == 0:
			Trip.objects.create(
				description = postData['description'],
				plan = postData['plan'],
				start_date = datetime.datetime.strptime(postData['start_date'], '%Y-%m-%d'),
				end_date = datetime.datetime.strptime(postData['end_date'], '%Y-%m-%d'),
				user = User.objects.get(id=user_id),
			).attendee.add(user)
		return errors


class Trip(models.Model):
	user = models.ForeignKey(User, related_name='trip_owner')
	description = models.CharField(max_length=255)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	plan = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	attendee = models.ManyToManyField(User, related_name="trips_attending")
	objects = TripManager()

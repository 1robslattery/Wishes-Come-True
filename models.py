from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
	def registerValidator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

		errors = {}
		if len(postData['fname']) < 1:
			errors['fname'] = "You must enter first name"
		if len(postData['lname']) < 1:
			errors['lname'] = "You must enter last name"
		if len(postData['email']) < 1:
			errors['email'] = "You must enter email"
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = ("Invalid email address!")
		else:
			emailtaken = User.objects.filter(email = postData['email'])
			if len(emailtaken) > 0:
				errors['emailtaken'] = "Email is already taken. Choose another email"
		if len(postData['password']) < 3:
			errors['password'] = "You must enter at least three characters"
		if postData['password'] != postData['confirm_password']:
			errors['passwordconfirm'] = "Password and confirm password must match"
		return errors

	def loginValidator(self, postData):
		errors = {}
		if len(postData['email']) < 1:
			errors['emaillength'] = "You must enter an email"
		userinDB = User.objects.filter(email = postData['email'])
		if len(userinDB) == 0:
			errors['emailnotregistered'] = "This email is not registered. Please register first."

		else:
			userinDB = userinDB[0]
			print(userinDB)
			if bcrypt.checkpw(postData['password'].encode(), userinDB.password.encode()):
				print("password match")
			else:
				print("failed password")
				errors['passwordwrong'] = "Incorrect password"
		print(errors)
		return errors

class wishManager(models.Manager):
	def wishValidator(self, postData):
		errors = {}
		if len(postData['item']) < 3:
			errors['item'] = "Wish must consist of at least 3 characters"
		if len(postData['desc']) < 1:
			errors['desc'] = "A description must be provided"
		if len(postData['desc']) < 3:
			errors['desclength'] = "A description must be at least 3 characters"
		return errors

class User(models.Model):
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Wish(models.Model):
	item = models.CharField(max_length=255)
	desc = models.TextField()
	is_granted = models.BooleanField(default = False)
	likes = models.ManyToManyField(User, related_name="items_liked")
	creator = models.ForeignKey(User, related_name="item_created", on_delete = models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = wishManager()
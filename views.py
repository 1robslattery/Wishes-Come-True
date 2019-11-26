from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def loginreg(request):
	return render(request, "loginreg.html")

def register(request):
	print(request.POST)
	errors = User.objects.registerValidator(request.POST)
	print(errors)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	passwordFromForm = request.POST['password']
	hashed_password = bcrypt.hashpw(passwordFromForm.encode(), bcrypt.gensalt())
	newuser = User.objects.create(firstname = request.POST['fname'], lastname = request.POST['lname'], email = request.POST['email'], password = hashed_password.decode())
	print(newuser)
	request.session['loggedinUserID'] = newuser.id
	return redirect("/success")

def login(request):
	print(request.POST)
	errors = User.objects.loginValidator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		loggedinuser = User.objects.filter(email = request.POST['email'])
		loggedinuser = loggedinuser[0]
		request.session['loggedinUserID'] = loggedinuser.id
		return redirect("/success")

def success(request):
	context = {
		"loggedinUser" : User.objects.get(id=request.session['loggedinUserID']),
		"all_ungranted_wishes" : Wish.objects.filter(is_granted = False),
		"all_granted_wishes" : Wish.objects.filter(is_granted = True)
	}
	return render(request, "wishes.html", context)

def addWish(request):
	context = {
		"loggedinUser" : User.objects.get(id=request.session['loggedinUserID'])
	}
	return render(request, "addWish.html", context)

def createWish(request):
	print(request.POST)
	loggedinUser = User.objects.get(id=request.session['loggedinUserID'])
	errors = Wish.objects.wishValidator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/addWish")
	newItem = Wish.objects.create(item = request.POST['item'], desc = request.POST['desc'], is_granted = False, creator = loggedinUser)
	print(newItem)
	return redirect("/success")

def removeitem(request, item_id):
	print(request.method)
	itemToRemove = Wish.objects.get(id = item_id)
	itemToRemove.delete()
	return redirect("/success")

def showEditPage(request, item_id):
	context = {
		"itemToEdit" : Wish.objects.get(id = item_id)
	}
	return render(request, "editItem.html", context)

def editItem(request, item_id):
	itemToEdit = Wish.objects.get(id = item_id)
	itemToEdit.item = request.POST['item']
	itemToEdit.desc = request.POST['desc']
	itemToEdit.save()
	return redirect("/success")

def logout(request):
	request.session.clear()
	return redirect("/")
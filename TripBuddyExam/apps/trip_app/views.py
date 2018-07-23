from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
	return render(request, 'trip_app/index.html')

def createUser(request):
	result = User.objects.validateRegistration(request.POST)
	print("in the views************")
	print(result)
	if type(result) is list:
		for error in result:
			messages.error(request, error)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
	return redirect('/travels')

def login(request):
	result = User.objects.validateLogin(request.POST)
	print("in the login************")
	print(result)
	if type(result) is str:
		messages.error(request, result)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

def travel(request):
	user = User.objects.get(id=request.session['user_id'])
	context = {
		'user' : user,
		'all_plans' : Trip.objects.exclude(attendee=user),
		'my_plans' : Trip.objects.filter(attendee=user),
	}
	return render(request, 'trip_app/travels.html', context)

def addTrip(request):
	return render(request, 'trip_app/add.html')

def createTrip(request):
	errors = Trip.objects.validateTrip(request.POST, request.session['user_id'])
	if len(errors) > 0:
		for error in errors:
			messages.error(request, error)
		return redirect('/addtrip')
	else:
		return redirect('/travels')

def view(request, description_id):
	context = {
		'trips' : Trip.objects.filter(id=description_id),
		'attendees': User.objects.filter(trips_attending = description_id)
	}
	return render(request, 'trip_app/view.html', context)

def join(request, id):
	me = User.objects.get(id = request.session['user_id'])
	trip = Trip.objects.get(id = id)
	trip.attendee.add(me)
	trip.save()
	return redirect('/travels')

def cancel(request, id):
	me = User.objects.get(id = request.session['user_id'])
	trip = Trip.objects.get(id = id)
	trip.attendee.remove(me)
	trip.save()
	return redirect('/travels')
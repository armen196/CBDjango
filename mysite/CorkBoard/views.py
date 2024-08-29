from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Users
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return HttpResponse("Welcome!")

def tm(request):
    return HttpResponse("You have reached temp")

@csrf_exempt
def verifyLogin(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = Users.objects.filter(username=username).first()
        if user:
            print("Exists")
            toReturn = {
                "code": 501,
                "message": "User exists"
            }
            return JsonResponse(toReturn)
        else:
            print("Does not exist")
            toReturn = {
                "code": 502,
                "message": "User does not exist"
            }
            return JsonResponse(toReturn)
    

@csrf_exempt
def addUser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        print(f"Username: {username}, Password: {password}")
        user = Users(username=username, password=password)
        user.save()
        print(f"Got user ${username} with password ${password}")
        return HttpResponse(f"User {username} added successfully!")
    else:
        return HttpResponse("Invalid request method.")
        
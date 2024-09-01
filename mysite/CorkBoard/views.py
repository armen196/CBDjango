from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Users
from django.views.decorators.csrf import csrf_exempt

import CorkBoard.codes as codes
import json

def home(request):
    return HttpResponse("Updated from my laptop!!")

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
                "code": codes.USER_EXISTS,
                "message": "User exists"
            }
            return JsonResponse(toReturn)
        else:
            print("Does not exist")
            toReturn = {
                "code": codes.USER_DOES_NOT_EXIST,
                "message": "User does not exist"
            }
            return JsonResponse(toReturn)
    

@csrf_exempt
def addUser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if (Users.objects.filter(username=username).first()):
            print(f"    Username {username} already taken")
            toReturn = {
                "code": codes.USERNAME_TAKEN,
                "message": "Username already taken"
            }
            return JsonResponse(toReturn)
        else:
            print(f"Registering username {username} with password {password}")
            user = Users(username=username, password=password)
            user.save()
            toReturn = {
                "code": codes.USERNAME_AVAILABLE,
                "message": "User added successfuly"
            }
            return JsonResponse(toReturn)
        
    else:
        return HttpResponse("Invalid request method.")
        
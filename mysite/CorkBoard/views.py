from ntpath import join
from pathlib import Path
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse
from .models import Users, Posts, PostsReplies, Lists, ListItem, Chore
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import os

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
                "firstName": user.firstName,
                "message": "User exists",
                "groupID": user.groupID
            }
            return JsonResponse(toReturn)
        else:
            print("Does not exist")
            toReturn = {
                "code": codes.USER_DOES_NOT_EXIST,
                "message": "User does not exist"
            }
            print("what")
            return JsonResponse(toReturn)
    
@csrf_exempt
def getGroupMembers(request):
    if request.method == "POST":
        data = json.loads(request.body)
        groupID = data.get('groupID')
        groupMembers = Users.objects.filter(groupID=groupID)
        
        return JsonResponse(list(groupMembers.values()), safe=False)
    
    


@csrf_exempt
def addUser(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        groupID = data.get('groupID')
        formData = request.FILES.get('image')
        print(formData)
        if (Users.objects.filter(username=username).first()):
            print(f"    Username {username} already taken")
            toReturn = {
                "code": codes.USERNAME_TAKEN,
                "message": "Username already taken"
            }
            return JsonResponse(toReturn)
        else:
            print(f"Registering user:   Username: {username}\n              Password: {password}\n              FirstName: {firstName}\n              LastName: {lastName}\n              GroupID: {groupID}")
            user = Users(username=username, password=password, firstName=firstName, lastName=lastName, groupID=groupID, image=formData)
            user.save()
            toReturn = {
                "code": codes.USERNAME_AVAILABLE,
                "message": "User added successfuly"
            }
            return JsonResponse(toReturn)
        
    else:
        return HttpResponse("Invalid request method.")

# class Users(models.Model):
#     username = models.CharField(max_length=25, null=False, blank=False)
#     password = models.CharField(max_length=15, null=False, blank=False)
#     firstName = models.CharField(max_length=25)
#     lastName = models.CharField(max_length=25)
#     groupID = models.CharField(max_length=10)
#     image = models.ImageField(upload_to='images/')

@csrf_exempt
def getUsers(request):
    if request.method == "POST":
        data = json.loads(request.body)
        groupID = data.get('groupID')
        toReturn = Users.objects.filter(groupID=groupID)
        if toReturn:
            print(f"Returning users for group {groupID}")
            return JsonResponse(list(toReturn.values('username', 'firstName', 'lastName', 'image')), safe=False)
        else:
            return HttpResponse(codes.NO_USERS)

@csrf_exempt   
def getPosts(request):
    if request.method == "POST":
        data = json.loads(request.body)
        groupID = data.get('groupID')
        if (Posts.objects.filter(groupID=groupID).count() > 0):
            print("    Replying with posts")
            posts = Posts.objects.filter(groupID=groupID)
            postsList = list(posts.values('groupID', 'postID','poster', 'post'))
            for item in postsList:
                print(item)
            return JsonResponse({'posts': postsList}, safe=False)
        else:
            print("    Found no posts... Replying with generic response")
            toReturn = {
                "posts" : [
                    {
                        "groupID": "null",
                        "postID": "null",
                        "poster": "No posts to show!",
                        "post": "Click the plus button in the top right to create your very first post!"
                    }
                ]
               
            }
            return JsonResponse(toReturn)

@csrf_exempt      
def getPostReplies(request):
    if request.method == "POST":
        data = json.loads(request.body)
        postID = data.get('postID')
        print(f"Replies requested: {postID}")
        replies = PostsReplies.objects.filter(postID=postID)
        if (replies):
            print("    Found reply")
            replyList = list(replies.values('postID', 'poster', 'post'))
            return JsonResponse({'comments': replyList}, safe=False)
        else:
            print(f"No comments for post with id {postID}, replying with generic response")
            toReturn = {
                "comments" : [
                    {
                        "postID": postID,
                        "poster": "No replies yet!",
                        "post": "Click on the reply button below to be the first to respond to this post"
                    }   
                ]
            }
            return JsonResponse(toReturn)
            #return HttpResponse("asdf")
        
@csrf_exempt      
def makePost(request):
    if request.method == "POST":
        data = json.loads(request.body)
        groupID = data.get('groupID')
        poster = data.get('poster')
        toPost = data.get('post')
        post = Posts.objects.create(groupID=groupID, poster=poster, post=toPost)
        post.postID = post.id
        post.save()
        print(f"groupID: {post.groupID}, Poster: {post.poster}, Post: {post.post}")
        return HttpResponse(post.id)
    
@csrf_exempt      
def makeReply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        postID = data.get('postID')
        poster = data.get('replier')
        post = data.get('post')
        post = PostsReplies.objects.create(postID=postID, poster=poster, post=post)
        post.save()
        print(f"        Recieved reply request: postID: {post.postID}, Poster: {post.poster}, Post: {post.post}")
        return HttpResponse(post.id)
    
@csrf_exempt
def makeList(request):
    if request.method == "POST":
        data = json.loads(request.body)
        listName = data.get('listName')
        groupID = data.get('groupID')
        list = Lists.objects.create(groupID=groupID, listName=listName)
        list.listID = list.id
        list.save()
        print(f"Making list {listName} for group {groupID} with listID {list.listID}")
        return HttpResponse(list.listID)

# name = models.CharField(max_length=255)
# quantity = models.IntegerField(default=1)
# bought = models.BooleanField(default=False)
# list = models.ForeignKey(Lists, related_name='items', on_delete=models.CASCADE)
@csrf_exempt
def makeItem(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get('item')
        quantity = data.get('quantity')
        bought = data.get('bought')
        listID = data.get('listID')
        parentList = Lists.objects.get(listID=listID)
        item = ListItem.objects.create(name=name, bought=False, list=parentList)
        item.save()
        print(f"Saving item {item} to list {parentList.listName}")
        return HttpResponse("Eureka")
        
@csrf_exempt
def getItems(request):
    if request.method == "POST":
        data = json.loads(request.body)
        listID = data.get('listID')
        parentList = Lists.objects.get(listID=listID)
        itemList = ListItem.objects.filter(list=parentList)
        if (itemList):
            print(f"Returning list for {parentList.listName}")
            return JsonResponse({'items': itemList}, safe=False)
        else: 
            
            
            return JsonResponse({'items': toReturn}, safe=False)
        
@csrf_exempt
def removeItem(request):
    if request.method == "POST":
        print()
        data = json.loads(request.body)
        print(data)
        itemID = data.get('id')
        itemToDelete = ListItem.objects.get(id=itemID)
        print(f"Removing item {itemToDelete.name}")
        itemToDelete.delete()
        return HttpResponse("Success")
    
@csrf_exempt
def markAsPurchased(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        itemID = data.get('id')
        itemToChange = ListItem.objects.get(id=itemID)
        print(f"Changing item {itemToChange.name} to purchased")
        itemToChange.bought = True
        itemToChange.save()
        return HttpResponse("Success")

@csrf_exempt
def changeName(request):
    if request.method == "POST":
        #print(f"Changing list {listToChange.listName} to {listName}")
        data = json.loads(request.body)
        listName = data.get('listName')
        toChange = data.get('toChange')
        listToChange = Lists.objects.get(listName=toChange)
        print(f"Changing list {listToChange.listName} to {listName}")
        listToChange.listName = listName
        listToChange.save()
        return HttpResponse("Changed list name")
    
@csrf_exempt
def deleteList(request):
    if request.method == "POST":
        #print(f"Changing list {listToChange.listName} to {listName}")
        data = json.loads(request.body)
        listName = data.get('listName')
        listToDelete = Lists.objects.get(listName=listName)
        print(f"Deleting list {listToDelete}")
        listToDelete.delete()
        return HttpResponse("List Deleted")
        
@csrf_exempt      
def getList(request):
    if request.method == "POST":
        data = json.loads(request.body)
        groupID = data.get('groupID')
        print(f"Lists requested group: {groupID}")
        lists = Lists.objects.all().filter(groupID=groupID)
        toReturn = []
        for li in lists:
            items = ListItem.objects.filter(list=li)
            item_list = [model_to_dict(item) for item in items]
            if (not item_list):
                item_list = [
                    {
                        "name": "No items yet!",
                        "quantity": "0",
                        "bought": False,
                        "items": "null"
                    }
                ]
                    
            
            data = {
                'name': li.listName,
                'listID': li.listID,
                'items': item_list
            }
            toReturn.append(data)
        return JsonResponse({'lists': toReturn}, safe=False)
    
@csrf_exempt
def getChores(request):
    if request.method == "POST":
        data = json.loads(request.body)
        groupID = data.get("groupID")
        chores = Chore.objects.filter(groupID=groupID).values()
        if chores:
            toReturn = list(chores)
            
            return JsonResponse(toReturn, safe=False)
        else: 
            return HttpResponse("No chores")
            
@csrf_exempt
def addChore(request):
    if request.method == "POST":
        data = json.loads(request.body)
        groupID = data.get("groupID")
        chore = data.get("chore")
        description = data.get("description")
        poster = Users.objects.get(username=data.get("userName"))
        print(f"groupID: {groupID}")
        if Chore.objects.filter(chore=chore):
            return HttpResponse(codes.CHORE_ALREADY_EXISTS)
        choreToAdd = Chore.objects.create(groupID=groupID, chore=chore, poster=poster, description=description)
        choreToAdd.save()
        print(f"Adding {chore} with description {description}")
        return HttpResponse(codes.CHORE_ADDED)
        
@csrf_exempt
def removeChore(request):
    if request.method == "POST":
        data = json.loads(request.body)
        choreToDelete = Chore.objects.filter(chore=data.get("chore"))
        choreToDelete.delete()
        
@csrf_exempt
def getImageFromId(request, id):
    if request.method == "GET":
        BASE_DIR = Path(__file__).resolve().parent.parent
        user = Users.objects.get(id=id);
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media/images/')
        return FileResponse(open(join(MEDIA_ROOT, user.username + ".jpg"), 'rb'), content_type='image/jpeg')
    else:
        return HttpResponse('Nope...')
    
@csrf_exempt
def markChoreAsCompleted(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data.get("choreID")
        completer = data.get("userName")
        chore = Chore.objects.get(id=id)
        completerID = Users.objects.get(username=completer)
        print(chore.chore)
        if chore.completed:
            chore.completer = None
        else:
            chore.completer = completerID
        chore.completed = not chore.completed
        chore.save()
        print(f"Saving chore {chore.chore} with new status {chore.completed} completer {chore.completer}")
        return HttpResponse("Successfully marked chore")
    else:
        return HttpResponse('Nope...')
    
@csrf_exempt
def getUsernameFromID(request, id):
    if request.method == "GET":
        user = Users.objects.get(id=id)
        return HttpResponse(user.username)
    

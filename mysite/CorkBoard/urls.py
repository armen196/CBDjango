from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("addUser/", views.addUser, name="addUser"),
    path("signIn/", views.verifyLogin, name="verifyLogin"),
    path("getPosts/", views.getPosts, name="getPosts"),
    path("getPostsReplies/", views.getPostReplies, name="getPostReplies"),
    path("makePost/", views.makePost, name="makePost"),
    path("makeReply/", views.makeReply, name="makeReply"),
    path("makeList/", views.makeList, name="makeList"),
    path("getList/", views.getList, name="getList"),
    path("makeItem/", views.makeItem, name="makeItem"),
    path("removeItem/", views.removeItem, name="removeItem"),
    path("markAsPurchased/", views.markAsPurchased, name="markAsPurchased"),
    path("changeName/", views.changeName, name="changeName"),
    path("deleteList/", views.deleteList, name="deleteList"),
    
]
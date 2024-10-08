from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

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
    path("getGroupMembers/", views.getGroupMembers, name="getGroupMembers"),
    path("getUsers/", views.getUsers, name="getUsers"),
    path("getChores/", views.getChores, name="getChores"),
    path("addChore/", views.addChore, name="addChore"),
    path("removeChore/", views.removeChore, name="removeChore"),
    path("getImageFromID/<int:id>", views.getImageFromId, name="getImageFromId"),
    path("markChoreAsCompleted/", views.markChoreAsCompleted, name="markChoreAsCompleted"),
    path("getUsernameFromID/<int:id>", views.getUsernameFromID, name="getUsernameFromID"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
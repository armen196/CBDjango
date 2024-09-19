import os
import django
import sys

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Set up Django
django.setup()

# Import the model after setting up Django
from CorkBoard.models import Users, Posts, PostsReplies, Lists, ListItem

# Function to print all users
def print_users():
    users = Users.objects.all()
    for user in users:
        print(f"User name: {user.username}, Password: {user.password}")

def delete_all_users():
    Users.objects.all().delete()
    
def delete_all_posts():
    Posts.objects.all().delete()
    PostsReplies.objects.all().delete()
    
def delete_all_lists():
    Lists.objects.all().delete()
    ListItem.objects.all().delete()

def delete_all():
    delete_all_lists()
    delete_all_posts()
    delete_all_users()

# Call the function
if __name__ == "__main__":
    if(sys.argv[1] == 'print_users'):
        print_users()
    if (sys.argv[1] == 'delete_all'):
        delete_all_users()
    if (sys.argv[1] == 'help'):
        print("Usage: \n    - print_users: Print all active users\n    - delete_all: Delete all existing users")
    if (sys.argv[1] == 'delete_posts'):
        delete_all_posts()
    if (sys.argv[1] == 'delete_lists'):
        delete_all_lists()
    if (sys.argv[1] == 'delete_all'):
        delete_all()

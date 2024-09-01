import os
import django
import sys

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Set up Django
django.setup()

# Import the model after setting up Django
from CorkBoard.models import Users

# Function to print all users
def print_users():
    users = Users.objects.all()
    for user in users:
        print(f"User name: {user.username}, Password: {user.password}")

def delete_all():
    Users.objects.all().delete()

# Call the function
if __name__ == "__main__":
    if(sys.argv[1] == 'print_users'):
        print_users()
    if (sys.argv[1] == 'delete_all'):
        delete_all()
    if (sys.argv[1] == 'help'):
        print("Usage: \n    - print_users: Print all active users\n    - delete_all: Delete all existing users")


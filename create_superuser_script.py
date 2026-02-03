
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    username = 'admin'
    password = 'admin'
    email = 'admin@example.com'
    
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists. Resetting password.")
        u = User.objects.get(username=username)
        u.set_password(password)
        u.is_superuser = True
        u.is_staff = True
        u.save()
    else:
        print(f"Creating user '{username}'.")
        User.objects.create_superuser(username, email, password)
    
    print(f"Superuser Ready -> Username: {username} | Password: {password}")

if __name__ == "__main__":
    create_admin()

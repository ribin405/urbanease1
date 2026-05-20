"""Account app models.

The project uses ``urbanease.User`` as its configured auth user model.
Keeping another concrete ``AbstractUser`` subclass here creates reverse
accessor clashes with Django's auth groups and permissions.
"""

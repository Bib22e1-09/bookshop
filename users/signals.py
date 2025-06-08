# signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db import connection
from users.models import CustomUser

@receiver(post_save, sender=CustomUser)
def create_db_user(sender, instance, created, **kwargs):
    if created:
        role = 'superadmin_role' if instance.is_superuser else 'customer_role'
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE USER {instance.username} IN ROLE {role};")

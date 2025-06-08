# users/management/commands/sync_db_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import connection
import psycopg2

class Command(BaseCommand):
    help = 'Синхронизация пользователей и групп Django с PostgreSQL'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                # Создать PostgreSQL роли на основе Django групп
                for group in Group.objects.all():
                    role_name = f"{group.name}_role"
                    cursor.execute(
                        "SELECT 1 FROM pg_roles WHERE rolname = %s", 
                        [role_name]
                    )
                    if not cursor.fetchone():
                        cursor.execute(
                            f'CREATE ROLE "{role_name}"'
                        )
                        self.stdout.write(f'Создана роль: {role_name}')
                
                # Назначить пользователей в роли
                for user in User.objects.all():
                    # Проверить существование пользователя в PostgreSQL
                    cursor.execute(
                        "SELECT 1 FROM pg_roles WHERE rolname = %s", 
                        [user.username]
                    )
                    if not cursor.fetchone():
                        cursor.execute(
                            f'CREATE USER "{user.username}"'
                        )
                        self.stdout.write(f'Создан пользователь: {user.username}')
                    
                    # Назначить роли
                    for group in user.groups.all():
                        role_name = f"{group.name}_role"
                        cursor.execute(
                            f'GRANT "{role_name}" TO "{user.username}"'
                        )
                        self.stdout.write(f'Роль {role_name} назначена {user.username}')
                
            except psycopg2.Error as e:
                self.stderr.write(f'Ошибка PostgreSQL: {e}')
            except Exception as e:
                self.stderr.write(f'Ошибка: {e}')

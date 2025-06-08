# middleware.py
import psycopg2
from django.conf import settings

class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        if request.user.is_authenticated:
            db_config = settings.DATABASES['default']
            conn_params = {
                'dbname': db_config['NAME'],
                'user': db_config['USER'],  # Используйте основного пользователя БД
                'password': db_config['PASSWORD'],
                'host': db_config['HOST'],
                'port': db_config['PORT'],
            }
            with psycopg2.connect(**conn_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SET app.user_id = %s;", [str(request.user.id)])
                    if request.user.role == 'superadmin':
                        cursor.execute("SET ROLE superadmin_role;")
                    elif request.user.role == 'admin':
                        cursor.execute("SET ROLE admin_role;")
                    else:
                        cursor.execute("SET ROLE customer_role;")
        return self.get_response(request)


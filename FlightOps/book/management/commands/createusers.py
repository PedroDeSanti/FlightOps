from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



def create_user(username, email, password, permissions):
    # Create user and save to the database
    user = User.objects.create_user(username, email, password)
    for permission in permissions:
        user.user_permissions.add(permission)
    user.save()
    return

def create_permission(name, codename):
    content_type = ContentType.objects.get(app_label='auth', model='user')
    permission = Permission.objects.create(name=name, codename=codename, content_type=content_type)
    permission.save()
    return permission


class Command(BaseCommand):
    help = 'Create user'

    def handle(self, *args, **kwargs):
        permission_1 = create_permission("Administrar voos", "administrarvoo")
        permission_2 = create_permission("Monitorar voos", "monitorarvoo")
        permission_3 = create_permission("Gerar relatorios", "gerarrelatorio")
        
        create_user("usuario_1", "usuario1@flightops.com", "senha_1", [permission_1])
        create_user("usuario_2", "usuario2@flightops.com", "senha_2", [permission_2])
        create_user("usuario_3", "usuario3@flightops.com", "senha_3", [permission_3])
        create_user("dev", "dev@flightops.com", "senha", [permission_1, permission_2, permission_3])
        return 
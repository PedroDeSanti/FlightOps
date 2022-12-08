from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



def create_user(username, email, password, permissions):
    # Create user and save to the database
    user, created = User.objects.get_or_create(username=username, email=email)
    if created:
        user.set_password(password)
        for permission in permissions:
            user.user_permissions.add(permission)
        user.save()
    return

def create_permission(name, codename):
    content_type = ContentType.objects.get(app_label='auth', model='user')
    permission, created = Permission.objects.get_or_create(name=name, codename=codename, content_type=content_type)
    permission.save()
    return permission


class Command(BaseCommand):
    help = 'Create user'

    def handle(self, *args, **kwargs):
        permission_1 = create_permission("Administrar voos", "administrarvoo")
        permission_2 = create_permission("Monitorar voos", "monitorarvoo")
        permission_2_1 = create_permission("Funcionarios companhias aereas", "funcionario")
        permission_2_2 = create_permission("Piloto", "piloto")
        permission_2_3 = create_permission("Torre de controle", "torre")
        permission_3 = create_permission("Gerar relatorios", "gerarrelatorio")
        
        create_user("operador", "usuario1@flightops.com", "1234", [permission_1])
        create_user("funcionario", "usuario21@flightops.com", "1234", [permission_2, permission_2_1])
        create_user("piloto", "usuario22@flightops.com", "1234", [permission_2, permission_2_2])
        create_user("torre", "usuario23@flightops.com", "1234", [permission_2, permission_2_3])
        create_user("gerente", "usuario3@flightops.com", "gerente", [permission_3])
        create_user("dev", "dev@flightops.com", "dev", [permission_1, permission_2, permission_2_1, permission_2_2, permission_2_3, permission_3])
        return 
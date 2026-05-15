from django.db import migrations
import os


def create_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASSWORD')
    if not email or not password:
        # Nothing to do if creds not provided
        return

    full_name = os.environ.get('ADMIN_FULL_NAME', 'Super Admin')
    role = os.environ.get('ADMIN_ROLE', 'super_admin')

    user, created = User.objects.get_or_create(email=email, defaults={
        'full_name': full_name,
        'role': role,
        'is_staff': True,
        'is_superuser': True,
        'is_approved': True,
    })

    if not created:
        user.full_name = full_name
        user.role = role
        user.is_staff = True
        user.is_superuser = True
        user.is_approved = True

    user.set_password(password)
    user.save()


def remove_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    email = os.environ.get('ADMIN_EMAIL')
    if not email:
        return
    try:
        user = User.objects.get(email=email)
        user.delete()
    except User.DoesNotExist:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0006_populate_existing_users_approved'),
    ]

    operations = [
        migrations.RunPython(create_admin, remove_admin),
    ]

from django.db import migrations
import os
from django.contrib.auth.hashers import make_password


def promote_admin(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASSWORD')
    if not email:
        return

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return

    full_name = os.environ.get('ADMIN_FULL_NAME', '')
    if full_name:
        parts = full_name.split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ''

    user.role = os.environ.get('ADMIN_ROLE', 'super_admin')
    user.is_staff = True
    user.is_superuser = True
    user.is_approved = True

    if password:
        user.password = make_password(password)

    user.save()


def reverse_promote(apps, schema_editor):
    # Do not reverse destructive promotion automatically.
    return


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0007_create_admin_from_env'),
    ]

    operations = [
        migrations.RunPython(promote_admin, reverse_promote),
    ]

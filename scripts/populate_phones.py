import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings.development')
import django
django.setup()
from apps.accounts.models import User

for idx, u in enumerate(User.objects.order_by('id').all(), start=1):
    if not u.phone:
        u.phone = f'+1-555-01{str(idx).zfill(2)}'
        u.save()
        print('Updated', u.id, u.email, u.phone)
    else:
        print('Skipped', u.id, u.email, u.phone)

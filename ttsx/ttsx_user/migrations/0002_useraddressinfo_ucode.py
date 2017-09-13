# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ttsx_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddressinfo',
            name='ucode',
            field=models.CharField(null=True, max_length=30),
        ),
    ]

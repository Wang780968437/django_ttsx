# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddressInfo',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('uname', models.CharField(max_length=20)),
                ('uaddress', models.CharField(max_length=100)),
                ('uphone', models.CharField(max_length=11)),
=======
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('uname', models.CharField(max_length=20)),
                ('uaddress', models.CharField(max_length=100)),
                ('uphone', models.CharField(max_length=11)),

>>>>>>> dev
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
=======
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
>>>>>>> dev
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('uemail', models.CharField(max_length=30)),
                ('isValid', models.BooleanField(default=True)),
                ('isActive', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='useraddressinfo',
            name='user',
            field=models.ForeignKey(to='ttsx_user.UserInfo'),
        ),
    ]

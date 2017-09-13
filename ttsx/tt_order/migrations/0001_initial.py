# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
<<<<<<< HEAD
        ('ttsx_user', '0001_initial'),
        ('tt_goods', '0001_initial'),
=======
>>>>>>> dev
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetailInfo',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='tt_goods.GoodsInfo')),
=======
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('count', models.IntegerField()),
>>>>>>> dev
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
<<<<<<< HEAD
                ('oid', models.CharField(serialize=False, max_length=20, primary_key=True)),
=======
                ('oid', models.CharField(primary_key=True, serialize=False, max_length=20)),
>>>>>>> dev
                ('odate', models.DateTimeField(auto_now_add=True)),
                ('oIsPay', models.BooleanField(default=False)),
                ('ototal', models.DecimalField(decimal_places=2, max_digits=6)),
                ('oaddress', models.CharField(max_length=150)),
<<<<<<< HEAD
                ('user', models.ForeignKey(to='ttsx_user.UserInfo')),
=======
>>>>>>> dev
            ],
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order',
            field=models.ForeignKey(to='tt_order.OrderInfo'),
        ),
    ]

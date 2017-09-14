# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetailInfo',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
=======
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
>>>>>>> xia
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
<<<<<<< HEAD
                ('oid', models.CharField(primary_key=True, serialize=False, max_length=20)),
=======
                ('oid', models.CharField(primary_key=True, max_length=20, serialize=False)),
>>>>>>> xia
                ('odate', models.DateTimeField(auto_now_add=True)),
                ('oIsPay', models.BooleanField(default=False)),
                ('ototal', models.DecimalField(decimal_places=2, max_digits=6)),
                ('oaddress', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='orderdetailinfo',
            name='order',
            field=models.ForeignKey(to='tt_order.OrderInfo'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[


                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),


                ('gtitle', models.CharField(max_length=20)),
                ('gpic', models.ImageField(upload_to='goods')),
                ('gprice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('isDelete', models.BooleanField(default=False)),
                ('gunit', models.CharField(default='500g', max_length=20)),
                ('gclick', models.IntegerField()),
                ('gjianjie', models.CharField(max_length=200)),
                ('gkucun', models.IntegerField()),
                ('gcontent', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[


                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),

                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),

                ('ttitle', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gtype',
            field=models.ForeignKey(to='tt_goods.TypeInfo'),
        ),
    ]

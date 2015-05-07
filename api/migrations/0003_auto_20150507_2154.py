# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_game_game_over'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='engine_colour',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='game_depth',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
    ]

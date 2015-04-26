# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('player_elo', models.IntegerField(default=-1)),
                ('exit_reason', models.IntegerField(default=-1)),
                ('plies_moved', models.IntegerField(default=0)),
                ('engine_scores', models.TextField()),
            ],
        ),
    ]

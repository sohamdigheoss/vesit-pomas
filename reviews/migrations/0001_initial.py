# Generated by Django 2.1.7 on 2019-03-11 14:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_no', models.IntegerField()),
                ('marks', models.IntegerField()),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='auth.Group')),
            ],
        ),
    ]

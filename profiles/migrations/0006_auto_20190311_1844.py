# Generated by Django 2.1.7 on 2019-03-11 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_groupdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupdata',
            name='domain',
        ),
        migrations.AddField(
            model_name='groupdata',
            name='domain',
            field=models.ManyToManyField(to='profiles.Domain'),
        ),
    ]

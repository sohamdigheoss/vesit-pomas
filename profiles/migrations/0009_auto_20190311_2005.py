# Generated by Django 2.1.7 on 2019-03-11 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_remove_groupdata_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupdata',
            name='domain',
            field=models.ManyToManyField(related_name='primary_domain', to='profiles.Domain'),
        ),
    ]

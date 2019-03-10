# Generated by Django 2.1.7 on 2019-03-10 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('projects', '0003_auto_20190309_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectgroup',
            name='group_id',
        ),
        migrations.RemoveField(
            model_name='projectgroup',
            name='project_id',
        ),
        migrations.AddField(
            model_name='project',
            name='group_id',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='auth.Group'),
        ),
        migrations.DeleteModel(
            name='ProjectGroup',
        ),
    ]

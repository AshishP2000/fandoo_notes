# Generated by Django 4.1.5 on 2023-01-30 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notes',
            old_name='user_id',
            new_name='user',
        ),
    ]

# Generated by Django 4.1.5 on 2023-01-31 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0003_notes_collaborator_notes_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='color',
            field=models.TextField(),
        ),
    ]

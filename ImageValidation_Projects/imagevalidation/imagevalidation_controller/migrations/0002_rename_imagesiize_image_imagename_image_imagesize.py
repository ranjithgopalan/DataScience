# Generated by Django 5.0.1 on 2024-01-26 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imagevalidation_controller', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='imageSiize',
            new_name='imagename',
        ),
        migrations.AddField(
            model_name='image',
            name='imagesize',
            field=models.IntegerField(default=0),
        ),
    ]

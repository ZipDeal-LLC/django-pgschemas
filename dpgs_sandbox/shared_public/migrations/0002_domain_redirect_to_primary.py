# Generated by Django 3.2.4 on 2021-10-27 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_public', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='redirect_to_primary',
            field=models.BooleanField(default=False),
        ),
    ]

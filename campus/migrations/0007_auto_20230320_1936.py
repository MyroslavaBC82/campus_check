# Generated by Django 2.1.5 on 2023-03-20 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus', '0006_studentprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.SlugField(default='gvbh_vhbj'),
        ),
        migrations.AddField(
            model_name='university',
            name='slug',
            field=models.SlugField(default='gvbh_vhbj'),
        ),
    ]

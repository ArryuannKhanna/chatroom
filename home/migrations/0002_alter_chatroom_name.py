# Generated by Django 4.2.10 on 2024-02-12 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

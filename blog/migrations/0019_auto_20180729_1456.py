# Generated by Django 2.0.7 on 2018-07-29 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20180729_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(default='Untitled', max_length=255),
        ),
    ]

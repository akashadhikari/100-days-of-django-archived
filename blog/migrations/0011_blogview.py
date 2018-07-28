# Generated by Django 2.0.7 on 2018-07-27 16:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_blog_code_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=40)),
                ('session', models.CharField(max_length=40)),
                ('created', models.DateTimeField(default=datetime.datetime(2018, 7, 27, 21, 55, 52, 563582))),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_views', to='blog.Blog')),
            ],
        ),
    ]
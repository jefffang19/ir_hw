# Generated by Django 3.1.1 on 2020-10-05 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_engine', '0004_auto_20200929_0245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='articleId',
        ),
        migrations.RemoveField(
            model_name='article',
            name='label',
        ),
        migrations.AddField(
            model_name='article',
            name='title',
            field=models.CharField(default='none', max_length=200),
            preserve_default=False,
        ),
    ]

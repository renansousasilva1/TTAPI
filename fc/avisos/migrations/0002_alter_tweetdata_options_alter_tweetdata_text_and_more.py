# Generated by Django 4.2.17 on 2025-02-28 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweetdata',
            options={},
        ),
        migrations.AlterField(
            model_name='tweetdata',
            name='text',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='tweetdata',
            name='timestamp',
            field=models.CharField(max_length=255),
        ),
    ]

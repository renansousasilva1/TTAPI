# Generated by Django 4.2.17 on 2025-02-28 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0002_alter_tweetdata_options_alter_tweetdata_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetdata',
            name='text',
            field=models.JSONField(),
        ),
    ]

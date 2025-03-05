# Generated by Django 4.2.17 on 2025-02-28 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0003_alter_tweetdata_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetdata',
            name='likes',
            field=models.IntegerField(blank=True, default=0, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tweetdata',
            name='replies',
            field=models.IntegerField(blank=True, default=0, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tweetdata',
            name='retweeted_by',
            field=models.CharField(blank=True, default=0, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='tweetdata',
            name='retweets',
            field=models.IntegerField(blank=True, default=0, max_length=255, null=True),
        ),
    ]

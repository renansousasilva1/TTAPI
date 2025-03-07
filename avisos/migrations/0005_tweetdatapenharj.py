# Generated by Django 4.2.17 on 2025-02-28 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avisos', '0004_alter_tweetdata_likes_alter_tweetdata_replies_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TweetDataPenhaRJ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('timestamp', models.CharField(max_length=255)),
                ('text', models.JSONField()),
                ('retweeted_by', models.CharField(blank=True, default=0, max_length=255, null=True)),
                ('replies', models.IntegerField(blank=True, default=0, null=True)),
                ('retweets', models.IntegerField(blank=True, default=0, null=True)),
                ('likes', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]

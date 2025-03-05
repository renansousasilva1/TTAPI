from django.db import models

class TweetData(models.Model):
    author = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)  # Agora é CharField
    text = models.JSONField()  # Usando JSONField para armazenar dados JSON
    retweeted_by = models.CharField(max_length=255, default=0, blank=True, null=True)
    replies = models.IntegerField(max_length=255, default=0, blank=True, null=True)
    retweets = models.IntegerField(max_length=255, default=0, blank=True, null=True)
    likes = models.IntegerField(max_length=255, default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.timestamp}"


class TweetDataPenhaRJ(models.Model):
    author = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)  # Pode ser datetime, se preferir
    text = models.JSONField()  # Usando JSONField para armazenar dados JSON
    retweeted_by = models.CharField(max_length=255, default=0, blank=True, null=True)
    replies = models.IntegerField(default=0, blank=True, null=True)
    retweets = models.IntegerField(default=0, blank=True, null=True)
    likes = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.timestamp}"
    


class TweetDataPonteRJ(models.Model):
    author = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)  # Pode ser datetime, se preferir
    text = models.JSONField()  # Usando JSONField para armazenar dados JSON
    retweeted_by = models.CharField(max_length=255, default=0, blank=True, null=True)
    replies = models.IntegerField(default=0, blank=True, null=True)
    retweets = models.IntegerField(default=0, blank=True, null=True)
    likes = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.timestamp}"


class TweetDataCOR(models.Model):
    author = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)  # Pode ser datetime, se preferir
    text = models.JSONField()  # Usando JSONField para armazenar dados JSON
    retweeted_by = models.CharField(max_length=255, default=0, blank=True, null=True)
    replies = models.IntegerField(default=0, blank=True, null=True)
    retweets = models.IntegerField(default=0, blank=True, null=True)
    likes = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.timestamp}"
    


class TweetDataVOZ(models.Model):
    author = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)  # Pode ser datetime, se preferir
    text = models.JSONField()  # Usando JSONField para armazenar dados JSON
    retweeted_by = models.CharField(max_length=255, default=0, blank=True, null=True)
    replies = models.IntegerField(default=0, blank=True, null=True)
    retweets = models.IntegerField(default=0, blank=True, null=True)
    likes = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.timestamp}"




class TweetDataTREM(models.Model):
    author = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)  # Pode ser datetime, se preferir
    text = models.JSONField()  # Usando JSONField para armazenar dados JSON
    retweeted_by = models.CharField(max_length=255, default=0, blank=True, null=True)
    replies = models.IntegerField(default=0, blank=True, null=True)
    retweets = models.IntegerField(default=0, blank=True, null=True)
    likes = models.IntegerField(max_length=255, default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.timestamp}"


class TweetDataPMERJ(models.Model):
    author = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)  # Pode ser datetime, se preferir
    text = models.JSONField()  # Usando JSONField para armazenar dados JSON
    retweeted_by = models.CharField(max_length=255, default=0, blank=True, null=True)
    replies = models.IntegerField(default=0, blank=True, null=True)
    retweets = models.IntegerField(default=0, blank=True, null=True)
    likes = models.IntegerField(max_length=255, default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.timestamp}"



class TweetDataCAZETV(models.Model):
    author = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)  # Pode ser datetime, se preferir
    text = models.JSONField()  # Usando JSONField para armazenar dados JSON
    retweeted_by = models.CharField(max_length=255, default=0, blank=True, null=True)
    replies = models.IntegerField(default=0, blank=True, null=True)
    retweets = models.IntegerField(default=0, blank=True, null=True)
    likes = models.IntegerField(max_length=255, default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.timestamp}"



















































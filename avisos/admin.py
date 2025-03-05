from django.contrib import admin
from .models import TweetData, TweetDataPenhaRJ, TweetDataPonteRJ, TweetDataVOZ

# Admin para o modelo TweetData
@admin.register(TweetData)
class TweetDataAdmin(admin.ModelAdmin):
    list_display = ('author', 'username', 'timestamp', 'retweets', 'likes', 'replies', 'retweeted_by')
    search_fields = ('author', 'username')
    list_filter = ('timestamp',)

# Admin para o novo modelo TweetDataPenhaRJ
@admin.register(TweetDataPenhaRJ)
class TweetDataPenhaRJAdmin(admin.ModelAdmin):
    list_display = ('author', 'username', 'timestamp', 'retweets', 'likes', 'replies', 'retweeted_by')
    search_fields = ('author', 'username')
    list_filter = ('timestamp',)


@admin.register(TweetDataPonteRJ)
class TweetDataPonteRJAdmin(admin.ModelAdmin):
    list_display = ('author', 'username', 'timestamp', 'retweets', 'likes', 'replies', 'retweeted_by')
    search_fields = ('author', 'username')
    list_filter = ('timestamp',)


@admin.register(TweetDataVOZ)
class TweetDataVOZAdmin(admin.ModelAdmin):
    list_display = ('author', 'username', 'timestamp', 'retweets', 'likes', 'replies', 'retweeted_by')
    search_fields = ('author', 'username')
    list_filter = ('timestamp',)
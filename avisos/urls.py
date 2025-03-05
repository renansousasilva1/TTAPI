from django.urls import path
from .views import (
    ProcessNitterView, ProcessNitterViewPenhaRJ, ProcessNitterViewPonteRJ, ProcessNitterViewCOR, ProcessNitterViewVOZ, ProcessNitterViewTremRJ, ProcessNitterViewPMERJ,  ProcessNitterViewCAZETV,
    listar_tweets, listar_tweets_penharj, listar_tweets_ponterj, listar_tweets_COR, listar_tweets_VOZ, listar_tweets_TREM, listar_tweets_PMERJ, listar_tweets_cazetv,
)

urlpatterns = [
    path('capture-screenshot/', ProcessNitterView.as_view(), name='capture-screenshot'),

    path('capture-screenshot-cazetv/', ProcessNitterViewCAZETV.as_view(), name='capture-screenshot-cazetv'),  # Nova UR


    path('capture-screenshot-tremrj/', ProcessNitterViewTremRJ.as_view(), name='capture-screenshot-tremrj'),  # Nova URL

    path('capture-screenshot-penharj/', ProcessNitterViewPenhaRJ.as_view(), name='capture-screenshot-penharj'),  # Nova URL

    path('capture-screenshot-ponterj/', ProcessNitterViewPonteRJ.as_view(), name='capture-screenshot-ponterj'),  # Nova URL

    path('capture-screenshot-cor/', ProcessNitterViewCOR.as_view(), name='capture-screenshot-cor'),  # Nova URL

    path('capture-screenshot-voz/', ProcessNitterViewVOZ.as_view(), name='capture-screenshot-voz'),  # Nova URL


    path('capture-screenshot-pmerj/', ProcessNitterViewPMERJ.as_view(), name='capture-screenshot-pmerj'),  # Nova URL






    # URLs para exibir os tweets salvos
    path('listar-tweets/', listar_tweets, name='listar-tweets'),
    path('listar-tweets-cazetv/', listar_tweets_cazetv, name='listar-tweets_cazetv'),
    path('listar-tweets-pmerj/', listar_tweets_PMERJ, name='listar-tweets-pmerj'),
    path('listar-tweets-trem/', listar_tweets_TREM, name='listar-tweets-trem'),
    path('listar-tweets-voz/', listar_tweets_VOZ, name='listar-tweets-voz'),
    path('listar-tweets-cor/', listar_tweets_COR, name='listar-tweets'),
    path('listar-tweets-penharj/', listar_tweets_penharj, name='listar-tweets-penharj'),
    path('listar-tweets-ponterj/', listar_tweets_ponterj, name='listar-tweets-ponterj'),
]

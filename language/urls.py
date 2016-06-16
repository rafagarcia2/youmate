from django.conf.urls import url

from language import views

urlpatterns = [
    url(regex=r'^$',
        view=views.LanguageList.as_view(),
        name='language_list'),
]

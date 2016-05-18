from django.conf.urls import patterns, url

from language import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.LanguageList.as_view(),
        name='language_list'),
)

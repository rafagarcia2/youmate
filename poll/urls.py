from django.conf.urls import patterns, url

from poll import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.PollList.as_view(),
        name='poll_list'),
    url(regex=r'^create/$',
        view=views.PollCreateView.as_view(),
        name='poll_create'),
    url(regex=r'^(?P<pk>[0-9]+)/$',
        view=views.PollDetailView.as_view(),
        name='poll_detail'),
    url(regex=r'^(?P<pk>[0-9]+)/update/$',
        view=views.PollUpdateView.as_view(),
        name='poll_update'),
    url(regex=r'^(?P<poll__pk>[0-9]+)/answers/$',
        view=views.AnswerList.as_view(),
        name='poll_answer_list'),
    url(regex=r'^(?P<poll__pk>[0-9]+)/answers/create/$',
        view=views.AnswerCreateView.as_view(),
        name='poll_answer_create'),
    url(regex=r'^(?P<poll__pk>[0-9]+)/answers/(?P<pk>[0-9]+)/$',
        view=views.AnswerUpdateView.as_view(),
        name='poll_answer_detail'),
    url(regex=r'^(?P<poll__pk>[0-9]+)/answers/(?P<pk>[0-9]+)/like/$',
        view=views.AnswerLikeView.as_view(),
        name='poll_answer_like'),
    url(regex=r'^(?P<poll__pk>[0-9]+)/answers/(?P<pk>[0-9]+)/deslike/$',
        view=views.AnswerDeslikeView.as_view(),
        name='poll_answer_deslike'),
)

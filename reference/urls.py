from django.conf.urls import url

from reference import views

urlpatterns = [
    url(regex=r'^$',
        view=views.ReferenceList.as_view(),
        name='reference_list'),
    url(regex=r'^(?P<pk>[0-9]+)/$',
        view=views.ReferenceUpdateView.as_view(),
        name='reference_detail'),
]

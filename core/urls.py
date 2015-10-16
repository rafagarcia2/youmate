from django.conf.urls import patterns, url

from vanilla import views


class IndexView(views.TemplateView):
    template_name = 'index.html'


urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=IndexView.as_view(),
        name='index'),
)

from django.conf.urls import patterns, url

from core import views

urlpatterns = patterns(
    '',
    url(regex=r'^$',
        view=views.IndexView.as_view(),
        name='index'),
    url(regex=r'^confirmation/email/(?P<email_code>[\w-]+)/$',
        view=views.ConfirmationEmail.as_view(),
        name='confirmation_email'),
    url(regex=r'^profile/(?P<username>[\w-]+)/$',
        view=views.ProfileView.as_view(),
        name='profile'),
    url(regex=r'^profile/$',
        view=views.ProfileView.as_view(),
        name='profile'),
    url(regex=r'^update/about/profile/$',
        view=views.UpdateProfileAboutView.as_view(),
        name='update_profile_about_me'),
    url(regex=r'^validate/phone/profile/$',
        view=views.ValidatePhoneView.as_view(),
        name='validate_phone'),
    url(regex=r'^search/profile/$',
        view=views.SearchProfileView.as_view(),
        name='search_profile'),
)

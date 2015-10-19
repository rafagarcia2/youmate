from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy

from vanilla import TemplateView, UpdateView, DetailView

from core.forms import UpdateUserForm
from core.models import Profile


class IndexView(TemplateView):
    template_name = 'index.html'


class ProfileView(DetailView):
    model = Profile
    template_name = 'account/profile.html'

    def get_object(self):
        return self.request.user.profile

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)


class UpdateProfileView(UpdateView):
    model = Profile
    template_name = 'account/update_profile.html'
    form_class = UpdateUserForm
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user.profile

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateProfileView, self).dispatch(*args, **kwargs)

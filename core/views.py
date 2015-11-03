from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db.models import F

from vanilla import TemplateView, UpdateView, DetailView, ListView

from core.forms import UpdateUserForm
from core.models import Profile, SearchQuery


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


class SearchProfileView(ListView):
    model = Profile
    template_name = 'account/profile/search.html'

    def get_queryset(self):
        queryset = super(SearchProfileView, self).get_queryset()
        living_city = self.request.GET.get('living_city').lower()
        start = self.request.GET.get('start')
        end = self.request.GET.get('end')

        if not living_city:
            return queryset

        if self.request.user:
            instance, created = SearchQuery.objects.get_or_create(
                profile=self.request.user.profile,
                living_city=living_city,
                start=start or None,
                end=end or None
            )
            if not created:
                instance.count = F('count') + 1
                instance.save()

        return queryset.filter(
            living_city__icontains=living_city
        )

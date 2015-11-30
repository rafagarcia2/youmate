from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from vanilla import CreateView, ListView

from mate.forms import BecomeMatesForm
from mate.models import Mate
from core.models import Profile


class BecomeMatesView(CreateView):
    model = Mate
    template_name = 'account/profile.html'
    lookup_field = 'user__username'

    def get_form(self, data=None, files=None, **kwargs):
        initial = dict(
            from_user=self.request.user.profile.id,
            to_user=data and data.get('to_user')
        )
        return BecomeMatesForm(initial, files, **kwargs)

    def get_success_url(self):
        username = self.object.to_user.user.username
        return reverse_lazy('profile', kwargs={'username': username})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BecomeMatesView, self).dispatch(*args, **kwargs)


class MatesView(ListView):
    model = Mate
    template_name = 'account/profile/mates.html'
    paginate_by = 8

    def get_object(self):
        username = self.kwargs.get('username')

        if not username and self.request.user.is_authenticated():
            return self.request.user.profile
        else:
            return get_object_or_404(Profile, user__username=username)

    def get_context_data(self, **kwargs):
        context = super(MatesView, self).get_context_data(**kwargs)
        context.update(
            search=self.request.GET.get('search', None),
            object=self.get_object()
        )
        return context

    def get_queryset(self):
        queryset = super(MatesView, self).get_queryset()
        search = self.request.GET.get('search', None)
        queryset = queryset.filter(to_user=self.get_object())
        if not search:
            return queryset

        return queryset.filter(
            Q(from_user__user__first_name__icontains=search) |
            Q(from_user__user__username__icontains=search) |
            Q(from_user__living_city__icontains=search) |
            Q(from_user__born_city__icontains=search)
        )

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MatesView, self).dispatch(*args, **kwargs)

from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from vanilla import CreateView

from core.models import Profile
from reference.forms import ReferenceForm
from reference.models import Reference


class ReferenceCreateView(CreateView):
    model = Reference
    template_name = 'account/profile.html'

    def get_form(self, data=None, files=None, **kwargs):
        initial = dict(
            from_user=self.request.user.profile.id,
            to_user=data and data.get('to_user'),
            text=data and data.get('text'),
            rating=data and data.get('rating', 1),
        )
        return ReferenceForm(initial, files, **kwargs)

    def form_invalid(self, form):
        profile_id = self.request.POST.get('to_user')
        profile = get_object_or_404(Profile, id=profile_id)
        return redirect('profile', username=profile.user.username)

    def get_success_url(self):
        username = self.object.to_user.user.username
        return reverse('profile', kwargs={'username': username})

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReferenceCreateView, self).dispatch(*args, **kwargs)


class ReferenceActiveView(View):
    def get(self, request, id=None):
        self.object = get_object_or_404(Reference, id=id)
        profile = self.object.to_user

        if profile != request.user.profile:
            return redirect('profile')

        profile.references_to.update(active=False)
        self.object.active = True
        self.object.save()
        return redirect('profile')

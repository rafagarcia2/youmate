from django.shortcuts import redirect, get_list_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from vanilla import DetailView

from interest.forms import ProfileInterestForm
from core.models import Profile
from interest.models import Interest


class UpdateProfileInterestsViews(DetailView):
    model = Profile
    template_name = 'account/profile/interests.html'

    def get_context_data(self, **kwargs):
        context = super(
            UpdateProfileInterestsViews, self).get_context_data(**kwargs)
        context.update(profile_interestform_form=ProfileInterestForm())
        context.update(interests=Interest.objects.all())
        return context

    def get_object(self):
        return self.request.user.profile

    def post(self, *args, **kwargs):
        interests_ids = self.request.POST.getlist('interests')
        try:
            interests = get_list_or_404(Interest, id__in=interests_ids[:4])
        except:
            if not interests_ids:
                self.request.user.profile.interests.clear()
        else:
            self.request.user.profile.interests.clear()
            self.request.user.profile.interests.add(*interests)
        return redirect('profile_interests')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(
            UpdateProfileInterestsViews, self).dispatch(*args, **kwargs)

from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


from vanilla import CreateView

from mate.forms import BecomeMatesForm
from mate.models import Mate


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

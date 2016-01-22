from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import F

from vanilla import TemplateView, UpdateView, DetailView, ListView
from rest_framework.views import APIView
from rest_framework.response import Response

from core.forms import UpdateProfileAboutForm, ValidatePhoneForm
from reference.forms import ReferenceForm
from core.models import Profile, SearchQuery, code_generate


class IndexView(TemplateView):
    template_name = 'index.html'


class ProfileView(DetailView):
    model = Profile
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update(reference_form=ReferenceForm())
        context.update(
            update_profile_about_form=UpdateProfileAboutForm(
                instance=self.get_object()))
        return context

    def get_object(self):
        queryset = self.get_queryset()
        username = self.kwargs.get('username')

        if not username and self.request.user.is_authenticated():
            return self.request.user.profile
        else:
            return get_object_or_404(queryset, user__username=username)


class ValidatePhoneView(DetailView):
    model = Profile
    template_name = 'account/profile/validate_phone.html'

    def get_context_data(self, **kwargs):
        context = super(ValidatePhoneView, self).get_context_data(**kwargs)
        context.update(validate_phone_form=ValidatePhoneForm())
        return context

    def get_object(self):
        return self.request.user.profile


class ConfirmationEmail(DetailView):
    model = Profile
    template_name = 'account/confirmation_email_verified.html'

    def get_object(self):
        queryset = self.get_queryset()
        email_code = self.kwargs.get('email_code')
        profile = get_object_or_404(queryset, email_code=email_code)
        profile.is_email_verified = True
        profile.email_code = code_generate(size=32)
        profile.save()
        return profile


class ConfirmationPhone(APIView):
    queryset = Profile.objects.all()

    def put(self, request, **kwargs):
        self.object = self.get_object()

        self.object.is_phone_verified = True
        self.object.save()

        return Response({
            'profile_id': self.object.id,
            'is_phone_verified': self.object.is_phone_verified,
        })

    def get_object(self):
        phone_code = self.kwargs.get('phone_code')
        profile = get_object_or_404(self.queryset, phone_code=phone_code)
        profile.is_phone_verified = True
        profile.phone_code = code_generate()
        profile.save()
        return profile


class UpdateProfileAboutView(UpdateView):
    model = Profile
    template_name = 'account/profile.html'
    form_class = UpdateProfileAboutForm

    def get_object(self):
        return self.request.user.profile

    def form_invalid(self, form):
        return redirect('profile')

    def get_success_url(self):
        return reverse('profile')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateProfileAboutView, self).dispatch(*args, **kwargs)


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

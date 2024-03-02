from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UserForm


class RegistrationView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('index')
    template_name = 'usersRegistration/signup.html'

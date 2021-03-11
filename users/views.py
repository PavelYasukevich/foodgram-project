from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(SuccessMessageMixin, CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    success_message = 'Ученая запись успешно создана'
    template_name = 'users/reg.html'

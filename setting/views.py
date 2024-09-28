from django.shortcuts import render
from login.models import User, Avatar
from django.views.generic.edit import UpdateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from setting.forms import AvatarForm


# Create your views here.
# kenji1
# kenji.konno@soliton-advisors.com
# Def6392a / Melbourn65

# Create your views here.
from django.contrib.auth.decorators import login_required
@login_required()
def home(request):
    return render(request, 'setting/home.html')

class SettingUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "avatar"]
    template_name = 'setting/user_form.html'
    success_url = reverse_lazy('setting:home')  # Redirect after successful update

class AvatarUpdateView(FormView):
    fields = ["avatarid", "image"]
    template_name = 'setting/avatar_form.html'
    form_class = AvatarForm
    success_url = reverse_lazy('setting:home')  # Redirect after successful update

    def form_valid(self, form):
        # Handle form processing here, e.g., save the avatar
        avatar_id = form.cleaned_data['avatarid']
        image = form.cleaned_data['image']
        # Save the avatar logic goes here

        # Create or update the avatar instance
        Avatar.objects.update_or_create(
            avatarid=avatar_id,  # Use avatar_id to find the instance
            defaults={'image': image}  # Update the image field
        )
        
        return super().form_valid(form)
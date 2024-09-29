from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from login.forms import CustomUserCreationForm
from login.models import User
from django.utils.encoding import force_str
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode

# Create your views here.
# kenji2
# kenji.konno@soliton-advisors.com
# Def6392a / Melbourn65

class CustomLoginView(LoginView):
    template_name = 'login/login.html'
    authentication_form = AuthenticationForm #ログインに使用するフォームを指定
    redirect_authenticated_user = True #ユーザー認証後に自動的に表示させるか
    success_url = reverse_lazy('setting:home') #ログイン成功後に表示させるページ

    def get_success_url(self):
        return self.success_url

class CustomRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'login/register.html'
    success_url = reverse_lazy('user:login')  # Redirect to login page after successful registration

    def form_valid(self, form):
        # You can add custom logic here if needed
        print("form is valid in VIEW:")  # Log form errors
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Log form errors
        return self.render_to_response(self.get_context_data(form=form))

# ログイン後パスワードの変更をする場合に使用する
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'login/password_change_form.html'
    success_url = reverse_lazy('user:password_change_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()  # Make sure the form is included in the context
        return context

# ログイン後パスワードの変更をして完成した場合
class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'login/password_change_done.html'  # Custom success template

# ログアウトの機能
class CustomLogoutView(LogoutView):
    template_name = 'login/logged_out.html'

# パスワードを忘れた場合、再登録メールを送信する
class CustomPasswordResetView(PasswordResetView):
    template_name = 'login/password_reset_form.html'
    email_template_name = 'login/password_reset_email.html'  #Eメールのテンプレート
    subject_template_name = 'login/password_reset_subject.txt'  #Eメール Subject のテンプレート
    success_url = reverse_lazy('user:password_reset_done')  # URL to redirect to after form submission
    html_email_template_name = 'login/password_reset_email.html'  # Add this for HTML email

# パスワードリセット用のメールを送信した旨のページを表示する
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'login/password_reset_done.html'

# 実際にパスワードを変更する
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'login/password_reset_confirm.html'
    success_url = reverse_lazy('user:password_reset_complete')

    def get(self, request, *args, **kwargs):
        uid = kwargs['uidb64']
        token = kwargs['token']
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            self.user = get_object_or_404(User, pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            self.user = None
        return super().get(request, *args, **kwargs)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'login/password_reset_complete.html'



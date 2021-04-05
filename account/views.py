from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from blog.models import Article
from .forms import ProfileForm
from .mixins import FieldsMixin, FormValidMixin, AuthorAccessMixin, SuperUserAccessMixin, AuthorsAccessMixin

# @login_required
# def home(request):
#     return render(request,'registration/home.html')
from .models import User


class ArticleList(AuthorsAccessMixin, ListView) :
    template_name = 'registration/home.html'

    def get_queryset(self) :
        if self.request.user.is_superuser :
            return Article.objects.all()
        else :
            return self.request.user.articles.all()
            # return Article.objects.filter(author = self.request.user)


class ArticleCreate(AuthorsAccessMixin, FieldsMixin, FormValidMixin, CreateView) :
    model = Article
    template_name = 'registration/article-create-update.html'


class ArticleUpdate(AuthorAccessMixin, FieldsMixin, FormValidMixin, UpdateView) :
    model = Article
    template_name = 'registration/article-create-update.html'


class ArticleDelete(SuperUserAccessMixin, DeleteView) :
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_confirm_delete.html'


class Profile(LoginRequiredMixin, UpdateView) :
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('account:profile')
    form_class = ProfileForm

    def get_object(self, queryset=None) :
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self) :
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update(
            {
                'user' : self.request.user
            }
        )
        return kwargs


class Login(LoginView) :
    def get_success_url(self) :
        user = self.request.user

        if user.is_superuser or user.is_author :
            return reverse_lazy('account:home')
        else :
            return reverse_lazy('account:profile')


class PasswordChange(PasswordChangeView) :
    success_url = reverse_lazy('account:profile')


from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import User
from django.core.mail import EmailMessage


class Register(CreateView) :
    form_class = SignupForm
    template_name = 'registration/register.html'

    def form_valid(self, form) :
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)

        # sending email
        mail_subject = 'فعال سازی اکانت'
        message = render_to_string('registration/activate_account.html', {
            'user' : user,
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('<p>لینک فعالسازی به ایمیل شما ارسال شد </p>  <a href ="/login">ورود </a>')


def activate(request, uidb64, token) :
    try :
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) :
        user = None
    if user is not None and account_activation_token.check_token(user, token) :
        user.is_active = True
        user.save()
        # login(request, user)
        # # return redirect('home')
        return HttpResponse(
            '<p>اکانت شما با موفقیت فعال شد.برای ورود </p> <a href ="/login"> کلیک</a> کنید.')
    else :
        return HttpResponse('<p> لینک فعالسازی منقضی شده است </p> <a href ="/register">دوباره امتحان کنید </a> ')

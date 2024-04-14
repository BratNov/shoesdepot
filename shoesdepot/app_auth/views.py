from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import views as auth_views, login, get_user_model, logout
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegisterUserForm, LoginUserForm, UpdateUserForm, ChangePasswordForm, ProfileForm
from django.contrib import messages
from .models import Profile
from ..cart.models import Cart

UserModel = get_user_model()


class RegisterUserView(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'app_auth/register_user.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class LoginUserView(auth_views.LoginView):
    form_class = LoginUserForm
    template_name = 'app_auth/login_user.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user

        if 'cart' in self.request.session:
            cart_session = self.request.session['cart']
            try:
                user_cart = Cart.objects.get(user=user)
                cart_db = user_cart.cart_data
                combined_cart = {**cart_db, **cart_session}
                self.request.session['cart'] = combined_cart
                cart_items = sum(item['quantity'] for item in combined_cart.values())
                self.request.session['cart_items_count'] = cart_items
                user_cart.delete()
                messages.success(self.request, "Your cart has been successfully merged.")
                return redirect('cart_summary')
            except Cart.DoesNotExist:
                pass
        else:
            try:
                user_cart = Cart.objects.get(user=user)
                self.request.session['cart'] = user_cart.cart_data
                self.request.session['cart_items_count'] = user_cart.cart_items
                user_cart.delete()
                messages.success(self.request, "Your cart has been successfully loaded.")
                return redirect('cart_summary')
            except Cart.DoesNotExist:
                pass

        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        return next_url or reverse_lazy('home')


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'app_auth/profile.html'
    success_url = reverse_lazy('profile')
    extra_context = {'title': 'Update Profile', 'url': reverse_lazy('profile'), 'button': 'Update Profile'}

    def get_object(self, queryset=None):
        user = self.request.user
        return get_object_or_404(Profile, user=user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Profile successfully updated.')
        return super().form_valid(form)


class EmailChangeView(LoginRequiredMixin, generic.UpdateView):
    model = UserModel
    form_class = UpdateUserForm
    template_name = 'app_auth/profile.html'
    success_url = reverse_lazy('email_change')
    extra_context = {'title': 'Change Email', 'url': reverse_lazy('email_change'), 'button': 'Change Email'}

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Email successfully changed.')
        return super().form_valid(form)


class ChangePasswordView(LoginRequiredMixin, auth_views.PasswordChangeView):
    model = UserModel
    form_class = ChangePasswordForm
    template_name = 'app_auth/profile.html'
    success_url = reverse_lazy('change_password')
    extra_context = {'title': 'Change Password', 'url': reverse_lazy('change_password'), 'button': 'Change Password'}

    def form_valid(self, form):
        response = super().form_valid(form)
        new_password = form.cleaned_data['new_password1']
        self.request.user.set_password(new_password)
        self.request.user.save()
        login(self.request, self.request.user)
        messages.success(self.request, "Password changed successfully!")
        return response


class ProfileDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = UserModel
    template_name = 'app_auth/profile.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Delete Profile', 'url': reverse_lazy('delete_profile'), 'button': 'Delete Profile',
                     'alert': 'Are you sure you want to delete your profile? This action cannot be undone.'}

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def logaut_user(request):
    if 'cart_items_count' in request.session and request.session['cart_items_count'] > 0:
        cart = request.session.get('cart', {})
        cart_items = request.session.get('cart_items_count', 0)
        user = request.user
        Cart.objects.create(user=user, cart_data=cart, cart_items=cart_items)

    logout(request)
    return redirect('login_user')

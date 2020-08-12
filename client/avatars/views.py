from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
import connection
from braces.views import SelectRelatedMixin

from . import models

from django.contrib.auth import get_user_model
User = get_user_model()


class SingleAvatar(generic.DetailView):
    model = models.Avatar


class UserAvatar(generic.ListView):
    model = models.Avatar
    template_name = "avatars/user_avatar_list.html"
    success_url = reverse_lazy('avatars/user_avatar_list.html')
    home_page = "test.html"

    def post(self, request, username):
        choose = request.POST.get('avatar_list')
        if choose is None:
            messages.error(request, "You must choose avatar!")
            return HttpResponseRedirect(request.path_info)
        user_avatars = self.get_queryset()
        user_avatars.update(is_choosen=False)
        user_avatars.filter(avatar_name=choose).update(is_choosen=True)
        return render(request, self.home_page)

    def get_queryset(self):
        try:
            self.avatar_user = User.objects.prefetch_related("avatars").get(
                username__iexact=self.kwargs.get("username")
            )

        except User.DoesNotExist:
            raise Http404
        else:
            return self.avatar_user.avatars.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["avatar_user"] = self.avatar_user
        return context


class AvatarDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Avatar
    select_related = ["user"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreateAvatar(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):

    fields = ('avatar_name', 'avatar_password', 'avatar_email')
    model = models.Avatar
    select_related = ["user"]

    def get_success_url(self):
        return reverse_lazy('avatars:for_user', kwargs={'username': self.request.user})

    def form_valid(self, form):
        con = connection.Connection()
        name = form.cleaned_data['avatar_name']
        password = form.cleaned_data['avatar_password']
        email = form.cleaned_data['avatar_email']
        is_succeed, text_error = con.create_user(name, password, email)
        if is_succeed:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            messages.success(self.request, text_error)
            return super().form_valid(form)
        else:
            messages.error(self.request, text_error)
            return HttpResponseRedirect(self.request.path_info)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )

    def get_user(self):
        return self.request.user


class DeleteAvatar(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Avatar
    select_related = ["user"]

    def get_success_url(self):
        return reverse_lazy('avatars:for_user', kwargs={'username': self.request.user})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Avatar Deleted")
        return super().delete(*args, **kwargs)

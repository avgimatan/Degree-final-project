from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseRedirect, HttpResponse
from . import models
from django.contrib import messages
from .forms import SearchForm
import connection
import scrapy_running
from multiprocessing import Process

User = get_user_model()


class SearchChoose(generic.ListView):
    model = models.Search
    template_name = "search/search_base.html"

    def post(self, request):
        user_avatars = self.get_queryset()
        current_avatar = user_avatars.filter(is_choosen=True)
        if current_avatar is None:
            messages.error(request, "You must choose avatar before navigating to link")
            return HttpResponseRedirect(request.path_info)
        try:
            user = current_avatar[0].avatar_name
            password = current_avatar[0].avatar_password
        except:
            messages.error(request, "You must choose avatar before navigating to link")
            return HttpResponseRedirect(request.path_info)
        user_or_keyword = request.POST.get('crawling')
        crawl_text = request.POST.get('crawl_text')
        if crawl_text is "":
            messages.error(request, "Enter text before crawling")
            return HttpResponseRedirect(request.path_info)
        if user_or_keyword == 'user':
            p = Process(target=scrapy_running.scrapy_running_by_user, args=('author', crawl_text, user, password, str(self.request.user)))
            p.start()
            messages.add_message(request, messages.INFO, "Crawling By User Started")
            return HttpResponseRedirect(request.path_info)
        else:
            p = Process(target=scrapy_running.scrapy_running_by_user, args=('keywords', crawl_text, user, password, str(self.request.user)))
            p.start()
            messages.add_message(request, messages.INFO, "Crawling By Keyword Started")
            return HttpResponseRedirect(request.path_info)

    def get_queryset(self):
        try:
            self.avatar_user = User.objects.prefetch_related("avatars").get(
                username__iexact=self.request.user
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.avatar_user.avatars.all()


class UserDashboard(generic.FormView):
    # model = models.Search
    form_class = SearchForm
    template_name = "search/user_dashboard.html"

    def post(self, request):
        form = SearchForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['link']
            user_avatars = self.get_queryset()
            current_avatar = user_avatars.filter(is_choosen=True)
            if current_avatar is None:
                messages.error(request, "You must choose avatar before navigating to link")
                return HttpResponseRedirect(request.path_info)
            try:
                user = current_avatar[0].avatar_name
                password = current_avatar[0].avatar_password
            except:
                messages.error(request, "You must choose avatar before navigating to link")
                return HttpResponseRedirect(request.path_info)
            try:
                con = connection.Connection()
                con.go_to_link(text, user, password)
            except:
                pass
            return HttpResponseRedirect(request.path_info)

    def get_queryset(self):
        try:
            self.avatar_user = User.objects.prefetch_related("avatars").get(
                username__iexact=self.request.user
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.avatar_user.avatars.all()


class KeywordDashboard(generic.FormView):
    form_class = SearchForm
    template_name = "search/keyword_dashboard.html"

    def post(self, request):
        form = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['link']
            user_avatars = self.get_queryset()
            current_avatar = user_avatars.filter(is_choosen=True)
            if current_avatar is None:
                messages.error(request, "You must choose avatar before navigating to link")
                return HttpResponseRedirect(request.path_info)
            try:
                user = current_avatar[0].avatar_name
                password = current_avatar[0].avatar_password
            except:
                messages.error(request, "You must choose avatar before navigating to link")
                return HttpResponseRedirect(request.path_info)
            try:
                con = connection.Connection()
                con.go_to_link(text, user, password)
            except:
                pass
            return HttpResponseRedirect(request.path_info)

    def get_queryset(self):
        try:
            self.avatar_user = User.objects.prefetch_related("avatars").get(
                username__iexact=self.request.user
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.avatar_user.avatars.all()

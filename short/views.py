from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.db.models import F
from django.contrib import messages
from .forms import UrlForm
from .models import Urls


# Create your views here.

class Shortener:
    # basically https://github.com/delight-im/ShortURL/blob/master/Python/shorturl.py
    # minus the features it includes with the different alphabet
    _alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    _base = len(_alphabet)

    def Encode(self, number):
        string = ''
        while(number > 0):
            string = self._alphabet[number % self._base] + string
            number //= self._base
        return string

    def Decode(self, string):
        number = 0
        for char in string:
            number = number * self._base + self._alphabet.index(char)
        return number

def urlRedirect(request, string):
    # redirect from a shortened url
    foo = Shortener()
    try:
        RedirectLink = Urls.objects.get(pk=foo.Decode(string))
        RedirectLink.visits = F('visits') + 1
        RedirectLink.save()
    except:
        messages.add_message(request, messages.ERROR, 'This link is broken or has expired.')
        return redirect(reverse('home'))
    return HttpResponseRedirect(RedirectLink.url)

class Home(View):
    def get(self, request):
        return render(request, 'short/home.html')

    def post(self, request):
        form = UrlForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            foo = Shortener()
            if data['original']:
                try:
                    url = Urls.objects.create(url=data['original'])
                except:
                    url = Urls.objects.get(url=data['original'])
                new = foo.Encode(url.pk)
                context = {
                    'original' : url.url,
                    'shortened' : request.build_absolute_uri()+new
                }
            elif data['shortened']:
                #strip key from shortened url
                key = data['shortened'].replace(request.build_absolute_uri(),'')
                old = foo.Decode(key)
                try:
                    url = Urls.objects.get(pk=old)
                except:
                    messages.add_message(request, messages.ERROR, 'This link is broken or has expired.')
                    return redirect(reverse('home'))
                context = {
                    'original' : url.url,
                    'shortened' : data['shortened']
                }
        else:
            return redirect(reverse('home'))
        return render(request, 'short/home.html',context)

from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.db.models import F
from django.contrib import messages
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

# store Url in database and encode UrlID
def urlRedirect(request, string):
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
        data = request.POST.get('link_to_short')
        try:
            url = Urls.objects.create(url=data)
        except:
            url = Urls.objects.get(url=data)
        foo = Shortener()
        new = foo.Encode(url.id)
        context = {
            'original' : url.url,
            'shortened' : request.build_absolute_uri()+new
        }
        return render(request, 'short/home.html',context)

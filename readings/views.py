from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
import requests


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
# Create your views here.
class Home(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        data = []
        r = requests.get(
            'https://api.thingspeak.com/channels/306267/feeds.json?results=1'
            , params=request.GET)   
        if r.status_code == 200:
            data = r.json()
        temp = data['feeds'][0]['field1'] 
        mositure =  data['feeds'][0]['field2']
        at =  data['feeds'][0]['field3']
        return render(request, self.template_name,
                    {'temp': temp, 'mositure': mositure, 'at':  at,
                     'activedashboard': 'active'})

class Temperature(View):
    template_name = 'temperature.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                        {'activetemp': 'active'})

class Moisture(View):
    template_name = 'moisture.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                        {'activemositure': 'active'})

class Pressure(View):
    template_name = 'at.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                        {'activepressure': 'active'})           

@cache_page(CACHE_TTL)
def get_readings(request):
    data = []
    r = requests.get('https://api.thingspeak.com/channels/306267/feeds.json?results=100', params=request.GET)
    if r.status_code == 200:
        data = r.json() 
    return JsonResponse(list(data['feeds']), safe=False)

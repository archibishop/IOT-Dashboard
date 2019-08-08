from django.shortcuts import render
from django.views import View
import requests

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
                        {'temp': temp, 'mositure': mositure, 'at':  at})

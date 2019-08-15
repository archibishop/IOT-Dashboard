from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from easy_pdf.views import PDFTemplateView
from django.conf import settings
import requests
from io import BytesIO
from django.http import HttpResponse
from django.conf import settings
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from reportlab.platypus import SimpleDocTemplate, Image
from django.contrib.sites.shortcuts import get_current_site
import os


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

class PDF(View):
    def get(self, request, *args, **kwargs):
        data = []
        r = requests.get('https://api.thingspeak.com/channels/306267/feeds.json?results=100', params=request.GET)
        if r.status_code == 200:
            data = r.json()
        template_name = 'pdf-temp.html'     
        if kwargs['page'] == 2:
            template_name = 'pdf-moisture.html'
        elif kwargs['page'] == 3:  
            template_name = 'pdf-at.html'  
        return render(request, template_name,
                        {'activemositure': 'active', 'data_json': data})  
                         

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        local =  os.environ.get('local', True)
        doc = SimpleDocTemplate(response,topMargin=2)
        chrome_options = Options()
        chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', None)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless") 
        chrome_options.binary_location = chrome_bin
        # For local environment
        if local:
            driver = webdriver.Chrome(ChromeDriverManager().install(),
                                chrome_options=chrome_options)
        else:                        
            chrome_exec_shim = os.environ.get("$GOOGLE_CHROME_SHIM", "chromedriver")
            driver = webdriver.Chrome(executable_path=chrome_exec_shim,
                                chrome_options=chrome_options)
        domain = 'http://{}'.format(get_current_site(request))
        url = "{}/pdf/{}".format(domain, str(kwargs['page']))                                                                   
        driver.get(url)
        total_width = driver.execute_script("return document.body.scrollWidth")
        total_height = driver.execute_script("return document.body.scrollHeight")
        driver.set_window_size(total_width, total_height)      
        screenshot = driver.get_screenshot_as_png()
        i = Image(BytesIO(screenshot))
        i.drawHeight =  700
        i.drawWidth = 600
        elements = []
        elements.append(i)
        doc.build(elements)
        return response

# @cache_page(CACHE_TTL)
def get_readings(request):
    data = []
    r = requests.get('https://api.thingspeak.com/channels/306267/feeds.json?results=100', params=request.GET)
    if r.status_code == 200:
        data = r.json() 
    return JsonResponse(list(data['feeds']), safe=False)


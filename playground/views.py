from django.shortcuts import render
import logging
from rest_framework.views import APIView
import requests
# Create your views here.

logger = logging.getLogger(__name__) 

class HelloView(APIView):

   
    def get(self, request):
        try:
            logger.info("Calling httpbin")
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Receied the response')
            data = response.json()
        except requests.ConnectionError:
            logger.critical('httpbin is offline')

        return render(request, 'hello.html', context={
            'name':data
        })
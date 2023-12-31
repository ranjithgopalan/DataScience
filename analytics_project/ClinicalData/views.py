from django.shortcuts import render
import requests
# Create your views here.

# from django.contrib.sites import requests
from django.views import generic


def getclinicalData(request):
        url = 'https://ranjith1.azurewebsites.net/EmployeeList'
        # params = {'ID': {id}}
        # r = requests.get(url, params=params)
        r = requests.get(url)
        # print(r['results'][0])

        # Employee = r.json()
        # Employee_list = {'Employee': Employee['results']}
        return render( request, "ClinicalData.html", context ={"mylist":[r.content]})



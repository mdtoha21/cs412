from django.shortcuts import render

from django.http import HttpRequest, HttpResponse
import random
from datetime import datetime, timedelta


# Create your views here.

def home(request):

    template_name='restaurant/base.html'


    return render(request,template_name)


def order(request):


    return render(request, "restaurant/order.html")



def submit(request):

    print(request)
    template_name='restaurant/confirmation.html'

    if request.method=="POST":
        flavors = request.POST.getlist("flavor")
        toppings = request.POST.getlist("topping")

     

        ready_time = datetime.now() + timedelta(minutes=15)

        size = request.POST.get("size")
        adress=request.POST.get("adress")
        context = {
            "flavors": flavors,
            "size": size,
            "toppings": toppings,
            "adress": adress,
            "ready_time": ready_time,
        }

        return render(request, "restaurant/confirmation.html", context)
    else:
        return render(request, template_name, context)

    
    
    


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext, get_object_or_404
from django.core.mail import send_mail

from .models import Contact
from .forms import ContactForm


def contact_us(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        save_form = form.save(commit=False)
        send = send_mail('Message from Enchanted:', str(save_form.message), str(save_form.email), ['Djangorockstar@gmail.com'], fail_silently = True)
        save_form.save()
        
    return render_to_response('contact/contact_us.html', locals(), context_instance=RequestContext(request))

def home(request):
	return render_to_response('home.html', locals(), context_instance=RequestContext(request))
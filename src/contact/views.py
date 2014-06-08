from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext, get_object_or_404


from .models import Contact
from .forms import ContactForm


def contact_us(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        save_form = form.save(commit=False)
        save_form.save()
        
    return render_to_response('contact/contact_us.html', locals(), context_instance=RequestContext(request))
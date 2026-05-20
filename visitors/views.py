from django.shortcuts import render, redirect
from .forms import VisitorRequestForm


def create_visitor_request(request):

    if request.method == 'POST':

        form = VisitorRequestForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/visitors/success/')

    else:
        form = VisitorRequestForm()

    return render(request, 'visitors/request_form.html', {
        'form': form
    })


def success_page(request):
    return render(request, 'visitors/success.html')
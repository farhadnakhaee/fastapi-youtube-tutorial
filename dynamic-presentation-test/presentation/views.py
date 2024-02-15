from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .digikala_api import DigikalaAPI
from .models import Presentation, Url
import json

digikala_api = DigikalaAPI()

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                return redirect('presentation_list')

        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('presentation_list')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def presentation_list(request):
    user_object = request.user
    presentations = Presentation.objects.filter(user=user_object)
    response = {
        'presentations': [
        {
            'title': presentation.title, 
            'subtitle': presentation.subtitle, 
            'presenter_name': presentation.presenter_name, 
            'date': presentation.date, 
            'background_image': presentation.background_image.url, 
            'slug': presentation.slug, 
            'urls': [url.url for url in presentation.urls.all()]
            }
        for presentation in presentations]
        }

    return JsonResponse(response, safe=False)

@login_required(login_url='signin')
def create_presentation(request):

    if request.method == 'POST':
        urls = request.POST.getlist('urls[]')

        new_presentation = Presentation.objects.create(
            user=request.user,
            title=request.POST['title'],
            subtitle=request.POST['subtitle'],
            presenter_name=request.POST['presenter_name'],
            date=request.POST['date'],
            background_image=request.FILES.get('background_image'),
            slug=request.POST['slug'],
        )
        for url in urls:
            url_object, created = Url.objects.get_or_create(url=url)
            new_presentation.urls.add(url_object)
        new_presentation.save()

        # for order, url in enumerate(urls):
        #     # if url not in Url.objects.values('url'):
        #     data = digikala_api.get_section(url)
            # Url.objects.create(presentation=new_presentation, order=order+1, url=url)

        return redirect('presentation_list')
    return render(request, 'create_presentation.html')

@login_required(login_url='signin')
def delete_presentation(request, pk):
    presentation = Presentation.objects.get(id=pk)
    presentation.delete()
    return redirect('presentation_list')

# @login_required(login_url='signin')
# def update_presentation(request, pk):
    presentation = Presentation.objects.get(pk=pk)
    urls = Url.objects.filter(presentation=presentation)

    if request.method == "POST":
        new_background_image = request.FILES.get('background_image')
        if new_background_image:
            presentation.background_image=new_background_image
        presentation.title=request.POST['title']
        presentation.subtitle=request.POST['subtitle']
        presentation.presenter_name=request.POST['presenter_name']
        presentation.date=request.POST['date']
        presentation.slug=request.POST['slug']
        presentation.save()

        new_urls = request.POST.getlist('urls[]')
        urls.delete()
        for order, url in enumerate(new_urls):
            Url.objects.create(presentation=presentation, order=order+1, url=url)
        
        return redirect('presentation_list')
    return render(request, 'create_presentation.html', {'presentation': presentation, 'urls': urls})

@login_required(login_url='signin')
def slide_detail(request, presentation_name, slide_id):
    user = request.user
    presentation = get_object_or_404(Presentation, slug=presentation_name, user=user)
    url = get_object_or_404(Url, presentation=presentation, order=slide_id)
    data = url.fetch_data()
    data['order'] = url.order
    return JsonResponse(data, safe=False)

@login_required(login_url='signin')
def presentation_slides_order(request, presentation_name):
    presentation = get_object_or_404(Presentation, slug=presentation_name)
    orders_of_urls = Url.objects.filter(presentation=presentation)
    response = {'presentation_name': presentation.slug,
                'ids_of_slides': [url.id for url in orders_of_urls], 
                'orders_of_slides': [url.order for url in orders_of_urls],
                }
    return JsonResponse(response, safe=False)
    
    
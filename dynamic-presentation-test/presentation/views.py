from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Presentation, Slide
from .serializers import PresentationSerializer
from .digikala_api import DigikalaAPI

digikala_api = DigikalaAPI()


class PresentationList(ListCreateAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    permission_classes = [AllowAny]


class PresentationDetail(RetrieveUpdateDestroyAPIView):
    queryset = Presentation.objects.all()
    serializer_class = PresentationSerializer
    lookup_field = "slug"


class SlideDetailView(APIView):
    def get(self, request, slug, order):
        presentation = get_object_or_404(Presentation, slug=slug)
        slide = presentation.slides.filter(order=order).first()

        if slide is None:
            return Response({"error": "Slide not found."}, status=404)

        return Response(slide.data)


# user views


@login_required(login_url='login')
def index(request):
    presentations = Presentation.objects.filter(user=request.user).all()
    return render(request, "presentation/presentation_list.html", {"presentations": presentations})


def login(request):

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    else:
        return render(request, 'presentation/login.html')
    

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def create(request):
    if request.method == 'POST':
        urls = request.POST.getlist('urls[]')

        presentation = Presentation.objects.create(
            user=request.user,
            title = request.POST['title'],
            subtitle = request.POST['subtitle'],
            presenter_name = request.POST['presenter_name'],
            present_date = request.POST['present_date'],
            background_image = request.FILES.get('background_image'),
            slug = request.POST['slug'],
        )
        
        for order, url in enumerate(urls):
            Slide.objects.create(
                presentation=presentation,
                order=order+1,
                url=url,
                data=digikala_api.get_section(url),
            )
        presentation.save()

        return redirect('index')
    return render(request, 'presentation/create_presentation.html')


@login_required(login_url='login')
def delete(request, slug):
    presentation = Presentation.objects.filter(user=request.user, slug=slug).first()
    presentation.delete()
    return redirect('index')


@login_required(login_url='login')
def update(request, slug):
    presentation = Presentation.objects.filter(user=request.user, slug=slug).first()
    slides = Slide.objects.filter(presentation=presentation)

    if request.method == "POST":
        new_background_image = request.FILES.get('background_image')
        if new_background_image:
            presentation.background_image=new_background_image
        presentation.title=request.POST['title']
        presentation.subtitle=request.POST['subtitle']
        presentation.presenter_name=request.POST['presenter_name']
        presentation.date=request.POST['present_date']
        presentation.slug=request.POST['slug']
        presentation.save()

        new_urls = request.POST.getlist('urls[]')
        slides.delete()
        for order, url in enumerate(new_urls):
            Slide.objects.create(
                presentation=presentation,
                order=order+1,
                url=url,
                data=digikala_api.get_section(url),
            )
        
        return redirect('index')
    return render(request, 'presentation/create_presentation.html', {'presentation': presentation, 'slides': slides})
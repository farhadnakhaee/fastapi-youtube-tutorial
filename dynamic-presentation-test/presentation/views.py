from django.shortcuts import render
from .digikala_api import DigikalaAPI

def section(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        section_url = request.POST['section']
        section_data = DigikalaAPI.get_section(section_url)
        user = User.objects.get(username=username)
        
        if section_data:
            return render(request, 'context.html', {'order': 1, 'result': section_data})


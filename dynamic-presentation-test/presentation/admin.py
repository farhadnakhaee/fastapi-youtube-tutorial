import json
from typing import Any
from django.contrib import admin, messages
from django import forms
from django.http import HttpRequest
from django.utils.html import format_html
from .models import Presentation, Slide
from .digikala_api import DigikalaAPI

digikala_api = DigikalaAPI()


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ["presentation", "url", "order"]
    readonly_fields = ('presentation', 'url', 'order', 'pretty_json_data',)
    exclude = ('data',)

    def pretty_json_data(self, obj):
        data = json.dumps(obj.data, indent=4)
        return format_html('<pre>{}</pre>', data)
    
    pretty_json_data.short_description = 'JSON Data'


class SlideInline(admin.TabularInline):
    model = Slide
    extra = 0
    exclude = ('data',)
    ordering = ('order',) # todo: add ordering to main file


class PresentationAdminForm(forms.ModelForm):
    class Meta:
        model = Presentation
        exclude = ('user',)


@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    form = PresentationAdminForm
    inlines = [SlideInline]
    list_display = ["title", "subtitle", "present_date"]
    prepopulated_fields = {"slug": ['title', 'subtitle']}

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def save_related(self, request: Any, form: Any, formsets: Any, change: Any) -> None:
        super().save_related(request, form, formsets, change)

        for order, slide in enumerate(form.instance.slides.all()):
            slide_data = digikala_api.get_section(slide.url)
            if slide_data:
                slide_data['order'] = order + 1 
                slide_data['html_id'] = slide.url
                slide.data = slide_data
                slide.order = order + 1
                slide.save()
            else:
                messages.warning(request, f"Warning: Url ({slide.url}) is Wrong!")
            # todo: add this else block



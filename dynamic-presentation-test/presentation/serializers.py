from rest_framework import serializers
from .models import Presentation, Slide
from .digikala_api import DigikalaAPI

digikala_api = DigikalaAPI()

class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ["url"]


class PresentationSerializer(serializers.ModelSerializer):
    slides = SlideSerializer(many=True)
    slides_count = serializers.SerializerMethodField(method_name="calculate_slides_count")

    class Meta:
        model = Presentation
        fields = [
            "title",
            "subtitle",
            "presenter_name",
            "present_date",
            "slug",
            "background_image",
            "slides_count",
            "slides",
        ]

    def calculate_slides_count(self, presentation: Presentation):
        return Slide.objects.filter(presentation=presentation).count()

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        slides_data = validated_data.pop('slides')
        presentation = Presentation.objects.create(**validated_data)
        for order, slide_data in enumerate(slides_data):
            data = digikala_api.get_section(slide_data["url"])
            Slide.objects.create(presentation=presentation, url=slide_data["url"], order=order, data=data)
        return presentation

from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from .models import Title


class TitleFilter(FilterSet):
    name = CharFilter(field_name='name')
    year = NumberFilter(field_name='year')
    rating = NumberFilter(field_name='rating')
    description = CharFilter(field_name='description')
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

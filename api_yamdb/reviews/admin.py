from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.resources import ModelResource

from .models import Category, Comment, Genre, Review, Title, TitleGenre


class CategoryResource(ModelResource):
    """Модель ресурсов категорий произведений."""

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
        )


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    """Модель эскпорта и импорта категорий приложений."""

    resource_classes = (CategoryResource,)
    list_display = (
        'id',
        'name',
        'slug',
    )


class GenreResource(ModelResource):
    """Модель ресурсов жанров произведений."""

    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'slug',
        )


@admin.register(Genre)
class GenresAdmin(ImportExportModelAdmin):
    """Модель эскпорта и импорта произведений."""

    resource_classes = (GenreResource,)
    list_display = (
        'id',
        'name',
        'slug',
    )


class TitleResource(ModelResource):
    """Модель ресурсов произведений."""

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
        )


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    """Модель эскпорта и импорта произведений."""

    resource_classes = (TitleResource,)
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
    )


class TitleGenreResource(ModelResource):
    """Модель ресурсов произведений и жанров."""

    title = Field(attribute='title_id', column_name='title_id')
    genre = Field(attribute='genre_id', column_name='genre_id')

    class Meta:
        model = TitleGenre
        fields = (
            'id',
            'title',
            'genre',
        )


@admin.register(TitleGenre)
class TitlesGenresAdmin(ImportExportModelAdmin):
    """Модель эскпорта и импорта произвдеений, и жанров."""

    resource_classes = (TitleGenreResource,)
    list_display = (
        'id',
        'title',
        'genre',
    )


class CommentResource(ModelResource):
    """Модель ресурсов комментариев."""

    review = Field(attribute='review_id', column_name='review_id')

    class Meta:
        model = Comment
        fields = (
            'id',
            'review',
            'text',
            'author',
            'pub_date',
        )


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    """Модель эскпорта и импорта комментариев."""

    resource_classes = (CommentResource,)
    list_display = (
        'id',
        'review',
        'text',
        'author',
        'pub_date',
    )


class ReviewResource(ModelResource):
    """Модель ресурсов отзывов."""

    title = Field(attribute='title_id', column_name='title_id')

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'text',
            'author',
            'score',
            'pub_date',
        )


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    """Модель эскпорта и импорта отзывов."""

    resource_classes = (ReviewResource,)
    list_display = (
        'id',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )

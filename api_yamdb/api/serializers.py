from django.core.validators import MaxLengthValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=(
            validators.UniqueValidator(
                queryset=Category.objects.all(),
                message='slug категорий должно быть уникальными!',
            ),
            MaxLengthValidator(50),
        )
    )

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )
        extra_kwargs = {
            'name': {'required': True},
            'slug': {'required': True},
        }


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        validators=(
            validators.UniqueValidator(
                queryset=Genre.objects.all(),
                message='slug жанров должно быть уникальными!',
            ),
            MaxLengthValidator(50),
        )
    )

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )
        extra_kwargs = {
            'name': {'required': True},
            'slug': {'required': True},
        }


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

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
        extra_kwargs = {
            'id': {'required': True},
            'name': {'required': True},
            'year': {'required': True},
            'rating': {'required': True},
            'description': {'required': True},
            'genre': {'required': True},
            'category': {'required': True},
        }

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj)
        if reviews.count() == 0:
            return None
        else:
            total_score = sum([review.score for review in reviews])
            return round(total_score / reviews.count(), 2)


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
        extra_kwargs = {
            'id': {'required': True},
            'name': {'required': True},
            'description': {'required': True},
            'genre': {'required': True},
            'category': {'required': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        if Review.objects.filter(title=title, author=author).exists():
            raise ValidationError('Нельзя добавить больше одного отзыва!')
        return data

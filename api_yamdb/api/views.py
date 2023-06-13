from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from reviews.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title

from .permissions import IsAdminModeratorOwnerOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
)


class CustomIsAdminOrReadOnlyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Нестандартный вьюсет с фильтром и сортировкой по id.
    Админ может получить/создать/удалить.
    Все остальные могут только получить.
    """

    http_method_names = ('get', 'post', 'delete')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    ordering = ('id',)


class CategoryViewSet(CustomIsAdminOrReadOnlyViewSet):
    """Вьюсет для действий: Получить/Создать/Удалить категорию"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class GenreViewSet(CustomIsAdminOrReadOnlyViewSet):
    """Вьюсет для действий: Получить/Создать/Удалить жанр"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class TitleViewSet(
    CustomIsAdminOrReadOnlyViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """Вьюсет для действий: Получить/Создать/Обновить/Удалить категорию"""

    queryset = Title.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(
                Review,
                pk=self.kwargs.get('review_id'),
                title_id=self.kwargs.get('title_id'),
            ),
        )

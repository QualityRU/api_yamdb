from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year
from users.models import CustomUser


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        verbose_name='Категория',
        help_text='Введите категорию произведения',
        max_length=256,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name='Группа',
        help_text='Введите группу категории произведения',
        max_length=50,
        blank=False,
        unique=True,
    )

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        verbose_name='Жанр',
        help_text='Введите жанр произведения',
        max_length=256,
        blank=False,
    )
    slug = models.SlugField(
        verbose_name='Группа',
        help_text='Введите группу жанра произведения',
        max_length=50,
        blank=False,
        unique=True,
    )

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        verbose_name='Название',
        help_text='Введите название произведения',
        max_length=256,
        blank=False,
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Дата выхода',
        help_text='Введите дату выхода произведения',
        blank=False,
        validators=[
            validate_year,
        ],
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание произведения',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        verbose_name='Жанр',
        help_text='Выберите жанр произведения',
        blank=False,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Выберите категорию произведения',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('id',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Модель произведений и жанров."""

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        help_text='Выберите произведение',
        on_delete=models.CASCADE,
        null=True,
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        help_text='Выберите жанр',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'
        ordering = ('id',)

    def __str__(self):
        return str(self.title)


class Review(models.Model):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь',
    )
    score = models.IntegerField(
        'Оценка', validators=[MaxValueValidator(10), MinValueValidator(1)]
    )
    pub_date = models.DateTimeField('Дата отзыва', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            )
        ]


class Comment(models.Model):
    """Модель комментария."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь',
    )
    pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

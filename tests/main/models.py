from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Расширенный профиль пользователя"""
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    patronymic = models.CharField(max_length=150, verbose_name='Отчество', blank=True)
    city = models.CharField(max_length=100, verbose_name='Город', blank=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', verbose_name='Роль')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль {self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматическое создание профиля при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Автоматическое сохранение профиля при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


class NKO(models.Model):
    """Модель НКО"""
    name = models.CharField(max_length=200, verbose_name='Название')
    category = models.CharField(max_length=100, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    about = models.TextField(verbose_name='О нас', blank=True)
    activities = models.TextField(verbose_name='Направления деятельности', blank=True)
    volunteer_help = models.TextField(verbose_name='Как помогают волонтёры', blank=True)
    address = models.CharField(max_length=300, verbose_name='Адрес', blank=True)
    email = models.EmailField(verbose_name='Email', blank=True)
    phone = models.CharField(max_length=50, verbose_name='Телефон', blank=True)
    website = models.URLField(verbose_name='Сайт', blank=True)
    vk = models.URLField(verbose_name='ВКонтакте', blank=True)
    icon = models.CharField(max_length=10, default='🏢', verbose_name='Иконка')
    city = models.CharField(max_length=100, verbose_name='Город')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрено')

    class Meta:
        verbose_name = 'НКО'
        verbose_name_plural = 'НКО'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class News(models.Model):
    """Модель новостей"""
    title = models.CharField(max_length=300, verbose_name='Заголовок')
    excerpt = models.TextField(verbose_name='Краткое описание')
    content = models.TextField(verbose_name='Полный текст')
    city = models.CharField(max_length=100, verbose_name='Город', blank=True)
    icon = models.CharField(max_length=10, default='📰', verbose_name='Иконка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Event(models.Model):
    """Модель событий"""
    title = models.CharField(max_length=300, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    organizer = models.CharField(max_length=200, verbose_name='Организатор')
    location = models.CharField(max_length=300, verbose_name='Место проведения')
    date = models.DateTimeField(verbose_name='Дата и время')
    city = models.CharField(max_length=100, verbose_name='Город')
    category = models.CharField(max_length=100, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создал')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрено')

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['date']

    def __str__(self):
        return self.title


class KnowledgeItem(models.Model):
    """Модель материалов базы знаний"""
    TYPE_CHOICES = [
        ('video', 'Видео'),
        ('document', 'Документ'),
        ('guide', 'Руководство'),
        ('presentation', 'Презентация'),
    ]

    title = models.CharField(max_length=300, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип')
    icon = models.CharField(max_length=10, default='📄', verbose_name='Иконка')
    file = models.FileField(upload_to='knowledge/', blank=True, verbose_name='Файл')
    url = models.URLField(blank=True, verbose_name='Ссылка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Добавил')

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

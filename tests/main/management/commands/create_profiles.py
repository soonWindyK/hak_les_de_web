"""
Команда для создания профилей для всех пользователей без профиля
Запуск: python manage.py create_profiles
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import UserProfile


class Command(BaseCommand):
    help = 'Создает профили для всех пользователей без профиля'

    def handle(self, *args, **options):
        users_without_profile = []
        
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                users_without_profile.append(user)
                UserProfile.objects.create(user=user)
                self.stdout.write(
                    self.style.SUCCESS(f'Создан профиль для пользователя: {user.username}')
                )
        
        if not users_without_profile:
            self.stdout.write(
                self.style.WARNING('Все пользователи уже имеют профили')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Всего создано профилей: {len(users_without_profile)}')
            )

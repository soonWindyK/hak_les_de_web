from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegistrationForm, EmailAuthenticationForm
from .models import NKO, News, Event, KnowledgeItem


def index(request):
    """Главная страница"""
    return render(request, 'index.html')


def nko_list(request):
    """Список НКО"""
    # Получаем только одобренные НКО
    nko_list = NKO.objects.filter(is_approved=True)
    
    # Фильтрация по городу
    city = request.GET.get('city')
    if city:
        nko_list = nko_list.filter(city=city)
    
    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        nko_list = nko_list.filter(category=category)
    
    return render(request, 'nko.html', {'nko_list': nko_list})


def nko_detail(request, nko_id):
    """Детальная страница НКО"""
    nko = get_object_or_404(NKO, id=nko_id, is_approved=True)
    return render(request, 'nko_detail.html', {'nko': nko})


def news_list(request):
    """Список новостей"""
    news_list = News.objects.all()
    
    # Фильтрация по городу
    city = request.GET.get('city')
    if city:
        news_list = news_list.filter(city=city)
    
    return render(request, 'news.html', {'news_list': news_list})


def news_detail(request, news_id):
    """Детальная страница новости"""
    news = get_object_or_404(News, id=news_id)
    return render(request, 'news_detail.html', {'news': news})


def calendar_view(request):
    """Календарь событий"""
    # Получаем только одобренные события
    events_list = Event.objects.filter(is_approved=True)
    
    # Фильтрация по городу
    city = request.GET.get('city')
    if city:
        events_list = events_list.filter(city=city)
    
    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        events_list = events_list.filter(category=category)
    
    return render(request, 'calendar.html', {'events_list': events_list})


def knowledge_list(request):
    """База знаний"""
    knowledge_list = KnowledgeItem.objects.all()
    
    # Фильтрация по типу
    item_type = request.GET.get('type')
    if item_type:
        knowledge_list = knowledge_list.filter(type=item_type)
    
    return render(request, 'knowledge.html', {'knowledge_list': knowledge_list})


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Сохраняем отчество в профиль
            user.profile.patronymic = form.cleaned_data.get('patronymic', '')
            user.profile.save()
            
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Вход пользователя"""
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.first_name or user.username}!')
                return redirect('index')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Выход пользователя"""
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('index')


@login_required
def profile_redirect(request):
    """Перенаправление на страницу профиля в зависимости от роли"""
    # Создаем профиль, если его нет
    if not hasattr(request.user, 'profile'):
        from .models import UserProfile
        UserProfile.objects.create(user=request.user)
    
    user_role = request.user.profile.role
    
    if user_role == 'admin':
        return redirect('admin_dashboard')
    elif user_role == 'moderator':
        return redirect('moderator_dashboard')
    else:
        return redirect('user_profile')


@login_required
def user_profile(request):
    """Профиль обычного пользователя"""
    return render(request, 'profile/user_profile.html')


@login_required
def moderator_dashboard(request):
    """Панель модератора"""
    return render(request, 'profile/moderator_dashboard.html')


@login_required
def admin_dashboard(request):
    """Панель администратора"""
    return render(request, 'profile/admin_dashboard.html')

// Базовая функциональность для сайта "Добрые дела Росатома"

document.addEventListener('DOMContentLoaded', function() {
    // Обработка выдвижной полоски выбора города
    const cityToggleBtn = document.getElementById('cityToggleBtn');
    const cityBar = document.getElementById('cityBar');
    const citySearch = document.getElementById('citySearch');
    const cityGrid = document.getElementById('cityGrid');
    const cityItems = document.querySelectorAll('.city-grid-item');
    const selectedCityText = document.getElementById('selectedCityText');

    // Открытие/закрытие полоски выбора города
    if (cityToggleBtn) {
        cityToggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            cityBar.classList.toggle('active');
            cityToggleBtn.classList.toggle('active');
            if (cityBar.classList.contains('active')) {
                setTimeout(() => {
                    citySearch.focus();
                }, 100);
            }
        });
    }

    // Закрытие при клике вне полоски
    document.addEventListener('click', function(e) {
        if (cityBar && cityBar.classList.contains('active')) {
            if (!cityBar.contains(e.target) && e.target !== cityToggleBtn && !cityToggleBtn.contains(e.target)) {
                cityBar.classList.remove('active');
                if (cityToggleBtn) {
                    cityToggleBtn.classList.remove('active');
                }
            }
        }
    });

    // Предотвращение закрытия при клике внутри city-bar
    if (cityBar) {
        cityBar.addEventListener('click', function(e) {
            e.stopPropagation();
        });
    }

    // Поиск по городам
    if (citySearch) {
        citySearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            cityItems.forEach(item => {
                const cityName = item.textContent.toLowerCase();
                if (cityName.includes(searchTerm)) {
                    item.classList.remove('hidden');
                } else {
                    item.classList.add('hidden');
                }
            });
        });
    }

    // Выбор города
    cityItems.forEach(item => {
        item.addEventListener('click', function() {
            const cityValue = this.getAttribute('data-city');
            const cityName = this.textContent;
            
            // Обновляем текст кнопки
            if (selectedCityText) {
                selectedCityText.textContent = cityName;
            }
            
            // Убираем выделение со всех элементов
            cityItems.forEach(i => i.classList.remove('selected'));
            
            // Выделяем выбранный элемент
            this.classList.add('selected');
            
            // Закрываем полоску
            if (cityBar) {
                cityBar.classList.remove('active');
            }
            if (cityToggleBtn) {
                cityToggleBtn.classList.remove('active');
            }
            
            // Сохраняем выбор и фильтруем контент
            filterContentByCity(cityValue, cityName);
            
            // Очищаем поиск
            if (citySearch) {
                citySearch.value = '';
                cityItems.forEach(i => i.classList.remove('hidden'));
            }
        });
    });

    // Восстановление выбранного города при загрузке
    const savedCity = localStorage.getItem('selectedCity');
    const savedCityName = localStorage.getItem('selectedCityName');
    if (savedCity && savedCityName) {
        if (selectedCityText) {
            selectedCityText.textContent = savedCityName;
        }
        cityItems.forEach(item => {
            if (item.getAttribute('data-city') === savedCity) {
                item.classList.add('selected');
            }
        });
    }

    // Обработка фильтров
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            const selectedFilter = this.value;
            console.log('Выбран фильтр:', selectedFilter);
            // Здесь будет логика фильтрации
        });
    });

    // Обработка поиска
    const searchInputs = document.querySelectorAll('.search-input');
    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            const searchQuery = this.value.toLowerCase();
            console.log('Поиск:', searchQuery);
            // Здесь будет логика поиска
        });
    });

    // Плавная прокрутка для якорных ссылок
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Закрытие полоски при нажатии Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && cityBar && cityBar.classList.contains('active')) {
            cityBar.classList.remove('active');
            if (cityToggleBtn) {
                cityToggleBtn.classList.remove('active');
            }
        }
    });
});

// Функция фильтрации контента по городу
function filterContentByCity(city, cityName) {
    // Сохраняем выбранный город в localStorage
    if (city) {
        localStorage.setItem('selectedCity', city);
        localStorage.setItem('selectedCityName', cityName);
    } else {
        localStorage.removeItem('selectedCity');
        localStorage.removeItem('selectedCityName');
    }
    
    // В реальном приложении здесь будет AJAX-запрос к серверу
    // для получения отфильтрованных данных
    console.log('Фильтрация контента для города:', city);
}

// Функция для добавления анимации при появлении элементов
function animateOnScroll() {
    const elements = document.querySelectorAll('.nko-card, .knowledge-card, .event-card, .news-card, .cta-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '0';
                entry.target.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    entry.target.style.transition = 'opacity 0.5s, transform 0.5s';
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, 100);
                
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    elements.forEach(element => {
        observer.observe(element);
    });
}

// Запуск анимации при загрузке
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', animateOnScroll);
} else {
    animateOnScroll();
}




    // User menu dropdown functionality
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdown = document.getElementById('userDropdown');

    if (userMenuBtn && userDropdown) {
        // Toggle dropdown on button click
        userMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdown.style.display = userDropdown.style.display === 'block' ? 'none' : 'block';
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!userMenuBtn.contains(e.target) && !userDropdown.contains(e.target)) {
                userDropdown.style.display = 'none';
            }
        });
    }

// Проверка даты рождения - запрет будущих дат при отправке формы
document.addEventListener('DOMContentLoaded', function() {
    const birthDateInput = document.querySelector('input[name="birth_date"]');
    const birthDateError = document.getElementById('birth_date_error');
    
    if (birthDateInput && birthDateError) {
        // Находим форму, содержащую поле даты рождения
        const form = birthDateInput.closest('form');
        
        if (form) {
            form.addEventListener('submit', function(e) {
                const selectedDate = new Date(birthDateInput.value);
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                
                if (birthDateInput.value && selectedDate > today) {
                    e.preventDefault();
                    birthDateError.style.display = 'block';
                    birthDateInput.focus();
                } else {
                    birthDateError.style.display = 'none';
                }
            });
            
            // Скрываем ошибку при изменении даты
            birthDateInput.addEventListener('input', function() {
                birthDateError.style.display = 'none';
            });
        }
    }
});


// Функция для добавления/удаления НКО в избранное
function toggleFavorite(button, nkoId) {
    button.classList.toggle('active');
    
    // Здесь будет AJAX-запрос к серверу для сохранения в избранное
    const isActive = button.classList.contains('active');
    
    if (isActive) {
        console.log('Добавлено в избранное: НКО ID', nkoId);
        // Отправка запроса на сервер для добавления в избранное
        // fetch('/api/favorites/add', { method: 'POST', body: JSON.stringify({ nko_id: nkoId }) })
    } else {
        console.log('Удалено из избранного: НКО ID', nkoId);
        // Отправка запроса на сервер для удаления из избранного
        // fetch('/api/favorites/remove', { method: 'POST', body: JSON.stringify({ nko_id: nkoId }) })
    }
}

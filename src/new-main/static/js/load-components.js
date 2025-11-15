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
            
            if (selectedCityText) {
                selectedCityText.textContent = cityName;
            }
            
            cityItems.forEach(i => i.classList.remove('selected'));
            this.classList.add('selected');
            
            if (cityBar) {
                cityBar.classList.remove('active');
            }
            if (cityToggleBtn) {
                cityToggleBtn.classList.remove('active');
            }
            
            filterContentByCity(cityValue, cityName);
            
            if (citySearch) {
                citySearch.value = '';
                cityItems.forEach(i => i.classList.remove('hidden'));
            }
        });
    });

    // Восстановление выбранного города
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

    // Закрытие при нажатии Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && cityBar && cityBar.classList.contains('active')) {
            cityBar.classList.remove('active');
            if (cityToggleBtn) {
                cityToggleBtn.classList.remove('active');
            }
        }
    });

    // Подсветка активной страницы в навигации
    highlightActivePage();
}

// Функция для подсветки активной страницы
function highlightActivePage() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href');
        if (linkPage === currentPage || (currentPage === '' && linkPage === 'index.html')) {
            link.classList.add('active');
        }
    });
}

// Функция фильтрации контента по городу
function filterContentByCity(city, cityName) {
    if (city) {
        localStorage.setItem('selectedCity', city);
        localStorage.setItem('selectedCityName', cityName);
    } else {
        localStorage.removeItem('selectedCity');
        localStorage.removeItem('selectedCityName');
    }
    console.log('Фильтрация контента для города:', city);
}

// Загрузка компонентов при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadComponent('header-placeholder', 'components/header.html');
    loadComponent('footer-placeholder', 'components/footer.html');
});

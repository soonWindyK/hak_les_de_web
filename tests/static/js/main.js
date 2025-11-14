// Переключение мобильного меню
function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    navMenu.classList.toggle('active');
}

// Переключение меню языка
function toggleLangMenu() {
    const langMenu = document.getElementById('langMenu');
    langMenu.classList.toggle('active');
}

// Закрытие меню при клике вне его
document.addEventListener('click', (e) => {
    const langSwitcher = document.querySelector('.lang-switcher');
    const langMenu = document.getElementById('langMenu');
    
    if (langSwitcher && !langSwitcher.contains(e.target)) {
        langMenu.classList.remove('active');
    }
});

// Смена языка
async function changeLanguage(lang) {
    try {
        await fetch('/api/set-lang', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ lang: lang })
        });
        
        location.reload();
    } catch (error) {
        console.error('Ошибка смены языка:', error);
    }
}

// Установка города
async function setCity(city) {
    try {
        await fetch('/api/set-city', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ city: city })
        });
        
        location.reload();
    } catch (error) {
        console.error('Ошибка установки города:', error);
    }
}

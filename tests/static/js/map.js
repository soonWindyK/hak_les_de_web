let currentLang = 'ru';
let map;
let markers = [];
let cities = [];
let translations = {};
let ymapsLoaded = false;

// Загрузка данных городов
async function loadCities(lang) {
    try {
        const response = await fetch(`/api/cities/${lang}`);
        cities = await response.json();
        console.log('Города загружены:', cities.length);
    } catch (error) {
        console.error('Ошибка загрузки городов:', error);
    }
}

// Загрузка переводов
async function loadTranslations(lang) {
    try {
        const response = await fetch(`/api/translations/${lang}`);
        translations = await response.json();
        console.log('Переводы загружены:', translations);
    } catch (error) {
        console.error('Ошибка загрузки переводов:', error);
    }
}

// Динамическая загрузка API Яндекс.Карт с нужным языком
function loadYandexMapsAPI(lang) {
    return new Promise((resolve, reject) => {
        const mapLang = lang === 'en' ? 'en_US' : 'ru_RU';
        
        // Удаляем старый скрипт если есть
        const oldScript = document.querySelector('script[src*="api-maps.yandex.ru"]');
        if (oldScript) {
            oldScript.remove();
        }
        
        // Очищаем ymaps если был загружен
        if (window.ymaps) {
            delete window.ymaps;
        }
        
        const script = document.createElement('script');
        script.src = `https://api-maps.yandex.ru/2.1/?lang=${mapLang}&load=package.full`;
        script.type = 'text/javascript';
        script.async = true;
        
        script.onload = () => {
            console.log('Яндекс.Карты загружены с языком:', mapLang);
            resolve();
        };
        
        script.onerror = () => {
            reject(new Error('Не удалось загрузить Яндекс.Карты'));
        };
        
        document.head.appendChild(script);
    });
}

// Создание карты
function createMap() {
    // Сохраняем текущий центр и зум если карта уже существует
    let currentCenter = [60, 65];
    let currentZoom = 4;
    
    if (map) {
        currentCenter = map.getCenter();
        currentZoom = map.getZoom();
        map.destroy();
        map = null;
    }
    
    // Создаём новую карту
    map = new ymaps.Map('map', {
        center: currentCenter,
        zoom: currentZoom,
        controls: ['zoomControl', 'fullscreenControl']
    });
    
    addMarkers();
}

// Инициализация карты с нужным языком
async function initMapWithLang(lang) {
    try {
        await loadYandexMapsAPI(lang);
        await loadCities(lang);
        await loadTranslations(lang);
        
        ymaps.ready(() => {
            createMap();
        });
    } catch (error) {
        console.error('Ошибка инициализации карты:', error);
    }
}

// Первая инициализация
initMapWithLang(currentLang);

// Добавление маркеров на карту
function addMarkers() {
    markers.forEach(marker => map.geoObjects.remove(marker));
    markers = [];
    
    cities.forEach(city => {
        const placemark = new ymaps.Placemark(
            city.coords,
            {
                balloonContentHeader: `<strong style="color: #0066CC; font-size: 16px;">${city.name}</strong>`,
                balloonContentBody: `
                    <p style="margin: 5px 0;"><strong>${translations.founded}:</strong> ${city.founded}</p>
                    <p style="margin: 5px 0;"><strong>${translations.population}:</strong> ${city.population}</p>
                `,
                hintContent: city.name
            },
            {
                preset: 'islands#blueCircleDotIcon',
                iconColor: '#0066CC'
            }
        );
        
        placemark.events.add('click', () => {
            showCityInfo(city);
        });
        
        map.geoObjects.add(placemark);
        markers.push(placemark);
    });
}

// Отображение информации о городе
function showCityInfo(city) {
    const cityInfoDiv = document.getElementById('cityInfo');
    cityInfoDiv.innerHTML = `
        <h4>${city.name}</h4>
        <p><strong>${translations.founded}:</strong> ${city.founded}</p>
        <p><strong>${translations.population}:</strong> ${city.population}</p>
        <p>${city.info}</p>
    `;
}

// Смена языка
async function changeLanguage(lang) {
    currentLang = lang;
    
    // Обновляем тексты интерфейса
    await loadTranslations(lang);
    
    document.getElementById('pageTitle').textContent = translations.pageTitle;
    document.getElementById('infoPanelTitle').textContent = translations.infoPanelTitle;
    document.getElementById('selectCityText').textContent = translations.selectCityText;
    document.getElementById('legendTitle').textContent = translations.legendTitle;
    document.getElementById('legendText').textContent = translations.legendText;
    document.getElementById('footerText').textContent = translations.footerText;
    document.getElementById('currentLang').textContent = translations.currentLang;
    
    document.getElementById('cityInfo').innerHTML = `<p id="selectCityText">${translations.selectCityText}</p>`;
    
    // Перезагружаем карту с новым языком
    await initMapWithLang(lang);
}

/**
 * Интерактивный календарь мероприятий
 * 
 * Функции:
 * - renderCalendar() - отрисовка календаря
 * - changeMonth(delta) - переключение месяцев
 * - selectDay(date) - выбор дня и показ мероприятий
 * - getEventsForDate(date) - получение мероприятий для даты
 */

// Глобальные переменные (инициализируются в HTML)
// eventsData, translations, currentDate, selectedDate, dayNames, monthNames

/**
 * Отрисовка календаря
 */
function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    // Обновляем заголовок
    document.getElementById('currentMonth').textContent = `${monthNames[month]} ${year}`;
    
    // Первый день месяца
    const firstDay = new Date(year, month, 1);
    // Последний день месяца
    const lastDay = new Date(year, month + 1, 0);
    
    // День недели первого дня (0 = воскресенье, нужно сделать 0 = понедельник)
    let firstDayOfWeek = firstDay.getDay();
    firstDayOfWeek = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;
    
    const daysInMonth = lastDay.getDate();
    
    // Очищаем календарь
    const grid = document.getElementById('calendarGrid');
    grid.innerHTML = '';
    
    // Добавляем заголовки дней недели
    dayNames.forEach(day => {
        const header = document.createElement('div');
        header.className = 'calendar-day-header';
        header.textContent = day;
        grid.appendChild(header);
    });
    
    // Добавляем пустые ячейки до первого дня
    for (let i = 0; i < firstDayOfWeek; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day other-month';
        grid.appendChild(emptyDay);
    }
    
    // Добавляем дни месяца
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    for (let day = 1; day <= daysInMonth; day++) {
        const date = new Date(year, month, day);
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        
        // Проверяем, сегодня ли это
        if (date.getTime() === today.getTime()) {
            dayElement.classList.add('today');
        }
        
        // Проверяем, есть ли события в этот день
        const events = getEventsForDate(date);
        if (events.length > 0) {
            dayElement.classList.add('has-events');
        }
        
        // Номер дня
        const dayNumber = document.createElement('div');
        dayNumber.className = 'day-number';
        dayNumber.textContent = day;
        dayElement.appendChild(dayNumber);
        
        // Индикаторы событий
        if (events.length > 0) {
            const indicators = document.createElement('div');
            for (let i = 0; i < Math.min(events.length, 3); i++) {
                const indicator = document.createElement('span');
                indicator.className = 'event-indicator';
                indicators.appendChild(indicator);
            }
            dayElement.appendChild(indicators);
        }
        
        // Обработчик клика
        dayElement.onclick = () => selectDay(date);
        
        grid.appendChild(dayElement);
    }
}

/**
 * Получение мероприятий для конкретной даты
 */
function getEventsForDate(date) {
    const dateStr = date.toISOString().split('T')[0];
    return eventsData.filter(event => event.date === dateStr);
}

/**
 * Переключение месяца
 */
function changeMonth(delta) {
    currentDate.setMonth(currentDate.getMonth() + delta);
    renderCalendar();
}

/**
 * Переход к сегодняшнему дню
 */
function goToToday() {
    currentDate = new Date();
    renderCalendar();
    selectDay(new Date());
}

/**
 * Выбор дня и отображение мероприятий
 */
function selectDay(date) {
    selectedDate = date;
    const events = getEventsForDate(date);
    
    const eventsList = document.getElementById('eventsList');
    const selectedDateEl = document.getElementById('selectedDate');
    const eventsContainer = document.getElementById('eventsContainer');
    
    // Форматируем дату
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    selectedDateEl.textContent = date.toLocaleDateString('ru-RU', options);
    
    if (events.length === 0) {
        eventsContainer.innerHTML = `<p>${translations.noEvents}</p>`;
    } else {
        eventsContainer.innerHTML = events.map(event => `
            <div class="event-card">
                <h3>${event.title}</h3>
                <p class="event-time">⏰ ${event.time}</p>
                <p><strong>📍 ${translations.location}:</strong> ${event.location}</p>
                ${event.city ? `<p><strong>🏙️ ${translations.city}:</strong> ${event.city}</p>` : ''}
                <p>${event.description}</p>
                <p><strong>👤 ${translations.organizer}:</strong> ${event.organizer}</p>
            </div>
        `).join('');
    }
    
    eventsList.style.display = 'block';
    eventsList.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Инициализация календаря при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    renderCalendar();
});

from flask import Flask, render_template, request, session, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Translations dictionary
translations = {
    'pl': {
        'Our Contacts': 'Nasze Kontakty',
        'Our Services': 'Nasze Usługi',
        'Our Gallery': 'Nasza Galeria',
        'Reviews': 'Opinie',
        'Call Now': 'Zadzwon',
        'Location': 'Lokalizacja i Kontakty',
        'Find Us': 'Znajdź Nas',
        'Visit Our Salon': 'Odwiedź Nasz Salon',
        'Get Directions': 'Wskazówki Dojazdu',
        'Open in Google Maps': 'Otwórz w Google Maps',
        'Parking': 'Parking',
        'Free parking available': 'Bezpłatny parking dostępny',
        'Public Transport': 'Transport Publiczny',
        'Bus stops nearby': 'Przystanki autobusowe w pobliżu',
        'Welcome to Beauty Salon': 'Witamy w Salonie Piękności',
        'Salon Name': '"CIACH CIACH I URODA"',
        'Your beauty is our passion': 'Twoje piękno jest naszą pasją',
        'Explore Services': 'Zobacz Usługi',
        'Address': 'Adres',
        'Phone': 'Telefon',
        'Email': 'E-mail',
        'Working Hours': 'Godziny Pracy',
        'Mon-Fri': 'Pon-Pt',
        'Sat-Sun': 'Sob-Nd',
        'Manicure': 'Manicure',
        'Professional nail care and beautiful designs': 'Profesjonalna pielęgnacja paznokci i piękne wzory',
        'Classic Manicure': 'Manicure Klasyczny',
        'Gel Manicure': 'Manicure Żelowy',
        'Nail Art': 'Zdobienie Paznokci',
        'Pedicure': 'Pedicure',
        'Complete foot care for health and beauty': 'Kompleksowa pielęgnacja stóp dla zdrowia i urody',
        'Classic Pedicure': 'Pedicure Klasyczny',
        'Spa Pedicure': 'Pedicure Spa',
        'Medical Pedicure': 'Pedicure Leczniczy',
        'Haircut': 'Strzyżenie',
        'Stylish haircuts and professional styling': 'Stylowe fryzury i profesjonalna stylizacja',
        'Women\'s Cut': 'Strzyżenie Damskie',
        'Men\'s Cut': 'Strzyżenie Męskie',
        'Styling': 'Stylizacja',
        'Salon Interior': 'Wnętrze Salonu',
        'Our Salon': 'Nasz Salon',
        'Hair Styling': 'Stylizacja Włosów',
        'Amazing service! The staff is professional and friendly. My nails have never looked better!': 'Niesamowita obsługa! Personel jest profesjonalny i przyjazny. Moje paznokcie nigdy nie wyglądały lepiej!',
        'Best beauty salon in Warsaw! I always leave feeling beautiful and refreshed.': 'Najlepszy salon piękności w Warszawie! Zawsze wychodzę czując się piękna i odświeżona.',
        'Professional haircuts and excellent customer service. Highly recommend!': 'Profesjonalne strzyżenie i doskonała obsługa klienta. Gorąco polecam!',
        'All rights reserved.': 'Wszelkie prawa zastrzeżone.'
    },
    'en': {
        'Our Contacts': 'Our Contacts',
        'Our Services': 'Our Services',
        'Our Gallery': 'Our Gallery',
        'Reviews': 'Reviews',
        'Call Now': 'Call Now',
        'Location': 'Location and Contacts',
        'Find Us': 'Find Us',
        'Visit Our Salon': 'Visit Our Salon',
        'Get Directions': 'Get Directions',
        'Open in Google Maps': 'Open in Google Maps',
        'Parking': 'Parking',
        'Free parking available': 'Free parking available',
        'Public Transport': 'Public Transport',
        'Bus stops nearby': 'Bus stops nearby',
        'Welcome to Beauty Salon': 'Welcome to Beauty Salon',
        'Salon Name': '"CIACH CIACH I URODA"',
        'Your beauty is our passion': 'Your beauty is our passion',
        'Explore Services': 'Explore Services',
        'Address': 'Address',
        'Phone': 'Phone',
        'Email': 'Email',
        'Working Hours': 'Working Hours',
        'Mon-Fri': 'Mon-Fri',
        'Sat-Sun': 'Sat-Sun',
        'Manicure': 'Manicure',
        'Professional nail care and beautiful designs': 'Professional nail care and beautiful designs',
        'Classic Manicure': 'Classic Manicure',
        'Gel Manicure': 'Gel Manicure',
        'Nail Art': 'Nail Art',
        'Pedicure': 'Pedicure',
        'Complete foot care for health and beauty': 'Complete foot care for health and beauty',
        'Classic Pedicure': 'Classic Pedicure',
        'Spa Pedicure': 'Spa Pedicure',
        'Medical Pedicure': 'Medical Pedicure',
        'Haircut': 'Haircut',
        'Stylish haircuts and professional styling': 'Stylish haircuts and professional styling',
        'Women\'s Cut': 'Women\'s Cut',
        'Men\'s Cut': 'Men\'s Cut',
        'Styling': 'Styling',
        'Salon Interior': 'Salon Interior',
        'Our Salon': 'Our Salon',
        'Hair Styling': 'Hair Styling',
        'Amazing service! The staff is professional and friendly. My nails have never looked better!': 'Amazing service! The staff is professional and friendly. My nails have never looked better!',
        'Best beauty salon in Warsaw! I always leave feeling beautiful and refreshed.': 'Best beauty salon in Warsaw! I always leave feeling beautiful and refreshed.',
        'Professional haircuts and excellent customer service. Highly recommend!': 'Professional haircuts and excellent customer service. Highly recommend!',
        'All rights reserved.': 'All rights reserved.'
    },
    'uk': {
        'Our Contacts': 'Наші Контакти',
        'Our Services': 'Наші Послуги',
        'Our Gallery': 'Наша Галерея',
        'Reviews': 'Відгуки',
        'Location': 'Розташування і Контакти',
        'Find Us': 'Знайдіть Нас',
        'Visit Our Salon': 'Відвідайте Наш Салон',
        'Get Directions': 'Як Дістатися',
        'Open in Google Maps': 'Відкрити в Google Maps',
        'Parking': 'Паркування',
        'Free parking available': 'Безкоштовна парковка',
        'Public Transport': 'Громадський Транспорт',
        'Bus stops nearby': 'Автобусні зупинки поруч',
        'Welcome to Beauty Salon': 'Ласкаво просимо до Салону Краси',
        'Salon Name': '"CIACH CIACH I URODA"',
        'Your beauty is our passion': 'Ваша краса - наша пристрасть',
        'Explore Services': 'Переглянути Послуги',
        'Address': 'Адреса',
        'Phone': 'Телефон',
        'Email': 'Електронна пошта',
        'Working Hours': 'Години Роботи',
        'Mon-Fri': 'Пн-Пт',
        'Sat-Sun': 'Сб-Нд',
        'Manicure': 'Манікюр',
        'Professional nail care and beautiful designs': 'Професійний догляд за нігтями та красиві дизайни',
        'Classic Manicure': 'Класичний Манікюр',
        'Gel Manicure': 'Гелевий Манікюр',
        'Nail Art': 'Дизайн Нігтів',
        'Pedicure': 'Педикюр',
        'Complete foot care for health and beauty': 'Комплексний догляд за ногами для здоров\'я та краси',
        'Classic Pedicure': 'Класичний Педикюр',
        'Spa Pedicure': 'Спа Педикюр',
        'Medical Pedicure': 'Лікувальний Педикюр',
        'Haircut': 'Стрижка',
        'Stylish haircuts and professional styling': 'Стильні стрижки та професійна укладка',
        'Women\'s Cut': 'Жіноча Стрижка',
        'Men\'s Cut': 'Чоловіча Стрижка',
        'Styling': 'Укладка',
        'Call Now': 'Подзвонити',
        'Salon Interior': 'Інтер\'єр Салону',
        'Our Salon': 'Наш Салон',
        'Hair Styling': 'Укладка Волосся',
        'Amazing service! The staff is professional and friendly. My nails have never looked better!': 'Чудовий сервіс! Персонал професійний та привітний. Мої нігті ніколи не виглядали краще!',
        'Best beauty salon in Warsaw! I always leave feeling beautiful and refreshed.': 'Найкращий салон краси у Варшаві! Я завжди виходжу, відчуваючи себе красивою та оновленою.',
        'Professional haircuts and excellent customer service. Highly recommend!': 'Професійні стрижки та відмінне обслуговування клієнтів. Дуже рекомендую!',
        'All rights reserved.': 'Всі права захищені.'
    }
}


def get_locale():
    return session.get('language', 'pl')


def get_translation(key):
    locale = get_locale()
    return translations.get(locale, {}).get(key, key)


# Make translation function available in templates
app.jinja_env.globals.update(_=get_translation)
app.jinja_env.globals.update(get_locale=get_locale)
app.jinja_env.globals.update(current_year=datetime.now().year)


@app.route('/set_language/<language>')
def set_language(language):
    if language in ['pl', 'en', 'uk']:
        session['language'] = language
    return redirect(request.referrer or '/')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    # Create CSS file
    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(open('style.css', 'r', encoding='utf-8').read() if os.path.exists('style.css') else '')

    # Create JS file
    with open('static/js/script.js', 'w', encoding='utf-8') as f:
        f.write(open('script.js', 'r', encoding='utf-8').read() if os.path.exists('script.js') else '')

    # Create HTML template
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(open('index.html', 'r', encoding='utf-8').read() if os.path.exists('index.html') else '')

    app.run(debug=True)
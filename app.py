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
        'Nail Art': 'Zdobienie Paznokci',
        'Pedicure': 'Pedicure',
        'Complete foot care for health and beauty': 'Kompleksowa pielęgnacja stóp dla zdrowia i urody',
        'Spa Pedicure': 'Pedicure Spa',
        'Haircut': 'Strzyżenie',
        'Men barber cut':                         'Strzyżenie męskie barberskie (fade, crop) – 80 zł',
        'Buzz cut':                               'Strzyżenie buzz cut – 70 zł',
        'Beard':                                  'Broda – 50 zł (z brzytwą 60 zł)',
        'Combo':                                  'Combo – 110 zł (z brzytwą 120 zł)',
        'Clipper cut (one length)':               'Strzyżenie maszynką na jedną długość – 40 zł',
        'Mens long hair haircut':                 'Strzyżenie męskie długie włosy – 100 zł',
        'Kids haircut (up to 10 years)':          'Strzyżenie dziecka do 10 lat – 60 zł',
        'Womens haircut':                         'Strzyżenie damskie – 100 zł',
        'Bangs trim':                             'Strzyżenie grzywki – 20 zł',
        'Hair ends trimming':                     'Końcówki – 50 zł',
        'Styling':                                'Modelowanie – 70 zł',
        'Curls':                                  'Loki – 100 zł',
        'Classic Manicure':                       'Manicure klasyczny – 70 zł',
        'Hybrid Manicure':                        'Manicure hybrydowy – 130 zł',
        'Gel on natural nails':                   'Żel na naturalnej płytce – 150 zł',
        'Hybrid polish removal (other stylist)':  'Ściąganie lakieru hybryd (po innej stylistce) – 10 zł',
        'Gel removal (other stylist)':            'Ściąganie żelu (po innej stylistce) – 30 zł',
        'Nail decoration':                        'Zdobienie paznokci – od 10 zł (dodatkowo)',
        'Nail repair (one nail)':                 'Naprawa jednego paznokcia – 10 zł',
        'Nail repair (2–3 fingers)':              'Naprawa paznokci (2–3 palce) – 15 zł',
        'Cosmetic pedicure':                      'Pedicure kosmetyczny – 100 zł',
        'Hybrid pedicure':                        'Pedicure hybrydowy – 150 zł',
        'Hybrid pedicure (toes only)':            'Pedicure hybryd (opracowanie tylko palców) – 130 zł',
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
        'Nail Art': 'Nail Art',
        'Pedicure': 'Pedicure',
        'Complete foot care for health and beauty': 'Complete foot care for health and beauty',
        'Haircut': 'Haircut',
        'Men barber cut':                         'Men barber cut – 80 zł',
        'Buzz cut':                               'Buzz cut – 70 zł',
        'Beard':                                  'Beard – 50 zł (z brzytwą 60 zł)',
        'Combo':                                  'Combo – 110 zł (z brzytwą 120 zł)',
        'Clipper cut (one length)':               'Clipper cut (one length) – 40 zł',
        'Mens long hair haircut':                 'Men’s long hair haircut – 100 zł',
        'Kids haircut (up to 10 years)':          'Kids’ haircut (up to 10 years) – 60 zł',
        'Womens haircut':                         'Women’s haircut – 100 zł',
        'Bangs trim':                             'Bangs trim – 20 zł',
        'Hair ends trimming':                     'Hair ends trimming – 50 zł',
        'Styling':                                'Styling – 70 zł',
        'Curls':                                  'Curls – 100 zł',
        'Classic Manicure':                       'Classic manicure – 70 zł',
        'Hybrid Manicure':                        'Hybrid manicure – 130 zł',
        'Gel on natural nails':                   'Gel on natural nails – 150 zł',
        'Hybrid polish removal (other stylist)':  'Hybrid polish removal (other stylist) – 10 zł',
        'Gel removal (other stylist)':            'Gel removal (other stylist) – 30 zł',
        'Nail decoration':                        'Nail decoration - from 10 zł',
        'Nail repair (one nail)':                 'Nail repair (one nail) – 10 zł',
        'Nail repair (2–3 fingers)':              'Nail repair (2–3 fingers) – 15 zł',
        'Cosmetic pedicure':                      'Cosmetic pedicure – 100 zł',
        'Hybrid pedicure':                        'Hybrid pedicure – 150 zł',
        'Hybrid pedicure (toes only)':            'Hybrid pedicure (toes only) – 130 zł',
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
        'Nail Art': 'Дизайн Нігтів',
        'Pedicure': 'Педикюр',
        'Complete foot care for health and beauty': 'Комплексний догляд за ногами для здоров\'я та краси',
        'Haircut': 'Стрижка',
        'Men barber cut': 'Чоловіча барбер-стрижка – 80 zł',
        'Buzz cut': 'Стрижка "buzz cut" – 70 zł',
        'Beard': 'Корекція бороди – 50 zł (з бритвою 60 zł)',
        'Combo': 'Стрижка та борода (комбо) – 110 zł (з бритвою 120 zł)',
        'Clipper cut (one length)': 'Стрижка машинкою на одну довжину – 40 zł',
        'Mens long hair haircut': 'Стрижка довге чоловіче волосся – 100 zł',
        'Kids haircut (up to 10 years)': 'Дитяча стрижка (до 10 років) – 60 zł',
        'Womens haircut': 'Жіноча стрижка – 100 zł',
        'Bangs trim': 'Підрізання чілки – 20 zł',
        'Hair ends trimming': 'Підрізання кінчиків волосся – 50 zł',
        'Styling': 'Стилізація – 70 zł',
        'Curls': 'Локони – 100 zł',
        'Classic Manicure': 'Класичний манікюр – 70 zł',
        'Hybrid Manicure': 'Гібридний манікюр – 130 zł',
        'Gel on natural nails': 'Гель на натуральні нігті – 150 zł',
        'Hybrid polish removal (other stylist)': 'Зняття гібридного лаку (іншим майстром) – 10 zł',
        'Gel removal (other stylist)': 'Зняття гелю (іншим майстром) – 30 zł',
        'Nail decoration': 'Декор нігтів – від 10 zł',
        'Nail repair (one nail)': 'Ремонт одного нігтя – 10 zł',
        'Nail repair (2–3 fingers)': 'Ремонт нігтів (2–3 пальці) – 15 zł',
        'Cosmetic pedicure': 'Косметичний педикюр – 100 zł',
        'Hybrid pedicure': 'Гібридний педикюр – 150 zł',
        'Hybrid pedicure (toes only)': 'Гібридний педикюр (тільки пальці) – 130 zł',
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

    app.run()
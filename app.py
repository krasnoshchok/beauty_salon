from flask import Flask, render_template, request, session, redirect, url_for, make_response
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-only-for-local')

# Translations dictionary
translations = {
    'pl': {
        'Our Contacts': 'Nasze Kontakty',
        'Our Services': 'Nasze Usługi',
        'Our Gallery': 'Nasza Galeria',
        'Reviews': 'Opinie',
        'Call Now': 'Zadzwon',
        'Book Online': 'Zarezerwuj',
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
        'All rights reserved.': 'Wszelkie prawa zastrzeżone.',
        'Massage': 'Masaże',
        'Relaxing and therapeutic massage treatments': 'Relaksacyjne i terapeutyczne zabiegi masażu',
        'Classic Massage': 'Masaż Klasyczny – 150/200 zł',
        'Relaxation Massage': 'Masaż relaksacyjny – 150/200 zł',
        'Lymphatic Drainage': 'Drenaż limfatyczny – 230 zł+',
        'Sports Massage': 'Masaż sportowy – 150 zł',
        'Anti-cellulite Honey Massage': 'Masaż antycellulitowy miodem – 100 zł',
        'Chinese Cupping Massage': 'Masaż bańką chińską – 90 zł',
        'Kobido Massage': 'Masaż Kobido – 200 zł',
        'Sinus Massage': 'Masaż Zatokowy – 250 zł',
        'Vagus Nerve Massage': 'Masaż Nerwu Błędnego – 250 zł+',
        'Neck and Chest': 'Szyja + Kl.piersiowa – 80 zł',
        'Cosmetic Treatments': 'Zabiegi Kosmetyczne',
        'Professional facial and beauty treatments': 'Profesjonalne zabiegi na twarz i upiększające',
        'Kobido with Algae Mask': 'Kobido + maseczka algowa – 230 zł',
        'Relaxing Facial Treatment': 'Zabieg relaksująco-pielęgnacyjny na twarz – 80 zł',
        'Eyebrow Waxing': 'Regulacja brwi woskiem – 50 zł',
        'Eyebrow Shaping and Tinting': 'Regulacja brwi + Farbowanie – 80 zł+',
        'Eyebrow Henna': 'Henna brwi – 40 zł',
        'Depilation': 'Depilacja',
        'Professional waxing and sugaring services': 'Profesjonalne usługi depilacji woskiem i pastą cukrową',
        'Full Legs Waxing': 'Depilacja nogi - całość – 120 zł+',
        'Half Legs Waxing': 'Depilacja nogi - połowa – 80 zł',
        'Full Arms Waxing': 'Depilacja ręce - całość – 90 zł+',
        'Half Arms Waxing': 'Depilacja ręce - połowa – 60 zł',
        'Underarms Waxing': 'Depilacja pachy – 40 zł+',
        'Upper Lip Waxing': 'Depilacja wąsik – 40 zł+'
    },
    'en': {
        'Our Contacts': 'Our Contacts',
        'Our Services': 'Our Services',
        'Our Gallery': 'Our Gallery',
        'Reviews': 'Reviews',
        'Call Now': 'Call Now',
        'Book Online': 'Book Online',
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
        'All rights reserved.': 'All rights reserved.',
        'Massage': 'Massage',
        'Relaxing and therapeutic massage treatments': 'Relaxing and therapeutic massage treatments',
        'Classic Massage': 'Classic Massage – 150/200 zł',
        'Relaxation Massage': 'Relaxation Massage – 150/200 zł',
        'Lymphatic Drainage': 'Lymphatic Drainage – 230 zł',
        'Sports Massage': 'Sports Massage – 150 zł',
        'Anti-cellulite Honey Massage': 'Anti-cellulite Honey Massage – 100 zł',
        'Chinese Cupping Massage': 'Chinese Cupping Massage – 90 zł',
        'Kobido Massage': 'Kobido Massage – 200 zł',
        'Sinus Massage': 'Sinus Massage – 250 zł+',
        'Vagus Nerve Massage': 'Vagus Nerve Massage – 250 zł',
        'Neck and Chest': 'Neck and Chest – 80 zł',
        'Cosmetic Treatments': 'Cosmetic Treatments',
        'Professional facial and beauty treatments': 'Professional facial and beauty treatments',
        'Kobido with Algae Mask': 'Kobido with Algae Mask – 230 zł',
        'Relaxing Facial Treatment': 'Relaxing Facial Treatment – 80/150 zł',
        'Eyebrow Waxing': 'Eyebrow Waxing – 50 zł',
        'Eyebrow Shaping and Tinting': 'Eyebrow Shaping and Tinting – 80 zł',
        'Eyebrow Henna': 'Eyebrow Henna – 40 zł',
        'Depilation': 'Depilation',
        'Professional waxing and sugaring services': 'Professional waxing and sugaring services',
        'Full Legs Waxing': 'Full Legs Waxing – 120 zł+',
        'Half Legs Waxing': 'Half Legs Waxing – 80 zł',
        'Full Arms Waxing': 'Full Arms Waxing – 90 zł+',
        'Half Arms Waxing': 'Half Arms Waxing – 60 zł',
        'Underarms Waxing': 'Underarms Waxing – 40 zł+',
        'Upper Lip Waxing': 'Upper Lip Waxing – 40 zł+'
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
        'Book Online': 'Забронювати',
        'Salon Interior': 'Інтер\'єр Салону',
        'Our Salon': 'Наш Салон',
        'Hair Styling': 'Укладка Волосся',
        'All rights reserved.': 'Всі права захищені.',
        'Massage': 'Масаж',
        'Relaxing and therapeutic massage treatments': 'Релаксаційні та терапевтичні масажні процедури',
        'Classic Massage': 'Класичний масаж – 150/200 zł',
        'Relaxation Massage': 'Релаксаційний масаж – 150/200 zł',
        'Lymphatic Drainage': 'Лімфодренаж – 230 zł',
        'Sports Massage': 'Спортивний масаж – 150 zł',
        'Anti-cellulite Honey Massage': 'Антицелюлітний медовий масаж – 100 zł',
        'Chinese Cupping Massage': 'Масаж китайськими банками – 90 zł',
        'Kobido Massage': 'Масаж Кобідо – 200 zł',
        'Sinus Massage': 'Масаж пазух – 250 zł',
        'Vagus Nerve Massage': 'Масаж блукаючого нерва – 250 zł+',
        'Neck and Chest': 'Шия та груди – 80 zł',
        'Cosmetic Treatments': 'Косметичні процедури',
        'Professional facial and beauty treatments': 'Професійні процедури для обличчя та краси',
        'Kobido with Algae Mask': 'Кобідо з альгінатною маскою – 230 zł',
        'Relaxing Facial Treatment': 'Релаксуюча процедура для обличчя – 80/150 zł',
        'Eyebrow Waxing': 'Корекція брів воском – 50 zł',
        'Eyebrow Shaping and Tinting': 'Корекція та фарбування брів – 80 zł',
        'Eyebrow Henna': 'Хна для брів – 40 zł',
        'Depilation': 'Депіляція',
        'Professional waxing and sugaring services': 'Професійні послуги воскової та цукрової депіляції',
        'Full Legs Waxing': 'Депіляція ніг повністю – 120 zł+',
        'Half Legs Waxing': 'Депіляція половини ніг – 80 zł',
        'Full Arms Waxing': 'Депіляція рук повністю – 90 zł+',
        'Half Arms Waxing': 'Депіляція половини рук – 60 zł',
        'Underarms Waxing': 'Депіляція пахв – 40 zł+',
        'Upper Lip Waxing': 'Депіляція верхньої губи – 40 zł+'
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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_language/<language>')
def set_language(language):
    if language in ['pl', 'en', 'uk']:
        session['language'] = language
    return redirect(request.referrer or '/')


@app.route('/sitemap.xml')
def sitemap():
    pages = []
    languages = ['pl', 'en', 'uk']
    for lang in languages:
        pages.append({
            'loc': url_for('index', _external=True, lang=lang),
            'lastmod': datetime.now().strftime('%Y-%m-%d'),
            'priority': '1.0'
        })

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Add caching
from flask import send_from_directory
@app.route('/static/<path:path>')
def send_static(path):
    response = send_from_directory('static', path)
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

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

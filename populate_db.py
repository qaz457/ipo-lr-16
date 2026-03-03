# populate_db.py
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from myapp.models import ProductCategory, Manufacturer, Product, Cart, CartItem

def populate():
    print("Очистка старых данных...")
    CartItem.objects.all().delete()
    Cart.objects.all().delete()
    Product.objects.all().delete()
    ProductCategory.objects.all().delete()
    Manufacturer.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    print("Старые данные удалены.")

    print("Создание производителей (5 шт.)...")
    man1 = Manufacturer.objects.create(name="Hasbro", country="США", description="Крупнейший в мире производитель игрушек и настольных игр.")
    man2 = Manufacturer.objects.create(name="Hobby World", country="Россия", description="Ведущий издатель и локализатор настольных игр в России.")
    man3 = Manufacturer.objects.create(name="Asmodee", country="Франция", description="Мировой лидер в издании и дистрибуции настольных игр.")
    man4 = Manufacturer.objects.create(name="Zvezda", country="Россия", description="Известный производитель сборных моделей и настольных игр.")
    man5 = Manufacturer.objects.create(name="GaGa Games", country="Россия", description="Издательство, специализирующееся на веселых и семейных играх.")
    manufacturers = [man1, man2, man3, man4, man5]
    print("Производители созданы.")

    print("Создание категорий (10 шт.)...")
    cat1 = ProductCategory.objects.create(name="Стратегии", description="Игры, требующие продуманного планирования и тактики.")
    cat2 = ProductCategory.objects.create(name="Семейные", description="Игры для всех возрастов, с простыми правилами.")
    cat3 = ProductCategory.objects.create(name="Для вечеринок", description="Игры, в которых главное — общение и веселье.")
    cat4 = ProductCategory.objects.create(name="Детские", description="Развивающие и развлекательные игры для самых маленьких.")
    cat5 = ProductCategory.objects.create(name="Карточные", description="Игры, в которых основным компонентом являются карты.")
    cat6 = ProductCategory.objects.create(name="Кооперативные", description="Игроки объединяются для победы над самой игрой.")
    cat7 = ProductCategory.objects.create(name="Головоломки", description="Игры на логику и пространственное мышление.")
    cat8 = ProductCategory.objects.create(name="Варгеймы", description="Игры, симулирующие военные действия или противостояния.")
    cat9 = ProductCategory.objects.create(name="Экономические", description="Игры про управление ресурсами и финансами.")
    cat10 = ProductCategory.objects.create(name="Приключения", description="Игры с сюжетом и исследованием мира.")
    categories = [cat1, cat2, cat3, cat4, cat5, cat6, cat7, cat8, cat9, cat10]
    print("Категории созданы.")

    print("Создание товаров (34 шт.)...")

    products_data = [
        {'name': '7 Wonders', 'price': '94.01', 'category': cat1, 'manufacturer': man3, 'stock': 10, 'description': 'Карточная стратегия за 30 минут.'},
        {'name': 'Ticket to Ride', 'price': '86.10', 'category': cat2, 'manufacturer': man2, 'stock': 5, 'description': 'Хит. Путешествуйте по железным дорогам.'},
        {'name': 'Каркассон', 'price': '86.10', 'category': cat1, 'manufacturer': man2, 'stock': 7, 'description': 'Легендарная игра про средневековье.'},
        {'name': 'Кодовые имена', 'price': '34.95', 'category': cat3, 'manufacturer': man1, 'stock': 15, 'description': 'Игра для компании на ассоциации.'},
        {'name': 'Имаджинариум', 'price': '40.29', 'category': cat3, 'manufacturer': man5, 'stock': 12, 'description': 'Скидка! Игра в ассоциации с красочными картами.'},
        {'name': 'Манчкин', 'price': '38.70', 'category': cat5, 'manufacturer': man4, 'stock': 8, 'description': 'Пародийная карточная RPG.'},
        {'name': 'Бэнг!', 'price': '25.50', 'category': cat5, 'manufacturer': man3, 'stock': 20, 'description': 'Карточная игра про Дикий Запад.'},
        {'name': 'D&D Стартовый набор', 'price': '70.00', 'category': cat9, 'manufacturer': man1, 'stock': 3, 'description': 'Предзаказ. Начните свое приключение.'},
        {'name': 'Колонизаторы', 'price': '58.30', 'category': cat1, 'manufacturer': man2, 'stock': 6, 'description': 'Классическая экономическая стратегия.'},
        {'name': 'Монополия', 'price': '45.00', 'category': cat9, 'manufacturer': man1, 'stock': 25, 'description': 'Самая известная экономическая игра.'},
        {'name': 'Активити', 'price': '52.90', 'category': cat3, 'manufacturer': man1, 'stock': 11, 'description': 'Игра на объяснение слов.'},
        {'name': 'Дженга', 'price': '22.40', 'category': cat2, 'manufacturer': man4, 'stock': 30, 'description': 'Игра на ловкость рук.'},
        {'name': 'UNO', 'price': '15.90', 'category': cat5, 'manufacturer': man1, 'stock': 100, 'description': 'Быстрая карточная игра.'},
        {'name': 'Скрабл', 'price': '65.80', 'category': cat2, 'manufacturer': man4, 'stock': 9, 'description': 'Игра в слова.'},
        {'name': 'Шакал', 'price': '47.50', 'category': cat1, 'manufacturer': man5, 'stock': 4, 'description': 'Стратегия про пиратов и сокровища.'},
        {'name': 'Эволюция', 'price': '55.20', 'category': cat1, 'manufacturer': man2, 'stock': 13, 'description': 'Развивайте своих существ.'},
        {'name': 'Свинтус', 'price': '20.10', 'category': cat3, 'manufacturer': man2, 'stock': 22, 'description': 'Веселая карточная игра.'},
        {'name': 'Делиссимо', 'price': '39.90', 'category': cat4, 'manufacturer': man5, 'stock': 18, 'description': 'Детская игра про пиццу.'},
        {'name': 'Лабиринт', 'price': '32.30', 'category': cat7, 'manufacturer': man3, 'stock': 16, 'description': 'Игра-головоломка с движущимися стенами.'},
        {'name': 'Морской бой', 'price': '18.00', 'category': cat8, 'manufacturer': man4, 'stock': 27, 'description': 'Классическая игра на бумаге в коробке.'},
        {'name': 'Пандемия', 'price': '75.40', 'category': cat6, 'manufacturer': man3, 'stock': 5, 'description': 'Кооперативная игра про спасение мира.'},
        {'name': 'Ужас Аркхэма', 'price': '110.00', 'category': cat9, 'manufacturer': man3, 'stock': 2, 'description': 'Сложная кооперативная игра по Лавкрафту.'},
        {'name': 'Взрывные котята', 'price': '29.90', 'category': cat3, 'manufacturer': man5, 'stock': 14, 'description': 'Русская рулетка для вечеринок.'},
        {'name': 'Зомби в доме', 'price': '42.50', 'category': cat6, 'manufacturer': man4, 'stock': 19, 'description': 'Кооперативная игра про зомби.'},
        {'name': 'Сумерки Империи', 'price': '200.00', 'category': cat1, 'manufacturer': man3, 'stock': 1, 'description': 'Эпичная стратегия на весь день.'},
        {'name': 'Подземелье', 'price': '33.80', 'category': cat5, 'manufacturer': man2, 'stock': 17, 'description': 'Карточная игра про героев и монстров.'},
        {'name': 'Кортекс', 'price': '27.60', 'category': cat4, 'manufacturer': man1, 'stock': 21, 'description': 'Битва на скорость мышления.'},
        {'name': 'Спящие королевы', 'price': '24.90', 'category': cat4, 'manufacturer': man5, 'stock': 23, 'description': 'Детская стратегия про королей и queens.'},
        {'name': 'Диксит', 'price': '48.90', 'category': cat3, 'manufacturer': man2, 'stock': 10, 'description': 'Игра на ассоциации по картинкам.'},
        {'name': 'Цитадели', 'price': '28.40', 'category': cat1, 'manufacturer': man3, 'stock': 31, 'description': 'Карточная игра про строительство города.'},
        {'name': 'Билет на поезд: Европа', 'price': '92.50', 'category': cat1, 'manufacturer': man2, 'stock': 4, 'description': 'Самостоятельная версия хита.'},
        {'name': 'Медвед', 'price': '21.90', 'category': cat5, 'manufacturer': man5, 'stock': 26, 'description': 'Простая и веселая карточная игра.'},
        {'name': 'Халли Галли', 'price': '23.70', 'category': cat4, 'manufacturer': man1, 'stock': 24, 'description': 'Детская игра на реакцию.'},
        {'name': 'Коварный волк', 'price': '35.60', 'category': cat3, 'manufacturer': man2, 'stock': 28, 'description': 'Игра в мафию в современном формате.'},
    ]

    for data in products_data:
        Product.objects.create(
            name=data['name'],
            description=data['description'],
            image='photos/default.jpg',
            price=Decimal(data['price']),
            stock=data['stock'],
            category=data['category'],
            manufacturer=data['manufacturer']
        )
    print("34 товара создано.")

    print("Создание пользователей (5 шт.) и их корзин...")
    users = []
    for i in range(1, 6):
        user = User.objects.create_user(
            username=f'user{i}',
            email=f'user{i}@example.com',
            password=f'password{i}'
        )
        users.append(user)
        print(f"  Пользователь {user.username} создан.")

        cart = Cart.objects.create(user=user)
        print(f"  Корзина для {user.username} создана.")

        products_in_cart = Product.objects.all().order_by('?')[:3]
        for product in products_in_cart:
            quantity = min(2, product.stock)
            if quantity > 0:
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity
                )
                print(f"    В корзину добавлен товар: {product.name} ({quantity} шт.)")
    print("Пользователи и корзины созданы.")

    print("-" * 30)
    print("Наполнение базы данных успешно завершено!")
    print(f"Создано: Производителей: 5, Категорий: 10, Товаров: 34, Пользователей: 5 с корзинами.")

if __name__ == '__main__':
    populate()
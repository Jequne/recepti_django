from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recipes_site.recipes.models import Recipe

class Command(BaseCommand):
    help = 'Добавить тестовые рецепты и пользователей'

    def handle(self, *args, **kwargs):
        # Создать пользователей
        user1, _ = User.objects.get_or_create(username='ivan', defaults={'email': 'ivan@example.com'})
        user1.set_password('testpass123')
        user1.save()
        user2, _ = User.objects.get_or_create(username='anna', defaults={'email': 'anna@example.com'})
        user2.set_password('testpass123')
        user2.save()

        # Тестовые рецепты
        recipes = [
            {
                'title': 'Паста Карбонара',
                'description': 'Классическая итальянская паста с беконом и сливочным соусом.',
                'full_text': 'Паста Карбонара — это сливочный вкус, бекон и сыр пармезан.',
                'ingredients': 'Паста — 200 г\nБекон — 100 г\nЯйцо — 2 шт\nСливки — 100 мл\nПармезан — 50 г',
                'steps': '1. Отварить пасту.\n2. Обжарить бекон.\n3. Смешать яйца и сливки.\n4. Соединить всё и добавить сыр.'
            },
            {
                'title': 'Омлет с сыром',
                'description': 'Пышный омлет с добавлением сыра.',
                'full_text': 'Омлет с сыром — быстрый и вкусный завтрак.',
                'ingredients': 'Яйцо — 3 шт\nМолоко — 50 мл\nСыр — 40 г\nМасло — 10 г',
                'steps': '1. Взбить яйца с молоком.\n2. Вылить на сковороду.\n3. Посыпать сыром.\n4. Готовить под крышкой.'
            },
            {
                'title': 'Блины',
                'description': 'Тонкие домашние блины на молоке.',
                'full_text': 'Блины — универсальное блюдо для завтрака или десерта.',
                'ingredients': 'Молоко — 300 мл\nЯйцо — 2 шт\nМука — 150 г\nСахар — 1 ст.л.\nСоль — щепотка',
                'steps': '1. Смешать все ингредиенты.\n2. Жарить на сковороде с двух сторон.'
            },
            {
                'title': 'Салат Цезарь',
                'description': 'Лёгкий салат с курицей, сухариками и соусом.',
                'full_text': 'Салат Цезарь — популярное блюдо с оригинальным соусом.',
                'ingredients': 'Курица — 150 г\nСалат — 100 г\nСухарики — 30 г\nПармезан — 20 г\nСоус Цезарь — 30 г',
                'steps': '1. Обжарить курицу.\n2. Нарезать салат.\n3. Смешать ингредиенты и добавить соус.'
            },
            {
                'title': 'Шоколадный торт',
                'description': 'Нежный торт с шоколадным кремом.',
                'full_text': 'Шоколадный торт — идеальный десерт для сладкоежек.',
                'ingredients': 'Мука — 200 г\nКакао — 50 г\nЯйцо — 3 шт\nСахар — 150 г\nМолоко — 100 мл',
                'steps': '1. Смешать сухие ингредиенты.\n2. Добавить яйца и молоко.\n3. Выпекать 30 минут.'
            },
        ]
        for i, data in enumerate(recipes):
            Recipe.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description': data['description'],
                    'full_text': data['full_text'],
                    'ingredients': data['ingredients'],
                    'steps': data['steps'],
                    'author': user1 if i % 2 == 0 else user2
                }
            )
        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно добавлены!'))

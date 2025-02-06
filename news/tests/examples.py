# news/tests/examples.py
from django.test import TestCase

# Импортируем модель, чтобы работать с ней в тестах.
from news.models import News


# Создаём тестовый класс с произвольным названием, наследуем его от TestCase.
class TestNews(TestCase):
    # Все нужные переменные сохраняем в атрибуты класса.
    TITLE = 'Заголовок новости'
    TEXT = 'Тестовый текст'

    # В методе класса setUpTestData создаём тестовые объекты.
    # Оборачиваем метод соответствующим декоратором.
    @classmethod
    def setUpTestData(cls):
        # Стандартным методом Django ORM create() создаём объект класса.
        # Присваиваем объект атрибуту класса: назовём его news.
        cls.news = News.objects.create(
            # При создании объекта обращаемся к константам класса через cls.
            title=cls.TITLE,
            text=cls.TEXT,
        )

    # Проверим, что объект действительно был создан.
    def test_successful_creation(self):
        # При помощи обычного ORM-метода посчитаем количество записей в базе.
        news_count = News.objects.count()
        # Сравним полученное число с единицей.
        self.assertEqual(news_count, 1)

    def test_title(self):
        # Сравним свойство объекта и ожидаемое значение.
        # Чтобы проверить равенство с константой -
        # обращаемся к ней через self, а не через cls:
        self.assertEqual(self.news.title, self.TITLE)


"""
При тестировании можно создать несколько клиентов: в одном можно 
авторизоваться, а из другого клиента работать без авторизации, тестируя 
сценарии для анонимных пользователей. При этом в каждом тестирующем классе 
будет доступен и клиент, созданный автоматически.
"""
# Импортируем функцию для определения модели пользователя.
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
# Получаем модель пользователя.

User = get_user_model()


class TestNews(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаём пользователя.
        cls.user = User.objects.create(username='testUser')
        # Создаём объект клиента.
        cls.user_client = Client()
        # "Логинимся" в клиенте при помощи метода force_login().
        cls.user_client.force_login(cls.user)
        # Теперь через этот клиент можно отправлять запросы
        # от имени пользователя с логином "testUser".

"""
В ответ на любой запрос, отправленный через клиент, возвращается специальный 
объект класса Response. В нём содержится ответ сервера и дополнительная 
информация. Стоит обратить внимание на следующие атрибуты:
response.status_code — содержит код ответа запрошенного адреса;
response.content — данные ответа в виде строки байтов;
response.context — словарь переменных, переданный для отрисовки шаблона при 
вызове функции render();
response.templates — перечень шаблонов, вызванных для отрисовки запрошенной 
страницы;
"""
class TestRoutes(TestCase):

    def test_home_page(self):
        # Вызываем метод get для клиента (self.client)
        # и загружаем главную страницу.
        response = self.client.get('/')
        # Проверяем, что код ответа равен 200.
        self.assertEqual(response.status_code, 200)
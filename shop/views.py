from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    """Главная страница"""
    return HttpResponse("""
    <h1>Добро пожаловать в plantcare shop</h1>
    <p>ваш магазин товаров ухада за комнатными растениями</p>
    <ul>
        <li><a href="/about/">О магазине</a></li>
        <li><a href="/author/">Об авторе</a></li>
    </ul>
    """)
def about_shop(request):
    """Страница о магазине"""
    return HttpResponse("""
    <h1>О нашем магазине</h1>
    <p>Тема Магазин товаров для ухода за комнатными растениями (лейки, удобрения).</p>
    """)
def about_author(request):
    """Страница об авторе"""
    return HttpResponse("""
    <p>Лабараторную сделал Рубцов Петр Группа 89 ТП</p>
    
    """)
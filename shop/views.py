from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category, Manufacturer, Cart, CartItem

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


def catalog(request):
    products = Product.objects.all()
    

    category = request.GET.get('category')
    manufacturer = request.GET.get('manufacturer')
    search = request.GET.get('search')
    
    if category:
        products = products.filter(category_id=category)
    if manufacturer:
        products = products.filter(manufacturer_id=manufacturer)
    if search:
        products = products.filter(Q(nameicontains=search) | Q(descriptionicontains=search))
    
    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': Category.objects.all(),
        'manufacturers': Manufacturer.objects.all(),
    })

def product_detail(request, pk):
    return render(request, 'shop/product_detail.html', {
        'product': get_object_or_404(Product, id=pk)
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'quantity': 1}  
    )

    if not created and item.quantity < product.stock:
        item.quantity += 1
        item.save()

    return redirect('cart_detail')

@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        if qty > 0 and qty <= item.product.stock:
            item.quantity = qty
            item.save()
        elif qty <= 0:
            item.delete()
    
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    get_object_or_404(CartItem, id=item_id, cart__user=request.user).delete()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'shop/cart_detail.html', {
        'cart': cart,
        'items': cart.cartitem_set.all()
    })
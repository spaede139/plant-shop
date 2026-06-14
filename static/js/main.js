
function showNotification(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
    }
    

    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

function addToCartAPI(productId, quantity = 1) {

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                      document.cookie.match(/csrftoken=([^;]+)/)?.[1];
    

    const button = event?.target;
    const originalText = button?.innerHTML;
    if (button) {
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Загрузка...';
        button.disabled = true;
    }
    
    fetch('/api/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (button) {
            button.innerHTML = originalText;
            button.disabled = false;
        }
        
        if (data.success || data.status === 'success') {
            showNotification('Товар добавлен в корзину!', 'success');
     
            updateCartCount();
        } else {
            showNotification(data.message || 'Ошибка при добавлении', 'danger');
        }
    })
    .catch(error => {
        if (button) {
            button.innerHTML = originalText;
            button.disabled = false;
        }
        console.error('Ошибка:', error);
        showNotification('Ошибка соединения с сервером', 'danger');
    });
}


function updateCartCount() {
    fetch('/api/cart-count/')
        .then(response => response.json())
        .then(data => {
            const cartBadge = document.getElementById('cart-count');
            if (cartBadge && data.count > 0) {
                cartBadge.textContent = data.count;
                cartBadge.style.display = 'inline';
            } else if (cartBadge) {
                cartBadge.style.display = 'none';
            }
        })
        .catch(error => console.error('Ошибка:', error));
}


function loadProductsAPI(filters = {}) {
    let url = '/api/products/';
    const params = new URLSearchParams(filters);
    if (params.toString()) {
        url += '?' + params.toString();
    }
    

    const productsContainer = document.getElementById('products-container');
    if (productsContainer) {
        productsContainer.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-success" role="status">
                    <span class="visually-hidden">Загрузка...</span>
                </div>
                <p class="mt-2">Загрузка товаров...</p>
            </div>
        `;
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            displayProducts(data);
        })
        .catch(error => {
            console.error('Ошибка:', error);
            if (productsContainer) {
                productsContainer.innerHTML = `
                    <div class="alert alert-danger">
                        Ошибка загрузки товаров. Попробуйте позже.
                    </div>
                `;
            }
        });
}


function displayProducts(products) {
    const container = document.getElementById('products-container');
    if (!container) return;
    
    if (!products.length) {
        container.innerHTML = '<div class="alert alert-info">Товаров не найдено</div>';
        return;
    }
    
    let html = '<div class="row">';
    products.forEach(product => {
        html += `
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                    <div class="card-img-top bg-light text-center py-4">
                        <i class="fas fa-leaf fa-3x text-success"></i>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">${product.name}</h5>
                        <p class="card-text text-success fw-bold">${product.price} руб.</p>
                        <a href="/catalog/${product.id}/" class="btn btn-outline-success btn-sm">Подробнее</a>
                    </div>
                </div>
            </div>
        `;
    });
    html += '</div>';
    container.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            addToCartAPI(productId);
        });
    });
});
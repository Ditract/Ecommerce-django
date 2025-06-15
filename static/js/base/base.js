document.addEventListener('DOMContentLoaded', () => {
  initCartUI();
  initUserDropdown();
  initFlashMessageFadeout();
});

// -------------------
// Inicialización del carrito
// -------------------
function initCartUI() {
  const cartBtn = document.querySelector('.cart-btn');
  const cartSidebar = document.getElementById('cartSidebar');
  const cartOverlay = document.getElementById('cartOverlay');
  const closeCartBtn = document.querySelector('.close-cart-btn');

  if (!cartBtn || !cartSidebar || !cartOverlay || !closeCartBtn) return;

  cartBtn.addEventListener('click', () => {
    cartSidebar.classList.add('open');
    cartOverlay.classList.add('show');
    loadCartContent();
  });

  closeCartBtn.addEventListener('click', closeCart);
  cartOverlay.addEventListener('click', closeCart);

  // Cerrar el carrito
  function closeCart() {
    cartSidebar.classList.remove('open');
    cartOverlay.classList.remove('show');
  }

  // Agregar producto desde botón
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('add-to-cart')) {
      e.preventDefault();
      const url = e.target.href;

      fetch(url, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            loadCartContent();
            updateCartBadge(data.cart_items);
            cartSidebar.classList.add('open');
            cartOverlay.classList.add('show');
          } else {
            alert(data.error || 'No se pudo agregar al carrito.');
          }
        })
        .catch(error => {
          console.error('Error adding to cart:', error);
        });
    }
  });
}

// -------------------
// Cargar contenido dinámico del carrito
// -------------------
function loadCartContent() {
  fetch(cartDetailUrl, {
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  })
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return response.text();
    })
    .then(html => {
      const container = document.querySelector('.cart-sidebar-content');
      if (container) {
        container.innerHTML = html;
        attachEventListeners(); // <- Importante: volver a enlazar eventos
      }
    })
    .catch(error => {
      console.error('Error loading cart content:', error);
      const container = document.querySelector('.cart-sidebar-content');
      if (container) {
        container.innerHTML = '<p>Error al cargar el carrito.</p>';
      }
    });
}

// -------------------
// Actualizar/eliminar ítems del carrito
// -------------------
function attachEventListeners() {
  const updateForms = document.querySelectorAll('.cart-update-form');
  const removeLinks = document.querySelectorAll('.remove-item');

  updateForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      const itemId = form.dataset.itemId;

      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(response => response.json())
        .then(data => {
          const errorBox = document.getElementById(`cartError-${itemId}`);

          if (data.success) {
            if (errorBox) {
              errorBox.innerHTML = '';
              errorBox.style.display = 'none';
            }
            loadCartContent();
            updateCartBadge(data.cart_items);
          } else if (data.error && errorBox) {
            errorBox.innerHTML = `
              <div class="user-message">
                <p class="alert error">${data.error}</p>
              </div>
            `;
            errorBox.style.display = 'block';

            setTimeout(() => {
              errorBox.innerHTML = '';
              errorBox.style.display = 'none';
            }, 4000);
          }
        })
        .catch(error => {
          console.error('Error updating cart:', error);
        });
    });
  });

  removeLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      fetch(link.href, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            loadCartContent();
            updateCartBadge(data.cart_items);
          }
        })
        .catch(error => {
          console.error('Error removing item:', error);
        });
    });
  });
}

// -------------------
// Actualizar badge de ítems del carrito
// -------------------
function updateCartBadge(itemCount) {
  const badge = document.querySelector('.cart-badge');
  if (badge) {
    badge.textContent = itemCount;
  }
}

// -------------------
//  Dropdown de usuario
// -------------------
function initUserDropdown() {
  const userBtn = document.querySelector('.user-btn');
  const menu = document.getElementById('userMenu');

  if (!userBtn || !menu) return;

  userBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    menu.classList.toggle('hidden');
  });

  document.addEventListener('click', (event) => {
    if (!userBtn.contains(event.target) && !menu.contains(event.target)) {
      menu.classList.add('hidden');
    }
  });
}

// -------------------
// Desvanecer mensajes de Django
// -------------------
function initFlashMessageFadeout() {
  const userMessage = document.querySelector('.user-message');
  if (userMessage) {
    setTimeout(() => {
      userMessage.classList.add('fade-out');
      setTimeout(() => {
        userMessage.style.display = 'none';
      }, 500);
    }, 3000);
  }
}

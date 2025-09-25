document.addEventListener('DOMContentLoaded', () => {
  initCartUI();
});

// -------------------
// Inicialización del carrito
// -------------------
function initCartUI() {
  const cartSidebar = document.getElementById('cartSidebar');
  const cartOverlay = document.getElementById('cartOverlay');

  if (!cartSidebar || !cartOverlay) return;

  // Cargar contenido inicial del carrito y badge
  loadCartContent();

  // Escucha el botón del carrito para abrirlo manualmente
  const cartButton = document.querySelector('.cart-btn, .cart-icon');
  if (cartButton) {
    cartButton.addEventListener('click', () => {
      loadCartContent();
      openCart();
    });
  }

  // Escucha los formularios de "Agregar al carrito"
  const addForms = document.querySelectorAll('.cart-add-form, .form-agregar-carrito');
  addForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = new FormData(form);

      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            loadCartContent();
            updateCartBadge(data.cart_items);

            if (data.cart_items === 1) {
              openCart();
            } else {
              showToast("Producto agregado al carrito");
            }
          } else {
            showToast(data.error || "No se pudo agregar al carrito", true);
          }
        })
        .catch(error => {
          console.error("Error agregando al carrito:", error);
          showToast("Error al agregar al carrito", true);
        });
    });
  });

  // Cerrar carrito al hacer click en overlay o botón de cerrar
  cartOverlay.addEventListener('click', closeCart);
  const closeBtn = cartSidebar.querySelector('.close-cart-btn');
  if (closeBtn) closeBtn.addEventListener('click', closeCart);
}

// -------------------
// Helpers: abrir/cerrar carrito
// -------------------
function openCart() {
  const cartSidebar = document.getElementById('cartSidebar');
  const cartOverlay = document.getElementById('cartOverlay');
  if (cartSidebar) cartSidebar.classList.add('open');
  if (cartOverlay) cartOverlay.classList.add('show');
}

function closeCart() {
  const cartSidebar = document.getElementById('cartSidebar');
  const cartOverlay = document.getElementById('cartOverlay');
  if (cartSidebar) cartSidebar.classList.remove('open');
  if (cartOverlay) cartOverlay.classList.remove('show');
}

// -------------------
// Cargar contenido dinámico del carrito
// -------------------
function loadCartContent() {
  fetch(cartDetailUrl, {
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return response.text();
    })
    .then(html => {
      const container = document.querySelector('.cart-sidebar-content');
      if (container) {
        container.innerHTML = html;

        // ✅ Obtener el número de items distintos desde el HTML parcial
        const cartWrapper = container.querySelector('[data-cart-items]');
        if (cartWrapper) {
          const distinctItems = parseInt(cartWrapper.dataset.cartItems, 10) || 0;
          updateCartBadge(distinctItems);
        }

        attachEventListeners(); // volver a enlazar eventos dinámicos
      }
    })
    .catch(error => {
      console.error('Error cargando contenido del carrito:', error);
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
  const removeButtons = document.querySelectorAll('.remove-item-btn');

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

            const quantityInput = form.querySelector('.cart-quantity-input');
            if (quantityInput && quantityInput.dataset.originalValue) {
              quantityInput.value = quantityInput.dataset.originalValue;
            }

            setTimeout(() => {
              errorBox.innerHTML = '';
              errorBox.style.display = 'none';
            }, 5000);
          }
        })
        .catch(error => {
          console.error('Error actualizando carrito:', error);
        });
    });
  });

  removeButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      e.preventDefault();
      const url = button.dataset.url;

      fetch(url, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            loadCartContent();
            updateCartBadge(data.cart_items);
            showToast("Producto eliminado del carrito");
          }
        })
        .catch(error => {
          console.error('Error eliminando ítem del carrito:', error);
          showToast("Error eliminando el producto", true);
        });
    });
  });
}

// -------------------
// Actualizar badge de ítems del carrito
// -------------------
function updateCartBadge(itemCount) {
  const badge = document.querySelector('.cart-badge');
  if (!badge) return;

  if (itemCount > 0) {
    badge.textContent = itemCount;
    badge.style.display = 'inline-block';
  } else {
    badge.style.display = 'none';
  }
}

// -------------------
// Toast de notificaciones
// -------------------
function showToast(message, isError = false) {
  const toast = document.getElementById('toast');
  if (!toast) return;

  toast.textContent = message;
  toast.classList.add('show');
  toast.classList.toggle('error', isError);

  setTimeout(() => {
    toast.classList.remove('show', 'error');
  }, 3000);
}

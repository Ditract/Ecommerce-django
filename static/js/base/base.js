document.addEventListener('DOMContentLoaded', () => {
  const cartBtn = document.querySelector('.cart-btn');
  const cartSidebar = document.getElementById('cartSidebar');
  const cartOverlay = document.getElementById('cartOverlay');
  const closeCartBtn = document.querySelector('.close-cart-btn');

  // Abrir/cerrar carrito
  cartBtn.addEventListener('click', () => {
    cartSidebar.classList.add('open');
    cartOverlay.classList.add('show');
    loadCartContent();
  });

  closeCartBtn.addEventListener('click', closeCart);
  cartOverlay.addEventListener('click', closeCart);

  function closeCart() {
    cartSidebar.classList.remove('open');
    cartOverlay.classList.remove('show');
  }

  // ✅ Cargar contenido del carrito con el header necesario
  function loadCartContent() {
    fetch(cartDetailUrl, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
      })
      .then(html => {
        document.querySelector('.cart-sidebar-content').innerHTML = html;
        attachEventListeners();
      })
      .catch(error => {
        console.error('Error loading cart content:', error);
        document.querySelector('.cart-sidebar-content').innerHTML = '<p>Error al cargar el carrito.</p>';
      });
  }

  // Agregar producto al carrito
  document.addEventListener('click', (e) => {
    if (e.target.classList.contains('add-to-cart')) {
      e.preventDefault(); // Evita la redirección
      const url = e.target.href;
      fetch(url, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            loadCartContent();
            updateCartBadge(data.cart_items);
            cartSidebar.classList.add('open'); // Abre el aside automáticamente
            cartOverlay.classList.add('show');
          }
        })
        .catch(error => {
          console.error('Error adding to cart:', error);
        });
    }
  });

  // Actualizar y eliminar ítems
  function attachEventListeners() {
    const updateForms = document.querySelectorAll('.cart-update-form');
    const removeLinks = document.querySelectorAll('.remove-item');

    updateForms.forEach(form => {
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

  // Actualizar el badge del carrito (opcional)
  function updateCartBadge(itemCount) {
    const badge = document.querySelector('.cart-badge');
    if (badge) {
      badge.textContent = itemCount;
    }
  }
});

document.addEventListener('DOMContentLoaded', () => {
  initCartSidebarToggle();   // Abrir/cerrar sidebar
  initUserDropdown();        // Menú de usuario
  initFlashMessageFadeout(); // Mensajes flash
});

/**
 * -------------------
 * Abrir/cerrar sidebar del carrito
 * -------------------
 */
function initCartSidebarToggle() {
  const cartBtn = document.querySelector('.cart-btn');
  const cartSidebar = document.getElementById('cartSidebar');
  const cartOverlay = document.getElementById('cartOverlay');
  const closeCartBtn = document.querySelector('.close-cart-btn');

  if (!cartBtn || !cartSidebar || !cartOverlay || !closeCartBtn) return;

  const toggleCart = (open = true) => {
    cartSidebar.classList.toggle('open', open);
    cartOverlay.classList.toggle('show', open);
    // Evitar el scroll del body cuando el carrito está abierto
    document.body.style.overflow = open ? 'hidden' : '';
  };

  cartBtn.addEventListener('click', () => toggleCart(true));
  closeCartBtn.addEventListener('click', () => toggleCart(false));
  cartOverlay.addEventListener('click', () => toggleCart(false));

  // Cerrar con la tecla 'Escape'
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && cartSidebar.classList.contains('open')) {
      toggleCart(false);
    }
  });
}

/**
 * -------------------
 * Dropdown de usuario (CORREGIDO)
 * -------------------
 * Maneja la visibilidad del menú de usuario con la clase .is-visible
 */
function initUserDropdown() {
  const userBtn = document.querySelector('.user-btn');
  const menu = document.getElementById('userMenu');

  if (!userBtn || !menu) return;

  // Añadir atributos para accesibilidad
  userBtn.setAttribute('aria-haspopup', 'true');
  userBtn.setAttribute('aria-expanded', 'false');

 userBtn.addEventListener('click', (e) => {
  e.stopPropagation();
  const isVisible = menu.classList.toggle('is-visible');
  // AÑADIMOS también la clase 'show' para compatibilidad con Bootstrap
  menu.classList.toggle('show', isVisible);
  userBtn.setAttribute('aria-expanded', isVisible);
});

  // Cierra el menú si se hace clic fuera de él
  document.addEventListener('click', () => {
    if (menu.classList.contains('is-visible')) {
      menu.classList.remove('is-visible');
      userBtn.setAttribute('aria-expanded', 'false');
    }
  });

  // Evita que el menú se cierre al hacer clic dentro de él
  menu.addEventListener('click', (e) => e.stopPropagation());
}


/**
 * -------------------
 * Desvanecer mensajes de Django (Flash Messages)
 * -------------------
 */
function initFlashMessageFadeout() {
  const userMessage = document.querySelector('.user-message');
  if (userMessage) {
    setTimeout(() => {
      userMessage.classList.add('fade-out');
      // Espera a que termine la transición para quitarlo del DOM
      userMessage.addEventListener('transitionend', () => userMessage.remove());
    }, 4000); // Aumentado el tiempo a 4 segundos
  }
}
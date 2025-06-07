
  document.addEventListener('DOMContentLoaded', function () {
    const offcanvasElement = document.getElementById('sidebarMenuMobile');
    const offcanvas = bootstrap.Offcanvas.getOrCreateInstance(offcanvasElement);

    // Buscamos todos los links dentro del offcanvas
    const links = offcanvasElement.querySelectorAll('a.nav-link');

    links.forEach(link => {
      link.addEventListener('click', function () {
        offcanvas.hide(); // Cierra el offcanvas cuando se hace clic
      });
    });
  });

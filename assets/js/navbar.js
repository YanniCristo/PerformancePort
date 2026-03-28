console.log("JS caricato");

window.addEventListener("DOMContentLoaded", function () {
    let lastScrollTop = 0;
    const threshold = 5; // evita movimenti per micro-scroll

    window.addEventListener("scroll", function () {
        const navbar = document.querySelector(".main-navbar");
        if (!navbar) return;

        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        // Scroll verso il basso
        if (scrollTop > lastScrollTop + threshold) {
            navbar.classList.add("navbar-hidden");
        }
        // Scroll verso l'alto
        else if (scrollTop < lastScrollTop - threshold) {
            navbar.classList.remove("navbar-hidden");
        }

        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });
});
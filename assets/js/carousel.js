function initCarouselObserver() {
    if (window._carouselObserver) {
        window._carouselObserver.disconnect();
    }

    window._carouselObserver = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'src') {
                var img = mutation.target;
                img.style.opacity = '0';
                setTimeout(function() {
                    img.style.opacity = '1';
                }, 350);
            }
        });
    });

    var img = document.getElementById('carousel-image');
    if (img) {
        window._carouselObserver.observe(img, { attributes: true });
    }
}

// Inizializzazione al caricamento
document.addEventListener('DOMContentLoaded', initCarouselObserver);

// Reinizializzazione quando Dash aggiorna il DOM (cambio pagina)
var _pageObserver = new MutationObserver(function() {
    var img = document.getElementById('carousel-image');
    if (img && !img._observed) {
        img._observed = true;
        initCarouselObserver();
    }
});

_pageObserver.observe(document.body, { childList: true, subtree: true });
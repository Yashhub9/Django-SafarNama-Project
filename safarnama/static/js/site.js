document.addEventListener("DOMContentLoaded", function () {
    var navShell = document.querySelector(".nav-shell");
    var backToTop = document.querySelector(".back-to-top");
    var revealItems = document.querySelectorAll(".reveal-up");
    var parallaxItems = document.querySelectorAll("[data-parallax]");

    function handleScrollState() {
        if (navShell) {
            navShell.classList.toggle("is-scrolled", window.scrollY > 24);
        }
    }

    function handleParallax() {
        var offset = window.scrollY * 0.08;
        parallaxItems.forEach(function (item) {
            item.style.transform = "translateY(" + offset.toFixed(2) + "px)";
        });
    }

    if ("IntersectionObserver" in window && revealItems.length) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        revealItems.forEach(function (item) {
            observer.observe(item);
        });
    } else {
        revealItems.forEach(function (item) {
            item.classList.add("is-visible");
        });
    }

    if (backToTop) {
        backToTop.addEventListener("click", function (event) {
            event.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    window.addEventListener("scroll", function () {
        handleScrollState();
        if (parallaxItems.length) {
            window.requestAnimationFrame(handleParallax);
        }
    }, { passive: true });

    handleScrollState();
    if (parallaxItems.length) {
        handleParallax();
    }
});

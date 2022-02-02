// Loek van Steijn

// starts css animation when user scrolled 1100px down
window.onscroll = () => {
    var block = document.querySelectorAll('.appear');
    if (window.innerHeight + window.scrollY >= 1100)
    {
        block.forEach(function(element) {
            element.style.animationPlayState = "running";
        });
    }
};

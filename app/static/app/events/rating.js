document.addEventListener('DOMContentLoaded', function () {
    const ratingBlocks = document.querySelectorAll('.rating-block');

    const ratingLabels = {
        1: "Malo",
        2: "Aceptable",
        3: "Bueno",
        4: "Muy bueno",
        5: "Excelente"
    };

    ratingBlocks.forEach(block => {
        const stars = block.querySelectorAll('.star');
        const hoverRating = block.querySelector('.hover-rating');
        const avgRating = block.querySelector('.avg-rating');
        let rating = 0;

        function setStarsHover(value) {
            stars.forEach(star => {
                if (parseInt(star.dataset.value) <= value) {
                    star.classList.add('text-warning');
                    star.classList.remove('text-muted');
                } else {
                    star.classList.remove('text-warning');
                    star.classList.add('text-muted');
                }
            });
        }

        stars.forEach(star => {
            star.addEventListener('mouseover', () => {
                const value = parseInt(star.dataset.value);
                setStarsHover(value);
                hoverRating.textContent = `Estás calificando: ${ratingLabels[value]}`;
            });

            star.addEventListener('mouseout', () => {
                setStarsHover(rating);
                if (rating) {
                    hoverRating.textContent = `Estás calificando: ${ratingLabels[rating]}`;
                } else {
                    hoverRating.textContent = "Estás calificando: -";
                }
            });

            star.addEventListener('click', () => {
                rating = parseInt(star.dataset.value);
                setStarsHover(rating);
                hoverRating.textContent = `Estás calificando: ${ratingLabels[rating]}`;
                console.log('Rating elegido:', rating);
                // Aquí podrías hacer un fetch() para enviar la calificación
            });
        });
    });
});

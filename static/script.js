document.getElementById('recommendation-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent form from reloading the page

    const genre = document.getElementById('genre').value;
    const rating = document.getElementById('rating').value;

    const data = {
        genre: genre,
        rating: rating
    };

    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const recommendationsDiv = document.getElementById('recommendations');
        recommendationsDiv.innerHTML = ''; // Clear previous recommendations

        data.recommendations.forEach(movie => {
            const movieDiv = document.createElement('div');
            movieDiv.textContent = movie;
            recommendationsDiv.appendChild(movieDiv);
        });
    })
    .catch(error => console.error('Error:', error));
});

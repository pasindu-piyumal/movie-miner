function fetchMovies() {
    let search = document.getElementById("search").value;
    let genre = document.getElementById("genre").value;

    fetch(`/search?search=${search}&genre=${genre}`)
        .then(res => res.json())
        .then(data => {
            let html = "";

            if (data.length === 0) {
                html = "<p>No movies found</p>";
            }

            data.forEach(movie => {
                html += `
                    <div class="movie">
                        <h3>${movie.Title} (${movie.Year})</h3>
                        <p>⭐ IMDb: ${movie.IMDb}</p>
                        <p>⏱ ${movie.Duration}</p>
                        <p>🎭 ${movie.Genres}</p>
                        <p>${movie.Synopsis}</p>
                        <p><b>Cast:</b> ${movie.Cast}</p>
                        <p><b>Director:</b> ${movie.Director}</p>
                        <p><b>Streaming:</b> ${movie.Providers}</p>
                        <a href="${movie.link}" target="_blank">View More</a>
                    </div>
                `;
            });

            document.getElementById("results").innerHTML = html;
        });
}

document.getElementById("search").addEventListener("keyup", fetchMovies);
document.getElementById("genre").addEventListener("change", fetchMovies);

fetchMovies();
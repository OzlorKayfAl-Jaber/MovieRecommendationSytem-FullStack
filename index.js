const movieInput = document.getElementById("movie-name");
const searchBtn = document.getElementById("search-btn");
const result = document.getElementById("result");
const recDiv = document.getElementById("recommendations");

async function getMovie() {
    const name = movieInput.value.trim();
    if (!name) return;

    const url = `https://www.omdbapi.com/?t=${name}&apikey=${key}`;
    const response = await fetch(url);
    const data = await response.json();

    if (data.Response === "True") {
        result.innerHTML = `
            <h2>${data.Title}</h2>
            <img src="${data.Poster}" class="poster">
            <p>${data.Plot}</p>
        `;

        getRecommendations(name);
    } else {
        result.innerHTML = "Movie not found";
    }
}

async function getRecommendations(title) {
    const url = `http://127.0.0.1:8000/recommend?title=${encodeURIComponent(title)}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        recDiv.innerHTML = `
            <h3>Recommended Movies</h3>
            <ul>
                ${data.results.map(m => `<li>${m.title} ⭐ ${m.rating}</li>`).join("")}
            </ul>
        `;
    } catch {
        recDiv.innerHTML = "Recommendation service unavailable";
    }
}

searchBtn.addEventListener("click", getMovie);
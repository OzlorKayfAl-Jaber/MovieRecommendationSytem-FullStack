const MovieNameRef=document.getElementById("movie-name");
const searchBtn=document.getElementById("search-btn");
const result=document.getElementById("result");

// Function to fetch movie details from OMDb API
const getMovie=async ()=> {
    const movieName=MovieNameRef.value.trim();

    if ( !movieName) {
        result.innerHTML='<h3 class="msg">Please enter a movie name</h3>';
        return;
    }

const url=`https://www.omdbapi.com/?t=${encodeURIComponent(movieName)}&apikey=${key}`;

    try {
        const response=await fetch(url);
        const data=await response.json();

        if (data.Response==="True") {
            result.innerHTML=` <div class="info"><img src="${data.Poster}"alt="${data.Title} Poster"class="poster"><div class="movie-details"><h2>${data.Title}</h2><div class="rating"><img src="star-icon.svg"alt="Rating"><h4>${data.imdbRating}</h4></div><div class="details"><span>${data.Rated}</span><span>${data.Year}</span><span>${data.Runtime}</span></div><div class="genres">${data.Genre.split(",").map(g=> `<div class="genre">${g.trim()}</div>`).join('')}</div></div></div><h3>Plot:</h3><p>${data.Plot}</p><h3>Cast:</h3><p>${data.Actors}</p>`;
        }

        else {
            result.innerHTML=`<h3 class="msg">${data.Error}</h3>`;
        }
    }

    catch (error) {
        result.innerHTML='<h3 class="msg">Error fetching movie data. Please try again later.</h3>';
        console.error(error);
    }
}

// Event listeners
searchBtn.addEventListener("click", getMovie);
window.addEventListener("load", getMovie);
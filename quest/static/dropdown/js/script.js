// Use JavaScript to dynamically populate the testimonies section
const testimonySection = document.getElementById('testimonies');

// Assume you have a Django view that returns a JSON response with the testimonies data
fetch('/testimonies/api/')
 .then(response => response.json())
 .then(data => {
    data.forEach(testimony => {
      const testimonyHTML = `
        <div class="testimony">
          <img src="${testimony.photo}" alt="Girl's photo">
          <h2>${testimony.name}</h2>
          <p>${testimony.testimony}</p>
        </div>
      `;
      testimonySection.innerHTML += testimonyHTML;
    });
  });
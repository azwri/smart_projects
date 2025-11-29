document.addEventListener('DOMContentLoaded', function () {
    // Initialize the map centered on Aseer Region (Abha)
    var map = L.map('map').setView([18.2465, 42.5117], 9);

    // Add CartoDB Positron tile layer (Grayscale/Muted)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    // Example marker for Abha
    var marker = L.marker([18.2465, 42.5117]).addTo(map);
    marker.bindPopup("<b>Abha</b><br>Capital of Aseer Province.").openPopup();

    // TODO: Fetch province GeoJSON data from backend and render polygons
});

document.addEventListener("DOMContentLoaded", function() {
    // Obtener datos de objetos
    const objetos = JSON.parse(document.getElementById("objetos-data").textContent);

    // Coordenadas iniciales (Chile aprox)
    const startLat = -33.45;
    const startLng = -70.66;

    // Crear mapa
    const map = L.map("map").setView([startLat, startLng], 5);

    // Añadir tiles
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    const cardsDiv = document.getElementById("cards");

    // Función para mostrar info en panel
    function mostrarCard(obj) {
        cardsDiv.innerHTML = `
            <div class="card">
                <h3>${obj.nombre}</h3>
                <p>${obj.descripcion}</p>
                <p><strong>Publicado por:</strong> ${obj.usuario.username}</p>
                <a href="/inicio_sesion/detalle_objeto/${obj.id}/" class="btn btn-azul">Ver más</a>
            </div>
        `;
    }

    function limpiarCard() {
        cardsDiv.innerHTML = "";
    }

    // Crear marcadores
    objetos.forEach(function(obj) {
        if(obj.latitud && obj.longitud) {
            const marker = L.marker([obj.latitud, obj.longitud]).addTo(map);

            // Popup al hacer click
            marker.bindPopup(`
                <strong>${obj.nombre}</strong><br>
                ${obj.descripcion}<br>
                <a href="/inicio_sesion/detalle_objeto/${obj.id}/">Ver más</a>
            `);

            // Evento hover: mostrar en panel #cards
            marker.on("mouseover", function() { mostrarCard(obj); });
            marker.on("mouseout", function() { limpiarCard(); });
        }
    });
});

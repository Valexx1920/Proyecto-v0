document.addEventListener("DOMContentLoaded", function() {
    if (typeof L === "undefined") {
        console.error("Leaflet no está definido.");
        return;
    }

    const objetosData = document.getElementById("objetos-data");
    const cardsDiv = document.getElementById("lista-objetos");

    if (!objetosData) return;

    const objetos = JSON.parse(objetosData.textContent);

    const map = L.map("map");
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    const markers = [];

    function mostrarCard(obj) {
        cardsDiv.innerHTML = `
            <div class="card" data-id="${obj.id}">
                ${obj.imagen_url ? `<img src="${obj.imagen_url}" alt="${obj.nombre}" class="card-img">` : ""}
                <h3>${obj.nombre}</h3>
                <p>${obj.descripcion}</p>
                <p><strong>Publicado por:</strong> ${obj.usuario__username || 'Desconocido'}</p>
                ${obj.latitud && obj.longitud ? `<p><strong>Ubicación:</strong> (${obj.latitud}, ${obj.longitud})</p>` : ""}
                ${obj.id ? `<a href="/detalle_objeto/${obj.id}/" class="btn btn-azul">Ver más</a>` : ""}
            </div>
        `;

        const cardDiv = cardsDiv.querySelector(".card");
        if(cardDiv) {
            cardDiv.addEventListener("mouseover", () => {
                const markerObj = markers.find(m => m.id === obj.id);
                if(markerObj) markerObj.marker.openPopup();
            });
            cardDiv.addEventListener("mouseout", () => {
                const markerObj = markers.find(m => m.id === obj.id);
                if(markerObj) markerObj.marker.closePopup();
            });
            cardDiv.addEventListener("click", () => {
                if(obj.latitud && obj.longitud) {
                    map.flyTo([obj.latitud, obj.longitud], 15);
                    const markerObj = markers.find(m => m.id === obj.id);
                    if(markerObj) markerObj.marker.openPopup();
                }
            });
        }
    }

    function limpiarCard() { cardsDiv.innerHTML = ""; }

    function agregarMarcador(obj) {
        if(obj.latitud && obj.longitud) {
            const marker = L.marker([obj.latitud, obj.longitud]).addTo(map);

            marker.bindPopup(`
                ${obj.imagen_url ? `<img src="${obj.imagen_url}" alt="${obj.nombre}" style="width:120px;height:auto;margin-bottom:5px;">` : ""}
                <strong>${obj.nombre}</strong><br>
                ${obj.descripcion}<br>
                <small>Publicado por: ${obj.usuario__username || 'Desconocido'}</small><br>
                ${obj.id ? `<a href="/detalle_objeto/${obj.id}/">Ver más</a>` : ""}
            `);

            marker.on("mouseover", () => mostrarCard(obj));
            marker.on("mouseout", limpiarCard);

            markers.push({ id: obj.id, marker });
            return [obj.latitud, obj.longitud];
        }
        return null;
    }

    // Normalizar imagen_url
    objetos.forEach(obj => {
        obj.imagen_url = obj.imagen_url || null;
    });

    let bounds = [];
    objetos.forEach(obj => {
        const coord = agregarMarcador(obj);
        if(coord) bounds.push(coord);
    });

    if(bounds.length) map.fitBounds(bounds, { padding: [50,50] });
    else map.setView([-33.45, -70.66], 5);

    const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    const mapaSocket = new WebSocket(`${ws_scheme}://${window.location.host}/ws/mapa/`);

    mapaSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const obj = data.objeto;

        // Asegurarse de tener imagen_url
        obj.imagen_url = obj.imagen_url || null;

        const coord = agregarMarcador(obj);
        if(coord) {
            bounds.push(coord);
            map.fitBounds(bounds, { padding: [50,50] });
        }
    };
});

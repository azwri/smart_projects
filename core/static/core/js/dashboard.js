document.addEventListener('DOMContentLoaded', function () {
    // --- Map Initialization ---
    // Initialize the map centered on Aseer Region (Abha)
    var map = L.map('map', {
        zoomControl: false, // Hide zoom controls for cleaner widget look
        attributionControl: false
    }).setView([18.2465, 42.5117], 8);

    // Add CartoDB Positron tile layer (Grayscale/Muted)
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 20
    }).addTo(map);

    // Add Project Markers
    if (typeof projectsData !== 'undefined') {
        projectsData.forEach(project => {
            let color = '#3B82F6'; // Default Blue
            if (project.status === 'completed') color = '#10B981'; // Green
            if (project.status === 'delayed') color = '#EF4444'; // Red
            if (project.status === 'in_progress') color = '#F59E0B'; // Yellow

            let popupContent = `<b>${project.name}</b><br>${project.province__name}<br>Status: ${project.status}`;
            if (project.video) {
                popupContent += `<br><video width="200" controls class="mt-2 rounded"><source src="${project.video}" type="video/mp4">Your browser does not support the video tag.</video>`;
            }
            
            L.circleMarker([project.latitude, project.longitude], {
                radius: 8,
                fillColor: color,
                color: '#fff',
                weight: 2,
                opacity: 1,
                fillOpacity: 0.8
            }).addTo(map)
                .bindPopup(popupContent);
        });
    }

    // --- Chart.js Initialization ---

    // 1. Projects Line Chart - Removed
    // if (typeof lineChartData !== 'undefined') { ... }

    // 2. Monthly Bar Chart
    if (typeof barChartData !== 'undefined') {
        const ctxBar = document.getElementById('monthlyBarChart').getContext('2d');
        new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: barChartData.labels,
                datasets: [{
                    label: 'حالة المشاريع',
                    data: barChartData.values,
                    backgroundColor: barChartData.colors,
                    borderRadius: 4
                }]
            },
            options: {
                rtl: true,
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, grid: { display: false }, position: 'right' },
                    x: { grid: { display: false }, reverse: true }
                }
            }
        });
    }

    // 3. Plan Donut Chart
    if (typeof donutChartData !== 'undefined') {
        const ctxDonut = document.getElementById('planDonutChart').getContext('2d');
        new Chart(ctxDonut, {
            type: 'doughnut',
            data: {
                labels: donutChartData.labels,
                datasets: [{
                    data: donutChartData.values,
                    backgroundColor: donutChartData.colors,
                    borderWidth: 0
                }]
            },
            options: {
                rtl: true,
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: { legend: { display: false } }
            }
        });
    }
});

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

            // Special case for Fog Walkway (Live Stream)
            if (project.name === 'ممشى الضباب') {
                popupContent += `<br>
                 <div class="mt-2">
                    <span class="badge bg-danger mb-1">مباشر</span>
                    <button class="btn btn-sm btn-primary w-100 mt-1" onclick="openLiveModal()">مشاهدة البث المباشر</button>
                 </div>`;
            } else if (project.video) {
                // Static Video
                popupContent += `<br>
                <button class="btn btn-sm btn-outline-primary w-100 mt-2" onclick="openVideoModal('${project.name}', '${project.video}')">
                    <i class="bi bi-play-circle me-1"></i> مشاهدة الفيديو
                </button>`;
            }

            const marker = L.circleMarker([project.latitude, project.longitude], {
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

// --- Modal Logic ---
let currentPeer = null;

window.openVideoModal = function (title, videoUrl) {
    const modalElement = document.getElementById('videoModal');
    if (!modalElement) {
        console.error('Modal element not found!');
        return;
    }
    const modal = bootstrap.Modal.getOrCreateInstance(modalElement);
    document.getElementById('videoModalLabel').innerText = title;

    const videoPlayer = document.getElementById('modal-video-player');
    const liveContainer = document.getElementById('modal-live-container');

    // Show static player, hide live
    videoPlayer.classList.remove('d-none');
    liveContainer.classList.add('d-none');

    videoPlayer.src = videoUrl;
    modal.show();

    // Stop on close
    modalElement.addEventListener('hidden.bs.modal', function () {
        videoPlayer.pause();
        videoPlayer.src = "";
    }, { once: true });
};

window.openLiveModal = function () {
    const modalElement = document.getElementById('videoModal');
    if (!modalElement) {
        console.error('Modal element not found!');
        return;
    }
    const modal = bootstrap.Modal.getOrCreateInstance(modalElement);
    document.getElementById('videoModalLabel').innerText = "ممشى الضباب - بث مباشر";

    const videoPlayer = document.getElementById('modal-video-player');
    const liveContainer = document.getElementById('modal-live-container');
    const liveStatus = document.getElementById('modal-live-status');
    const liveVideo = document.getElementById('modal-live-video');

    // Show live, hide static
    videoPlayer.classList.add('d-none');
    liveContainer.classList.remove('d-none');
    liveStatus.innerText = "جاري الاتصال...";
    liveStatus.className = 'mt-3 text-info';

    modal.show();

    // Start Peer Connection
    const peer = new Peer(null, { debug: 2 });
    currentPeer = peer;

    peer.on('open', function (id) {
        console.log('Viewer Peer ID:', id);
        liveStatus.innerText = 'جاري طلب البث...';

        const conn = peer.connect('absher-fog-walkway');

        conn.on('open', function () {
            console.log('Connected to broadcaster. Requesting stream...');
            conn.send('call-me');
        });

        conn.on('error', function (err) {
            console.error('Connection error:', err);
            liveStatus.innerText = 'خطأ في الاتصال';
            liveStatus.className = 'mt-3 text-danger';
        });
    });

    peer.on('call', function (call) {
        console.log('Receiving call from broadcaster...');
        call.answer(null);

        call.on('stream', function (remoteStream) {
            liveStatus.innerText = "";
            liveVideo.srcObject = remoteStream;
            liveVideo.play().catch(e => console.error('Play error', e));
        });
    });

    peer.on('error', function (err) {
        console.error('Peer error:', err);
        liveStatus.innerText = 'خطأ: ' + (err.type === 'peer-unavailable' ? 'البث غير متاح حالياً' : err.type);
        liveStatus.className = 'mt-3 text-danger';
    });

    // Cleanup on close
    modalElement.addEventListener('hidden.bs.modal', function () {
        if (currentPeer) {
            currentPeer.destroy();
            currentPeer = null;
        }
        liveVideo.srcObject = null;
    }, { once: true });
};

// Initialize the map
const map = L.map('map-container').setView([51.505, -0.09], 2);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Function to add markers to the map
let currentMarkerId = null; // Store the current marker ID

// Function to add markers to the map
function addMarkersToMap(markers) {
    console.log("Adding markers to map:", markers);  // Debugging line
    markers.forEach(marker => {
        const mapMarker = L.marker([marker.latitude, marker.longitude], {
            icon: L.icon({
                iconUrl: '../static/img/algae.png',
                iconSize: [20, 20],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
            })
        }).addTo(map);

        // Bind popup and trigger summary generation when opened
        mapMarker.bindPopup(createMarkerPopup(marker)).on('popupopen', () => {
            currentMarkerId = marker.id; // Set the current marker ID when popup opens
            generateSummary(marker.location);
        });
    });
}

// Function to create popup content with tabs
function createMarkerPopup(marker) {
    return `
        <div>
            <ul class="nav nav-tabs" id="myTab" role="tablist">
                <li class="nav-item">
                    <a class="nav-link active" id="overview-tab" data-toggle="tab" href="#overview" role="tab" aria-controls="overview" aria-selected="true">Overview</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" id="images-tab" data-toggle="tab" href="#images" role="tab" aria-controls="images" aria-selected="false">Upload Images</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" id="video-tab" data-toggle="tab" href="#video" role="tab" aria-controls="video" aria-selected="false">Video</a>
                </li>
            </ul>
            <div class="tab-content" id="myTabContent">
                <div class="tab-pane fade show active" id="overview" role="tabpanel" aria-labelledby="overview-tab">
                    <div id="loadingIndicator" style="text-align: center;">
                        <div class="spinner-border" role="status">
                            <span class="sr-only">Loading...</span>
                        </div>
                    </div>
                    <div id="summaryContent" style="display: none;"></div>
                </div>
                <div class="tab-pane fade" id="images" role="tabpanel" aria-labelledby="images-tab">
                    <input type="file" multiple accept="image/*" onchange="previewAndUploadImages(event)" />
                    <div id="carouselExample" class="carousel slide" data-ride="carousel">
                        <div class="carousel-inner" id="imagePreview"></div>
                        <a class="carousel-control-prev" href="#carouselExample" role="button" data-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="sr-only">Previous</span>
                        </a>
                        <a class="carousel-control-next" href="#carouselExample" role="button" data-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="sr-only">Next</span>
                        </a>
                    </div>
                </div>
                <div class="tab-pane fade" id="video" role="tabpanel" aria-labelledby="video-tab">
                    <strong>Showcase of Allegro generated videos illustrating Algae Formation</strong>
                    <video id="videoPlayer" width="100%" height="100%" controls>
                        <source id="videoSource" src="${marker.videoUrl || 'https://apiplatform-rhymes-prod-va.s3.amazonaws.com/20241103044609.mp4'}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <div id="videoButtonContainer" style="display: none;">
                        <button id="generateVideoButton" class="btn btn-primary" onclick="generateVideo()">Generate Video</button>
                    </div>
                </div>
            </div>
        </div>
            `;
}

// Load overview functionality when page loads
function loadOverviewTab() {
    const script = document.createElement('script');
    script.src = '/static/js/overview.js';
    script.onload = () => console.log("Overview script loaded.");
    document.body.appendChild(script);
}
loadOverviewTab();

function loadImagesTab() {
    // Check if images.js is already loaded to avoid loading it multiple times
    if (!document.querySelector('script[src="/static/js/images.js"]')) {
        const script = document.createElement('script');
        script.src = '/static/js/images.js';
        script.onload = () => console.log("Images script loaded.");
        document.body.appendChild(script);
    }
}
loadImagesTab();

function loadVideoTab() {
    // Check if video.js is already loaded to avoid loading it multiple times
    if (!document.querySelector('script[src="/static/js/video.js"]')) {
        const script = document.createElement('script');
        script.src = '/static/js/video.js';
        script.onload = () => console.log("Video script loaded.");
        document.body.appendChild(script);
    }
}

// Call loadVideoTab when you want to enable the video functionality
loadVideoTab();

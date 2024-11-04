// Declare a global variable to store analysis results
let analysisResults = [];

// Function to preview and upload images
function previewAndUploadImages(event) {
    console.log("File upload event triggered");

    const files = event.target.files;
    const imagePreview = document.getElementById('imagePreview');
    imagePreview.innerHTML = ''; // Clear previous images

    // Check if files were selected
    if (files.length === 0) {
        alert("No files selected. Please choose images to upload.");
        return; // Exit early if no files are selected
    }

    Array.from(files).forEach((file, index) => {
        const reader = new FileReader();

        reader.onload = function(e) {
            const isActive = index === 0 ? 'active' : '';
            const carouselItem = `
                <div class="carousel-item ${isActive}">
                    <img src="${e.target.result}" class="d-block w-100" alt="Uploaded Image">
                    <div class="carousel-caption d-none d-md-block">
                        <p id="image-caption-${index}">Loading analysis...</p>
                    </div>
                </div>
            `;
            imagePreview.innerHTML += carouselItem;
        };

        // Read the file as a data URL
        reader.readAsDataURL(file);
    });

    // After previewing images, proceed to upload them
    uploadImagesToBackend(files, currentMarkerId);
}

// Function to upload images to the backend
// Function to upload images to the backend
function uploadImagesToBackend(files, markerId) {
    const formData = new FormData();
    Array.from(files).forEach(file => formData.append('images', file));
    formData.append('marker_id', markerId); // Append the current marker ID

    fetch('/upload_images', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Upload failed.");
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            console.error('Backend error:', data.error);
            alert(`An error occurred: ${data.error}`);
        } else {
            console.log('Image analysis results:', data);
            // Store the analysis results in the global variable
            analysisResults = data;

            // Clear existing data in local storage and store the new analysis results
            localStorage.clear(); // Clear any existing local storage data
            localStorage.setItem('analysisResults', JSON.stringify(data)); // Store new results

            displayAnalysisResults(data);
            alert("Images uploaded successfully!");
        }
    })
    .catch(error => {
        console.error('Error uploading images:', error);
        alert("There was an error uploading the images. Please try again.");
    });
}

// Function to display analysis results
function displayAnalysisResults(data) {
    // Assuming the result array corresponds to the image order
    data.forEach((result, index) => {
        const captionElement = document.getElementById(`image-caption-${index}`);
        if (captionElement) {
            captionElement.innerText = result; // Update the caption with the analysis result
        } else {
            console.warn(`Caption element for index ${index} not found.`);
        }
    });

    // Check if the videoButtonContainer exists before trying to show it
    const videoButtonContainer = document.getElementById("videoButtonContainer");
    if (videoButtonContainer) {
        videoButtonContainer.style.display = "block"; // Show the "Generate Video" button after analysis is complete
    } else {
        console.error("Element with ID 'videoButtonContainer' not found.");
    }
}

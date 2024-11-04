// Function to generate video with analysis results
function generateVideo() {
    console.log("Generate video button clicked");
    
    // Retrieve the stored analysis results from local storage
    const storedResults = localStorage.getItem('analysisResults');
    if (storedResults) {
        const analysisResults = JSON.parse(storedResults); // Parse the results back to an object
        const refinedPrompt = analysisResults.join(', '); // Create a single prompt from results
        
        // Call the backend to generate the video
        fetch('/generate_video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: refinedPrompt })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                alert(`Video generation refer link: ${data.request_id}`);
                
                // Update the video player with the new video URL
                const videoPlayer = document.getElementById('videoPlayer');
                const videoSource = document.getElementById('videoSource');
                
                // Update the src attribute of the video source
                videoSource.src = data.request_id; // Assuming request_id contains the video URL
                videoPlayer.load(); // Load the new video
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while generating the video.");
        });
    } else {
        alert("No analysis results available.");
    }
}

// Event listener for the generate video button
document.getElementById('generateVideoButton').addEventListener('click', generateVideo);

function generateSummary(location) {
    const loadingIndicator = document.getElementById('loadingIndicator');
    const summaryContent = document.getElementById('summaryContent');

    // Show loading indicator and hide summary content
    loadingIndicator.style.display = 'block';
    summaryContent.style.display = 'none';

    fetch('/generate_summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ location: location })
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading indicator and display the summary in the popup
        loadingIndicator.style.display = 'none';
        summaryContent.innerHTML = `<p>${data.summary}</p>`;
        summaryContent.style.display = 'block';  // Show the summary content
    })
    .catch(error => {
        console.error('Error:', error);
        loadingIndicator.style.display = 'none'; // Hide loading indicator on error
    });
}

document.getElementById('weatherForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    fetch('process.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded' // Change to match form submission
        },
        body: new URLSearchParams(data) // Convert data to URL-encoded format
    })
    .then(response => response.text()) // Get response as text
    .then(responseText => {
        console.log('Response Text:', responseText); // Log the full response
        try {
            const result = JSON.parse(responseText);
            console.log('Parsed JSON:', result); // Log the parsed JSON

            // Ensure we received the expected keys
            if (result.predicted_temperature !== undefined &&
                result.predicted_weathercode !== undefined &&
                result.assigned_weather_code_description !== undefined &&
                result.predicted_rain !== undefined) {
                
                const roundedTemperature = Math.ceil(result.predicted_temperature);
                const roundedWeatherCode = Math.ceil(result.predicted_weathercode);
                const roundedRain = Math.ceil(result.predicted_rain);

                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = `
                    <h2>Prediction Results</h2>
                    <p><strong>Predicted Temperature:</strong> ${roundedTemperature}°C</p>
                    <p><strong>Predicted Weather Code:</strong> ${roundedWeatherCode}</p>
                    <p><strong>Weather Description:</strong> ${result.assigned_weather_code_description}</p>
                    <p><strong>Predicted Rain:</strong> ${roundedRain}mm</p>
                `;
            } else {
                console.error('Unexpected JSON format:', result);
                document.getElementById('result').innerHTML = `<p>Error: Unexpected response format</p>`;
            }
        } catch (error) {
            console.error('Error parsing JSON:', error);
            document.getElementById('result').innerHTML = `<p>Error: Invalid response from server</p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = `<p>Error: ${error.message}</p>`;
    });
});

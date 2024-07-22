<?php
// Enable error reporting for debugging
error_reporting(E_ALL);
ini_set('display_errors', 1);

header('Content-Type: application/json'); // Ensure the response is always JSON

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check if required POST variables are set
    if (!isset($_POST["apparent_temperature_mean"]) || !isset($_POST["rain_sum"])) {
        echo json_encode(['error' => 'Invalid input']);
        exit;
    }

    $data = [
        "apparent_temperature_mean" => $_POST["apparent_temperature_mean"],
        "rain_sum" => $_POST["rain_sum"]
    ];

    $url = "https://function-1";
    $options = [
        "http" => [
            "header"  => "Content-type: application/json\r\n",
            "method"  => "POST",
            "content" => json_encode($data),
        ],
    ];
    $context = stream_context_create($options);
    $response = @file_get_contents($url, false, $context);

    // Check for errors in the response
    if ($response === FALSE) {
        echo json_encode(['error' => 'Error occurred while calling the API']);
        exit;
    }

    // Decode the JSON response from the API
    $json_response = json_decode($response, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        echo json_encode(['error' => 'Invalid JSON response']);
        exit;
    }

    // Return the API response
    echo json_encode($json_response);
}
?>

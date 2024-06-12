<?php
// Assuming you have a MySQL database
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "content_db";

// Create a connection to the database
$conn = new mysqli($servername, $username, $password, $dbname);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Retrieve the translated text from the Flask app
    $translated_text = $_POST['translated_text'];

    // Data sanitization to prevent SQL injection (recommended)
    $translated_text = mysqli_real_escape_string($conn, $translated_text);

    // You can insert the data into your database table here
    // For example, let's assume you have a table called 'survey'
    // with a column 'app_usage'
    $sql = "INSERT INTO survey (app_usage) VALUES ('$translated_text')";

    if ($conn->query($sql) === TRUE) {
        echo "Data inserted successfully!";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

$conn->close();
?>

<!DOCTYPE html>
<html>
<head>
    <title>PHP Page</title>
</head>
<body>
    <p>hi</p>
</body>
</html>

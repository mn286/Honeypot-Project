<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login</title>
    <style>
        /* Hide the form from human users */
        #login-form {
            display: none;
        }

        /* Honeytrap styles */
        .honeytrap {
            display: none;
        }
    </style>
    <script>
        // Disable form functionality for human users
        window.onload = function() {
            const form = document.getElementById('login-form');
            form.onsubmit = function(event) {
                event.preventDefault();
                alert('This form is not functional.');
            };
        };
    </script>
</head>
<body>
    <h1>Admin Login</h1>
    <form id="login-form" action="/admin/dashboard.php" method="post">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" disabled>
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" disabled>
        <br>
        <button type="submit" disabled>Login</button>
        <!-- Honeytrap field to detect bots -->
        <input type="hidden" name="honeypot_field" class="honeytrap" value="">
    </form>
</body>
</html>

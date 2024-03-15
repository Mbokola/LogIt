// JavaScript to redirect when "Home" link is clicked
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('home-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default action
        window.location.href = '/home'; // Redirect to Flask route
    });
});

// JavaScript to redirect when "Create Log" link is clicked
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('create-log-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default action
        window.location.href = '/create'; // Redirect to Flask route
    });
});

// JavaScript to redirect when "about" link is clicked
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('about-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default action
        window.location.href = '/about'; // Redirect to Flask route
    });
});

// JavaScript to redirect when "LogIt" link is clicked
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('logit').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default action
        window.location.href = '/sessions'; // Redirect to Flask route
    });
});

// JavaScript to redirect when "Logout" link is clicked
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('logout').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default action

        // Send a DELETE request to the logout route
        fetch('/sessions', {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                // If the request is successful, redirect to another page
                window.location.href = '/sessions'; // Redirect to home page or any other page
            } else {
                // Handle error if necessary
                console.error('Failed to logout:', response.statusText);
            }
        })
        .catch(error => {
            // Handle error if necessary
            console.error('Error logging out:', error);
        });
    });
});

// JavaScript to redirect when "Submit" link is clicked when creating log
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('logout').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default action

        // Send a DELETE request to the logout route
        fetch('/create', {
            method: 'POST'
        })
        .then(response => {
            if (response.ok) {
                // If the request is successful, redirect to another page
                window.location.href = '/home'; // Redirect to home page or any other page
            } else {
                // Handle error if necessary
                console.error('unsuccesful:', response.statusText);
            }
        })
        .catch(error => {
            // Handle error if necessary
            console.error('Error:', error);
        });
    });
});

// JavaScript to redirect when "Create Log" link is clicked
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('home-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default action
        window.location.href = '/'; // Redirect to Flask route
    });
});

// JavaScript to redirect when "Create Log" link is clicked
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('create-log-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default action
        window.location.href = '/create'; // Redirect to Flask route
    });
});

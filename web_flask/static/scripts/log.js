document.addEventListener('DOMContentLoaded', function() {
    const logsContainer = document.getElementById('logs-container');
    const logFormContainer = document.getElementById('log-form-container');

    fetch('/logs')
    .then(response => response.json())
    .then(data => {
        if (data.length === 0) {
            logsContainer.innerHTML = '<div class="center-text">No Logs to display</div>';
        } else {
            const logsList = document.createElement('ul');

            // Iterate through each log and create list item
            data.forEach(log => {
                const logItem = document.createElement('li');
                const logLink = document.createElement('a');

                // Set the text content and href for the log link
                logLink.textContent = log;
                logLink.href = '#';
                logLink.classList.add('log-name'); // Add class to identify log name links

                // Apply styles to the log link
                logLink.style.color = '#34495e'; // Set link color

                // Append the link to the list item and list item to the list
                logItem.appendChild(logLink);
                logsList.appendChild(logItem);
            });

            // Append the list to the logs container
            logsContainer.appendChild(logsList);
        }
    })
    .catch(error => console.error('Error fetching logs:', error));

    // Event listener for log name clicks
    logsContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('log-name')) {
            event.preventDefault();
            const logName = event.target.textContent;
            window.location.href = `/log/${logName}`;
        }
    });
});

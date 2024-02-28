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
                const logActions = document.createElement('div');
                const viewLogBtn = document.createElement('button');
                const logBtn = document.createElement('button');
                const delBtn = document.createElement('button'); // Create delete button

                // Set the text content and href for the log link
                logLink.textContent = log;
                logLink.href = '#';
                logLink.classList.add('log-name'); // Add class to identify log name links

                // Apply styles to the log link
                logLink.style.color = '#34495e'; // Set link color

                // Add text content and classes to log action buttons
                viewLogBtn.textContent = 'View';
                viewLogBtn.classList.add('view-log-btn');
                logBtn.textContent = 'Log';
                logBtn.classList.add('log-btn');
                delBtn.textContent = 'Delete'; // Set text content for delete button
                delBtn.classList.add('del-btn'); // Add class to identify delete button

                // Set data attributes for URLs
                viewLogBtn.setAttribute('data-url', `/log/view/${log}`);
                logBtn.setAttribute('data-url', `/log/${log}`);
                delBtn.setAttribute('data-log', log); // Set data attribute for log name

                // Append log action buttons to log actions container
                logActions.appendChild(viewLogBtn);
                logActions.appendChild(logBtn);
                logActions.appendChild(delBtn); // Append delete button to log actions
                logActions.classList.add('log-actions'); // Add class to identify log actions

                // Append the log link and log actions to the list item
                logItem.appendChild(logLink);
                logItem.appendChild(logActions);

                // Append the list item to the logs list
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
            const logActions = event.target.nextElementSibling; // Get the log actions container

            // Toggle visibility of log actions
            logActions.style.display = logActions.style.display === 'none' ? 'block' : 'none';

            // Hide log actions of other logs
            const allLogActions = document.querySelectorAll('.log-actions');
            allLogActions.forEach(action => {
                if (action !== logActions && action.style.display !== 'none') {
                    action.style.display = 'none';
                }
            });
        }
    });

    // Event listener for log action button clicks
    logsContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('view-log-btn') || event.target.classList.contains('log-btn')) {
            const url = event.target.getAttribute('data-url');
            if (url) {
                window.location.href = url; // Redirect to the specified URL
            }
        }
    });

    // Event listener for delete button clicks
    logsContainer.addEventListener('click', function(event) {
        if (event.target.classList.contains('del-btn')) {
            const logName = event.target.getAttribute('data-log');
            if (confirm(`Are you sure you want to delete the log '${logName}'?`)) {
                fetch(`/log/delete/${logName}`, {
                    method: 'DELETE'
                })
                .then(response => {
                    if (response.ok) {
                        // Reload the page after successful deletion
                        window.location.reload();
                    } else {
                        console.error('Error deleting log:', response.statusText);
                    }
                })
                .catch(error => console.error('Error deleting log:', error));
            }
        }
    });

});

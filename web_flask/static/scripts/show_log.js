function redirectToPage(logName, id) { // Modify to accept log name and ID
    window.location.href = '/log/' + logName + '/page/' + id; // Concatenate log name and ID in the URL
}

function showTooltip(event) {
    var tooltip = document.querySelector('.tooltip');
    tooltip.style.visibility = 'visible';
    tooltip.style.top = (event.clientY + 10) + 'px'; // Adjust tooltip's top position
    tooltip.style.left = (event.clientX + 10) + 'px'; // Adjust tooltip's left position

    setTimeout(function() {
        tooltip.style.visibility = 'hidden'; // Hide the tooltip after 3 seconds
    }, 100); // 3000 milliseconds = 3 seconds
}

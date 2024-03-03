document.addEventListener('DOMContentLoaded', function() {
    var addButton = document.querySelector('.add-button');
    var form = document.querySelector('.dynamic-form');
    var submitButton = form.querySelector('input[type="submit"]');

    function addField(event) {
        var inputType = form.querySelector('.field-type').value;

        var container = document.createElement("div");
        var label = document.createElement("label");
        var input = document.createElement("input");
        var removeButton = document.createElement("button");

        input.setAttribute("type", inputType);
        input.setAttribute("name", inputType.toLowerCase());
        input.setAttribute("required", "required"); // Add required attribute
        label.innerHTML = inputType + ": ";
        removeButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
        removeButton.setAttribute("type", "button");
        removeButton.addEventListener("click", function() {
            form.removeChild(container);
            if (form.lastChild.tagName === "BR") {
                form.removeChild(form.lastChild);
            }
        });

        container.appendChild(label);
        container.appendChild(input);
        container.appendChild(removeButton);

        // Insert the new field container before the first button (addButton)
        form.insertBefore(container, addButton);

        if (!form.querySelector('.dynamic-form div')) {
            form.insertBefore(document.createElement("br"), addButton); // Add a line break if no fields exist
        }
    }

    addButton.addEventListener("click", addField);
});

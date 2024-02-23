document.addEventListener('DOMContentLoaded', function() {
    var addButton = document.querySelector('.add-button');

    function addField(event) {
        var form = document.querySelector('.dynamic-form');
        var inputType = form.querySelector('.field-type').value;

        var container = document.createElement("div");
        var label = document.createElement("label");
        var input = document.createElement("input");
        var removeButton = document.createElement("button");

        input.setAttribute("type", inputType);
        input.setAttribute("name", inputType.toLowerCase());
        label.innerHTML = inputType + ": ";
        removeButton.innerHTML = '<i class="fas fa-trash-alt"></i>';
        removeButton.setAttribute("type", "button");
        removeButton.addEventListener("click", function() {
            form.removeChild(container);
            if (form.firstChild.tagName === "BR") {
                form.removeChild(form.firstChild);
            }
        });

        container.appendChild(label);
        container.appendChild(input);
        container.appendChild(removeButton);

        if (form.firstChild) {
            form.insertBefore(container, form.firstChild.nextSibling);
        } else {
            form.appendChild(container);
        }
        if (!form.firstChild || form.firstChild.tagName !== "BR") {
            form.insertBefore(document.createElement("br"), form.firstChild);
        }
    }

    addButton.addEventListener("click", addField);
});

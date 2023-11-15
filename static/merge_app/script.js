const list = document.getElementById('sortable-list');
    
let draggedItem = null;

list.addEventListener('dragstart', function (e) {
    draggedItem = e.target;
    setTimeout(function () {
        draggedItem.style.display = 'none';
    }, 0);
});

list.addEventListener('dragend', function () {
    setTimeout(function () {
        draggedItem.style.display = 'block';
        draggedItem = null;

        // Print the names of items in order after a drag-and-drop
        //const items = [...list.children];
        const items = [...list.querySelectorAll('.sortable-item')];
        const itemNames = items.map(item => item.textContent.trim()); // << == List of files in custom order

        const integers = [...list.querySelectorAll('.sortable-integer')];
        const intValues = items.map(item => item.textContent.trim());

        itemNamesField.value = itemNames.join(',');     // <<== LOOK AT THIS TO GET INTO FORM ABOVE ******

        
        console.log('Order after drag-and-drop:', itemNames);//itemNames
    }, 0);
});

list.addEventListener('dragover', function (e) {
    e.preventDefault();
    const afterElement = getDragAfterElement(list, e.clientY);

    if (afterElement == null) {
        list.appendChild(draggedItem);
    } else {
        list.insertBefore(draggedItem, afterElement);
    }
});

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('[draggable="true"]:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;

        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

document.getElementById('submit-button').addEventListener('click', function() {
    var selectedValues = [];

    // Iterate through each select element and get the selected value
    var uploadElements = document.querySelectorAll('[id^="custom-integer-"]');
    uploadElements.forEach(function(uploadElement) {
        var selectedValue = uploadElement.options[uploadElement.selectedIndex].value;
        selectedValues.push(selectedValue);
    });

    selectedValuesField.value = selectedValues.join(',');

    // Log the selected values to the console
    console.log(selectedValues);
});
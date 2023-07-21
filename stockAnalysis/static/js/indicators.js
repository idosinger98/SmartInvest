const items = typeof indicators !== 'undefined' ?
    indicators :
    {'Item 1': 'description', 'Item 2': 'description', 'Item 3': 'description'};
const checkboxListDiv = document.getElementById('checkboxList');

for (const key of Object.keys(items)) {
    const listItem = document.createElement('li');
    const checkbox = document.createElement('input');
    const label = document.createElement('label');
    const infoIcon = document.createElement('i');
    const tooltip = document.createElement('span');


    listItem.className = 'algoCheckBox'
    checkbox.type = 'checkbox';
    checkbox.value = key;
    checkbox.id = `checkbox_${key.replace(/\s/g, '_')}`;
    checkbox.className = 'algoCheckBox'

    label.htmlFor = checkbox.id;
    label.textContent = key;

    infoIcon.className = 'fas fa-exclamation-circle';
    infoIcon.appendChild(tooltip);

    tooltip.className = "tooltip";
    tooltip.textContent = items[key];

    listItem.appendChild(checkbox);
    listItem.appendChild(label);
    listItem.appendChild(infoIcon);
    checkboxListDiv.appendChild(listItem);
}
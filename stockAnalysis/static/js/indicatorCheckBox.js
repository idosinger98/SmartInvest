export class IndicatorCheckBox {
    constructor(name, info) {
        this.listItem = document.createElement('li');
        this.checkbox = document.createElement('input');
        this.label = document.createElement('label');
        this.infoIcon = document.createElement('i');
        this.tooltip = document.createElement('span');

        this.listItem.className = 'algoCheckBox';
        this.checkbox.type = 'checkbox';
        this.checkbox.value = name;
        this.checkbox.id = `checkbox_${name.replace(/\s/g, '_')}`;
        this.checkbox.className = 'algoCheckBox';

        this.label.htmlFor = this.checkbox.id;
        this.label.textContent = name;

        this.infoIcon.className = 'fas fa-exclamation-circle';
        this.infoIcon.appendChild(this.tooltip);

        this.tooltip.className = 'tooltip';
        this.tooltip.textContent = info;

        this.listItem.appendChild(this.checkbox);
        this.listItem.appendChild(this.label);
        this.listItem.appendChild(this.infoIcon);
    }

    getElement() {
        return this.listItem;
    }

    addEventListener(activeFunc,deactivateFunc){
        this.checkbox.addEventListener('change',()=> {
                if (this.checkbox.checked) {
                    activeFunc(this.checkbox.value);
                } else {
                    deactivateFunc(this.checkbox.value);
                }
            }
        );
    }
}
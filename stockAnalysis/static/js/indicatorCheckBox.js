import {GET_ALGOS_URL} from "../../../static/js/urls.js";

export class IndicatorCheckBox {
    constructor(name, info) {
        this.listItem = document.createElement('li');
        this.checkbox = document.createElement('input');
        this.label = document.createElement('label');
        this.infoIcon = document.createElement('i');
        this.tooltip = document.createElement('span');
        this.initHtmlElement(name, info);
        this.is_loaded = false;
        this.data = {};
    }

    initHtmlElement(name, info){
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

    isChecked(){
        return this.checkbox.checked;
    }

    getElementData(){
        return this.data;
    }

    addStatusChangeEventListener(activeFunc, deactivateFunc, data){
        this.checkbox.addEventListener('change',()=> {
                if (this.checkbox.checked) {
                    this.checkbox.disabled = true;
                    activeFunc(data);
                } else {
                    deactivateFunc(this.checkbox.value);
                }
            }
        );
    }

    getIndicatorAsync(data, chart) {
        if (this.is_loaded) {
            this.atomicCallback(chart,this.data);
            return;
        }

        fetch(GET_ALGOS_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'stock': data, 'indicators': [this.checkbox.value]})
        }).then(response => {
                if (!response.ok) {
                    throw new Error('Request failed with status: ' + response.status + response.body);
                }
                return response.json();
            }).then(data => {
                data = Object.fromEntries(Object.keys(data).map(key => [key, JSON.parse(data[key])]));
                Object.keys(data).forEach(key => {
                    Object.entries(data[key]).forEach(([secondaryKey, value]) =>
                        data[key][secondaryKey] = Object.entries(value).map(([key, value]) => [parseInt(key), value]));
                });
                this.data = data;
                this.is_loaded = true;
                this.atomicCallback(chart,data);
            })
            .catch(error => console.log(error));
    }

    atomicCallback(chart, data) {
        this.checkbox.disabled = true;
        if (this.checkbox.checked) {
            chart.addIndicatorToChart(data);
        }
        this.checkbox.disabled = false;
    }
}
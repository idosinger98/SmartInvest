import {sendToastMessage, MESSAGE_TYPE, sendNotLoginMessage} from '../../../static/js/toastinette.js';
import {SAVE_STOCK_URL} from "../../../static/js/urls.js";


const overlay = document.getElementById('overlay');
const windowElement = document.getElementById('window');
const closeButton = document.getElementById('closeButton');
const titleInput = document.getElementById('titleInput');
const publicCheckBox = document.getElementById('publicCheckBox');

publicCheckBox.addEventListener('change', () => {
    if (publicCheckBox.checked) {
        titleInput.style.display = 'block';
    } else {
        titleInput.style.display = 'none';
    }
});

document.getElementById('saveButton').addEventListener('click', function () {
    this.blur();
    if(!is_user_connected()){
        sendNotLoginMessage();
        return;
    }
    overlay.style.display = 'block';
    windowElement.style.display = 'block';
});

overlay.addEventListener('click', (event) => {
    if (event.target === overlay) {
        overlay.style.display = 'none';
        windowElement.style.display = 'none';
    }
});

closeButton.addEventListener('click', () => {
    overlay.style.display = 'none';
    windowElement.style.display = 'none';
});

export async function sendChart(chart){
    if(!isTitleFilled(publicCheckBox.checked, titleInput.value)){
        sendToastMessage(
            'in case you want to publish your analysis you must fill the title.',
            MESSAGE_TYPE.ERROR,
            {title: "empty title"}
        );
        return;
    }
    const description = document.getElementById('textArea').value;
    const stockSymbolValueLabel = document.getElementById('stockSymbolValue').getAttribute("data-stock-value");
    const bodyData = {
        'chart': await chart.chartToJson(),
        'description': description,
        'is_public': publicCheckBox.checked,
        'title': titleInput.value,
        'stockSymbolValue': stockSymbolValueLabel,
    };

    fetch(SAVE_STOCK_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bodyData)
        })
        .then(async response => [response.ok ? MESSAGE_TYPE.SUCCESS : MESSAGE_TYPE.ERROR, await response.text()])
        .then(message => sendToastMessage(message[1], message[0]))
        .catch(error => sendToastMessage(error, MESSAGE_TYPE.ERROR));
    overlay.style.display = 'none';
    windowElement.style.display = 'none';
}

function isTitleFilled(is_public, title){
    return !is_public ||  (title !== null && title.trim() !== "")
}

function is_user_connected(){
    const isAuthenticatedData = document.getElementById('isAuthenticated');
    return isAuthenticatedData ? JSON.parse(isAuthenticatedData.textContent.toLowerCase()) : false;
}
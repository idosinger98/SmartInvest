import {StockChart} from "../../../static/js/stockChart.js";
import {IndicatorCheckBox} from "../../../static/js/indicatorCheckBox.js";
import {SAVE_STOCK_URL, CHECK_CONNECTED_URL} from "../../../static/js/urls.js";
import {sendToastMessage, MESSAGE_TYPE, sendNotLoginMessage} from '../../../static/js/toastinette.js';

const data = JSON.parse(stockData['stock']);
const chart = new StockChart();
const checkboxListDiv = document.getElementById('checkboxList');

chart.createFromData(data);
chart.drawChart('chart_container');
for (const key of Object.keys(indicators)) {
    const listItem = new IndicatorCheckBox(key,indicators[key]);

    checkboxListDiv.appendChild(listItem.getElement());
    chart.addIndicatorCheckBox(listItem, data);
}

const overlay = document.getElementById('overlay');
const windowElement = document.getElementById('window');
const closeButton = document.getElementById('closeButton');
const submitButton = document.getElementById('submitButton');
const titleInput = document.getElementById('titleInput');
const publicCheckBox = document.getElementById('publicCheckBox');

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

submitButton.addEventListener('click', async () => {
    submitButton.blur();
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
    console.log(bodyData);

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
});

publicCheckBox.addEventListener('change', () => {
    if (publicCheckBox.checked) {
        titleInput.style.display = 'block';
    } else {
        titleInput.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const stockSymbolInput = document.getElementById('stockSymbolInput');
    const comparisonResult = document.getElementById('comparisonResult');
    const comparisonResultMessage = document.getElementById('compare-result-message');


  document.getElementById('compareButton').addEventListener('click', function() {
    console.log('compareButton was clicked!');
    const symbol = stockSymbolInput.value.toLowerCase();
    const fundamentalsItems = {}; // Create an empty object for the fundamentals items
    const fundamentalsList = document.querySelectorAll('#fundamentals-container ul li');
    for (const listItem of fundamentalsList) {
        const [key, value] = listItem.textContent.split(': ');
        fundamentalsItems[key] = value;
    }

    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/compareStocks/');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    xhr.onload = function() {
      if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText);
        comparisonResult.innerHTML = ''; // Clear previous content
        comparisonResultMessage.innerHTML = '';
        const fundamentals = response.fundamentals;
        const message = `${symbol.toUpperCase()} will ${response.is_better ? '' : 'not'} be a better invest!`;
        const messageElement = document.createElement('p');
        messageElement.textContent = message;
        messageElement.style.color = response.is_better ? 'green' : 'red';
        comparisonResultMessage.appendChild(messageElement);
        const stockName = document.createElement('p');
        stockName.textContent = symbol.toUpperCase();
        comparisonResult.appendChild(stockName);
        for (const key in fundamentals) {
            if (fundamentals.hasOwnProperty(key)) {
                const value = fundamentals[key];
                const listItem = document.createElement('li');
                listItem.textContent = `${key}: ${value}`;
                comparisonResult.appendChild(listItem);
            }
        }
      } else {
        comparisonResult.innerHTML = '';
        const message = 'Invalid input!';
        const messageElement = document.createElement('p');
        messageElement.textContent = message;
        comparisonResult.appendChild(messageElement);
      }
    };
    const payload = {
        symbol: symbol,
        fundamentalsItems: fundamentalsItems
    };
    xhr.send(JSON.stringify(payload));
  });
});

function getCookie(name) {
  let value = "; " + document.cookie;
  let parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function isTitleFilled(is_public, title){
    return !is_public ||  (title !== null && title.trim() !== "")
}

function is_user_connected(){
    const isAuthenticatedData = document.getElementById('isAuthenticated');
    console.log(isAuthenticatedData);
    return isAuthenticatedData ? JSON.parse(isAuthenticatedData.textContent.toLowerCase()) : false;
}
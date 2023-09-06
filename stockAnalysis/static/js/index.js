import {StockChart} from "../../../static/js/stockChart.js";
import {IndicatorCheckBox} from "../../../static/js/indicatorCheckBox.js";

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


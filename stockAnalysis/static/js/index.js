import {StockChart} from "../../../static/js/stockChart.js";
import {IndicatorCheckBox} from "../../../static/js/indicatorCheckBox.js";
import {sendChart} from "./overlayLogic.js";
import {MESSAGE_TYPE, sendToastMessage} from "../../../static/js/toastinette.js";

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


document.addEventListener('DOMContentLoaded', function () {
    const stockSymbolInput = document.getElementById('stockSymbolInput');
    const comparisonResult = document.getElementById('comparisonResult');
    const comparisonResultMessage = document.getElementById('compare-result-message');

     $(document).ready(function () {
        const chartContainer = document.getElementById("chartContainer");
        const symbol = chartContainer.getAttribute('data-sy'); // Replace with the actual symbol or retrieve it dynamically
        const requestData = {
            'sy': symbol
        };

        chartContainer.textContent = 'Calculating the graph prediction...';

        $.ajax({
            url: "mlAlgorithm/",  // Replace with the actual URL of your view
            method: "POST",
            dataType: "json",
            data: JSON.stringify(requestData), // Send the 'symbol' parameter in the request body
            contentType: "application/json",
            timeout: 150000,
            success: function (data) {
                console.log("Succeed to fetch data.");

                const chart2 = anychart.line()

                function transformData(data) {
                  data = JSON.parse(data);
                  const result = [];
                  for (const key in data) {
                    const innerData = data[key];
                    const innerArray = [];
                    for (const innerKey in innerData) {
                      innerArray.push([innerKey, innerData[innerKey]]);
                    }
                    result.push([key, innerArray]);
                  }
                  return result;
                }

                data = transformData(data);

                const rawData = chart2.line(Object.values(data[0][1]));
                const predictedData = chart2.line(Object.values(data[1][1])).stroke("orange");

                chartContainer.style.marginLeft = '0px';
                chartContainer.textContent = '';
                chart2.container("chartContainer");
                chart2.draw();

            },
            error: function (xhr, status, error) {
                console.log("Error:", status, error);
                if(xhr.responseJSON) {
                    console.log("Error Response Data:", xhr.responseJSON);
                }
            }
        });
    });

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
    comparisonResult.innerHTML = ''; // Clear previous content
    comparisonResultMessage.innerHTML = '';

    xhr.onload = function() {
      if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText);
        const fundamentals = response.fundamentals;
        const message = `${symbol.toUpperCase()} will ${response.is_better ? '' : 'not'} be a better invest!`;
        const messageElement = document.createElement('p');
        messageElement.textContent = message;
        messageElement.style.margin = '10px';
        messageElement.style.color = response.is_better ? 'green' : 'red';
        comparisonResultMessage.appendChild(messageElement);
        const stockName = document.createElement('h4');
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
        sendToastMessage(`The Symbol - ${symbol} does not exists!`, MESSAGE_TYPE.ERROR);
      }
      stockSymbolInput.value = '';
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

const submitButton = document.getElementById('submitButton');

submitButton.addEventListener('click',  () => {
    submitButton.blur();
    sendChart(chart);
});
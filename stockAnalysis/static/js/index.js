import {StockChart} from "../../../static/js/stockChart.js";
import {IndicatorCheckBox} from "../../../static/js/indicatorCheckBox.js";
import {SAVE_STOCK_URL, CHECK_CONNECTED_URL} from "../../../static/js/urls.js";
import {sendToastMessage, MESSAGE_TYPE, sendNotLoginMessage} from '../../../static/js/toastinette.js';

const data =
    typeof stockData !== 'undefined' ?
        JSON.parse(stockData['stock']) :
        {
            "Open": {
                "1648785600000": 172.9821241694,
                "1649044800000": 173.5188920982,
                "1649131200000": 176.4312464982,
                "1649217600000": 171.3221871912,
                "1649304000000": 170.1294054439,
                "1649390400000": 170.7456835967,
                "1649649600000": 167.6941675201,
                "1649736000000": 167.0083304288,
                "1649822400000": 166.3821070002,
                "1649908800000": 169.5926630087,
                "1650254400000": 162.9329956542,
                "1650340800000": 164.0263848509,
                "1650427200000": 167.7438545675,
                "1650513600000": 167.8929507273,
                "1650600000000": 165.4577208466,
                "1650859200000": 160.1498491913
            },
            "High": {
                "1648785600000": 173.8270121909,
                "1649044800000": 177.4152873022,
                "1649131200000": 177.2264326144,
                "1649217600000": 172.5845445185,
                "1649304000000": 172.3161556471,
                "1649390400000": 170.7456835967,
                "1649649600000": 168.0122328446,
                "1649736000000": 168.847182199,
                "1649822400000": 170.0101234722,
                "1649908800000": 170.238758348,
                "1650254400000": 165.5968666036,
                "1650340800000": 166.8095285078,
                "1650427200000": 167.8631423354,
                "1650513600000": 170.4971701434,
                "1650600000000": 166.8592194542,
                "1650859200000": 162.1875086348
            },
            "Low": {
                "1648785600000": 170.9047121797,
                "1649044800000": 173.3896699965,
                "1649131200000": 173.3697898094,
                "1649217600000": 169.105618706,
                "1649304000000": 168.8272957161,
                "1649390400000": 168.1812163744,
                "1649649600000": 164.5034889463,
                "1649736000000": 165.636634764,
                "1649822400000": 165.7658450114,
                "1649908800000": 164.046259321,
                "1650254400000": 162.5851121902,
                "1650340800000": 162.9230677828,
                "1650427200000": 165.0998825219,
                "1650513600000": 164.9110145408,
                "1650600000000": 160.527579232,
                "1650859200000": 157.5058772788
            },
            "Close": {
                "1648785600000": 173.2604370117,
                "1649044800000": 177.3655853271,
                "1649131200000": 174.0059356689,
                "1649217600000": 170.7953796387,
                "1649304000000": 171.1035003662,
                "1649390400000": 169.0658569336,
                "1649649600000": 164.7519836426,
                "1649736000000": 166.6504974365,
                "1649822400000": 169.3739776611,
                "1649908800000": 164.2947540283,
                "1650254400000": 164.0760803223,
                "1650340800000": 166.3920440674,
                "1650427200000": 166.2230682373,
                "1650513600000": 165.4179382324,
                "1650600000000": 160.815826416,
                "1650859200000": 161.8992614746
            },
            "Volume": {
                "1648785600000": 78751300,
                "1649044800000": 76468400,
                "1649131200000": 73401800,
                "1649217600000": 89058800,
                "1649304000000": 77594700,
                "1649390400000": 76575500,
                "1649649600000": 72246700,
                "1649736000000": 79265200,
                "1649822400000": 70618900,
                "1649908800000": 75329400,
                "1650254400000": 69023900,
                "1650340800000": 67723800,
                "1650427200000": 67929800,
                "1650513600000": 87227800,
                "1650600000000": 84882400,
                "1650859200000": 96046400
            },
        };

const chart = new StockChart();
chart.createFromData(data);
chart.drawChart('chart_container');

const items = typeof indicators !== 'undefined' ?
    indicators :
    {'Item 1': 'description', 'Item 2': 'description', 'Item 3': 'description'};
const checkboxListDiv = document.getElementById('checkboxList');

for (const key of Object.keys(items)) {
    const listItem = new IndicatorCheckBox(key,items[key]);

    checkboxListDiv.appendChild(listItem.getElement());
    chart.addIndicatorCheckBox(listItem, data);
}

const overlay = document.getElementById('overlay');
const windowElement = document.getElementById('window');
const closeButton = document.getElementById('closeButton');
const submitButton = document.getElementById('submitButton');
const titleInput = document.getElementById('titleInput');
const publicCheckBox = document.getElementById('publicCheckBox');


document.getElementById('saveButton').addEventListener('click', async function () {
    this.blur();
    if(!await is_user_connected()){
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

async function is_user_connected(){
    try {
        return (await fetch(CHECK_CONNECTED_URL, {
            method: 'GET',
        })).ok;
    }
    catch(e) {
        return false;
    }
}
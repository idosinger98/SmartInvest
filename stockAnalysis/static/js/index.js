import {StockChart} from "./stockChart.js";
import {IndicatorCheckBox} from "./indicatorCheckBox.js";

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

const volumeData = [];
const newData = [];

for (const timestamp of Object.keys(data.Open)) {
    newData.push([
        parseInt(timestamp),
        data['Open'][timestamp],
        data['High'][timestamp],
        data['Low'][timestamp],
        data['Close'][timestamp],
    ]);
    volumeData.push([parseInt(timestamp), data['Volume'][timestamp]]);
}

const chart = new StockChart();
chart.createFromData(newData,volumeData);

const lineData = [];

for (const timestamp of Object.keys(data.Open)) {
    lineData.push([
        parseInt(timestamp),
        data['Open'][timestamp],
    ]);
}

chart.drawChart('chart_container');

// indicators handle
const items = typeof indicators !== 'undefined' ?
    indicators :
    {'Item 1': 'description', 'Item 2': 'description', 'Item 3': 'description'};
const checkboxListDiv = document.getElementById('checkboxList');

for (const key of Object.keys(items)) {
    const listItem = new IndicatorCheckBox(key,items[key]);

    listItem.addEventListener(
        (name)=> chart.addIndicatorLineOnNewPlot(lineData,name),
        (name)=> chart.removeIndicatorLine(name));

    checkboxListDiv.appendChild(listItem.getElement());
}

document.getElementById('saveButton').addEventListener('click', function () {
    chart.saveChart();
    this.blur();
});


// function get_algos(data,callback){
//      fetch(url, {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify(data)
//   })
//   .then(response => {
//     if (!response.ok) {
//       throw new Error('Request failed with status: ' + response.status);
//     }
//     return response.json();
//   })
//   .then(data => callback(null, data))
//   .catch(error => callback(error, null));
// }
import {StockChart} from "../../../static/js/stockChart.js";


for(const post in posts_images){
    const postHtml = document.getElementById("post-" + post.id + "-img");
    const chart = new StockChart();
    chart.loadChartFromJson(post.stock_image);
    chart.chartToPng(postHtml);
}

  //   document.querySelector('#comment-form').addEventListener('submit', function (event) {
  //
  //     event.preventDefault(); // Prevent the default form submission behavior
  //     const form = event.target;
  //     const formData = new FormData(form);
  //
  //     const request = new XMLHttpRequest();
  //     request.open(form.method, form.action);
  //     request.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
  //     request.onload = function () {
  //         if (request.status === 200) {
  //             window.location.reload();
  //         } else {
  //             alert('An error occurred while sending the message. Please try again.');
  //         }
  //     };
  //     request.send(formData);
  // });

window.addEventListener("load", function() {
  // Hide the stock list container on page load
  const stockListContainer = document.getElementById("stock_list_container");
  stockListContainer.style.display = "none";

  document.getElementById("stockInput").addEventListener("keyup", function() {
    let search = this.value.toLowerCase();
    let all = document.querySelectorAll("#stock_list li");

    if (search == '') {
      stockListContainer.style.display = "none";
      for (let i of all) {
        let item = i.innerHTML.toLowerCase();
        i.classList.add("hide");
      }
    } else {

      for (let i of all) {
        let item = i.innerHTML.toLowerCase();
        stockListContainer.style.display = "block"
        if (item.indexOf(search) == -1) {
          i.classList.add("hide");
        } else {
          i.classList.remove("hide");
        }
      }
    }
  });

  let stockItems = document.querySelectorAll(".stock-item");
  stockItems.forEach(item => {
    item.addEventListener("click", function() {
      let stockSymbol = this.innerText;
      let url = "/stockgraph?sy=" + encodeURIComponent(stockSymbol);
      window.location.href = url;
    });
  });
});

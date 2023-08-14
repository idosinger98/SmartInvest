     document.querySelector('#contact-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission behavior

    let form = event.target;
    let formData = new FormData(form);

    let request = new XMLHttpRequest();
    request.open(form.method, form.action);
    request.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
    request.onload = function () {
      if (request.status === 200) {
        showSuccessMessage();
      } else {
        alert('An error occurred while sending the message. Please try again.');
      }
    };
    request.send(formData);
  });

  function showSuccessMessage() {
    let successMessage = document.querySelector('.sent-message');
    let formFields = document.querySelectorAll('#contact-form input, #contact-form textarea');
    let isValid = true;

    // Check if all required fields are filled
    for (let i = 0; i < formFields.length; i++) {
      if (formFields[i].hasAttribute('required') && formFields[i].value === '') {
        isValid = false;
        break;
      }
    }

    if (isValid) {
      successMessage.style.display = 'block';

      setTimeout(function () {
        successMessage.style.display = 'none';

        // Reset form fields after 3 seconds
        for (let i = 0; i < formFields.length; i++) {
          formFields[i].value = '';
        }
      }, 3000);
    }
  }

    function toggleReviewForm() {
         let reviewFormContainer = document.getElementById("reviewFormContainer");
         let reviewButton = document.getElementById("reviewButton");
        if (reviewFormContainer.style.display === "none") {
            reviewFormContainer.style.display = "block";
            reviewButton.style.display = "none";
        } else {
            reviewFormContainer.style.display = "none";
            reviewButton.style.display = "block";
        }
    }
    function toggleCancel() {
         let reviewFormContainer = document.getElementById("reviewFormContainer");
         let reviewButton = document.getElementById("reviewButton");
         reviewFormContainer.style.display = "none";
         reviewButton.style.display = "block";
    }


    // Function to check if the modal should be shown
  function shouldShowModal() {
    // Check if a cookie or local storage flag exists to indicate whether the modal has been shown before
    // Change "researchModalShown" to a unique name to avoid conflicts with other cookies or local storage data
    const modalShown = document.cookie.includes("researchModalShown") || localStorage.getItem("researchModalShown");
    return !modalShown;
  }

  // Function to set the flag indicating that the modal has been shown
  function setModalShown() {
    // Set a cookie to remember that the modal has been shown
    document.cookie = "researchModalShown=true; expires=Thu, 31 Dec 2099 23:59:59 UTC; path=/";
    // Alternatively, use local storage
    // localStorage.setItem("researchModalShown", "true");
  }

  window.onload = function() {
    // Check if the modal should be shown
    if (shouldShowModal()) {
      const researchModal = new bootstrap.Modal(document.getElementById('researchModal'));
      researchModal.show();
    }
  };

  // Add an event listener to the "OK" button in the modal
  const okButton = document.getElementById("okButton");
  okButton.addEventListener("click", function() {
    setModalShown(); // Set the flag indicating that the modal has been shown
  });

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
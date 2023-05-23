document.addEventListener('DOMContentLoaded', function() {
    var formContainer = document.getElementById('form-container');
  
    formContainer.addEventListener('submit', function(event) {
      event.preventDefault();
  
      var form = event.target;
      var formData = new FormData(form);
      var url = form.getAttribute('action');
  
      fetch(url, {
        method: 'POST',
        body: formData
      })
      .then(function(response) {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Request failed.');
        }
      })
      .then(function(data) {
        var message = data.message;
        var popupContainer = document.getElementById('popup-container');
        popupContainer.textContent = message;
        popupContainer.classList.add('fade-in');
        console.log(popupContainer)
  
        setTimeout(function() {
          popupContainer.style.top = '-10%';
          popupContainer.style.opacity = '0';
        }, 3000);
      })
      .catch(function(error) {
        console.log(error);
      });
    });
  });
  
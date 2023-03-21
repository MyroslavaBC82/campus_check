function initStarRating() {
  const ratingForms = document.querySelectorAll('form.star-rating-form');

  // Add event listeners to each rating form
  ratingForms.forEach(function(form) {
    form.addEventListener('click', function(event) { 
      event.preventDefault();

      // Send rating to server
      const data = new FormData(this);
      fetch(this.action, {
        method: this.method,
        headers: { 'X-CSRFToken': this.querySelector('input[name="csrfmiddlewaretoken"]').value },
        body: data
      }).then(response => {
        if (!response.ok) {
          throw new Error('Failed to save rating');
        }
        // Do not reload the page, update rating dynamically
        const ratingValue = parseInt(data.get('rating')); // Get the rating value from the form data
        const starContainer = this.querySelector('.star-rating'); // Get the star rating container element
        starContainer.dataset.rating = ratingValue; // Set the new rating value in the dataset attribute
      }).catch(error => {
        console.error(error);
      });
    });
  });
}

// Wait for the document to load before initializing the star rating system
document.addEventListener('DOMContentLoaded', function() {
  initStarRating();
});


$(function () {
  $(".rateyo").rateYo({
    starWidth: "80px"
  }).on("rateyo.change", function (e, data) {
    var rating = data.rating;
    $(this).parent().find('.result').text('rating :'+ rating);
   });
});
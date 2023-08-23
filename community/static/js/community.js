

for(const post of posts_images){
    const postHtml = document.getElementById("post-" + post['id'] + "-img");
    if(Object.keys(post['stock_image']).length !== 0) {         // for cases that the post is old test data
        const postImage = JSON.parse(post['stock_image']);
        if ('image' in postImage && postImage['image'] !== '') {
            postHtml.src = postImage['image'];
        }
    }
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
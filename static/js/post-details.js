
// script.js
$(document).ready(function() {
  // Function for post likes
  let likeButton = $('#likeButton');
  let postId = likeButton.data('post-id');
  let profileId = likeButton.data('profile-id');

  $.ajax({
    url: 'check-like/',
    method: 'GET',
    data: {
      'post_id': postId,
      'profile_id': profileId
    },
    success: function(response) {
      if (response.liked) {
        $('#likeIcon').text('Unlike');
      } else {
        $('#likeIcon').text('Like');
      }
    }
  });

  document.getElementById('likeButton').addEventListener('click', function() {
    let profileId = this.getAttribute('data-profile-id');
    let postId = this.getAttribute('data-post-id');
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/community/like_post/' + postId + '/' + profileId + '/');
    xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));

    xhr.onload = function() {
      if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText);
        if (response.is_liked) {
          document.getElementById('likeButton').innerHTML = '(' + response.likes + ') Like';
        } else {
          document.getElementById('likeButton').innerHTML = '(' + response.likes + ') Unlike';
        }
      }
    };
    xhr.send();
  });
});

// Helper function for CSRF token
function getCookie(name) {
  let value = "; " + document.cookie;
  let parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
}

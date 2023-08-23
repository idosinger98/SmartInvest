import {StockChart} from "../../../static/js/stockChart.js";


const chart = new StockChart();
console.log(postData);
chart.loadChartFromJson(JSON.stringify(postData));
chart.drawChart('chart_container');


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
    xhr.open('POST', '/community/like_post/' + postId + '/');
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

$(document).ready(function() {
  for (let i = 1; i <= counter; i++) {
    let likesCommentIcon = $('#likesCommentIcon' + i);
    let commentId = likesCommentIcon.data('comment-id');
    let profileId = likesCommentIcon.data('profile-id');

    $.ajax({
      url: 'check-comment-like/',
      method: 'GET',
      data: {
        'comment_id': commentId,
        'profile_id': profileId
      },
      success: function(response) {
        if (response.liked) {
          likesCommentIcon.text('Unlike');
        } else {
          likesCommentIcon.text('Like');
        }
      }
    });

    document.getElementById('likesCommentIcon' + i).addEventListener('click', function() {
      let profileId = this.getAttribute('data-profile-id');
      let commentId = this.getAttribute('data-comment-id');
      let xhr = new XMLHttpRequest();
      xhr.open('POST', '/community/like_comment/' + commentId + '/');

      // Get the CSRF token from the cookie and set it in the request header
      let csrfToken = getCommentCookie('csrftoken');
      xhr.setRequestHeader('X-CSRFToken', csrfToken);

      xhr.onload = function() {
        if (xhr.status === 200) {
          let response = JSON.parse(xhr.responseText);
          let likesCommentIcon = document.getElementById('likesCommentIcon' + i);
          let likesCommentCounter = document.getElementById('likesCommentCounter' + i);
          likesCommentCounter.innerHTML = '(' + response.likes + ')';
          if (response.is_liked) {
            likesCommentIcon.innerHTML = 'Like';
          } else {
            likesCommentIcon.innerHTML = 'Unlike';
          }
        }
      };
      xhr.send();
    });
  }
});

// Function to get the CSRF token from the cookie
function getCommentCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Check if the cookie name matches the expected format for the CSRF token
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function confirmDelete(post_id, comment_id, profile_id) {
    const csrfToken = getCookie('csrftoken');
    const confirmation = confirm("Are you sure you want to delete this comment?");
    if (confirmation) {
        fetch(`/community/delete-comment/${post_id}/${comment_id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            if (response.ok) {
                // Reload the page or perform any necessary actions
                window.location.reload();
            } else {
                console.error('Error deleting comment:', response.status);
                // Handle the error or display an appropriate message to the user
            }
        })
        .catch(error => {
            console.error('Error deleting comment:', error);
            // Handle the error or display an appropriate message to the user
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const deleteCommentButtons = document.querySelectorAll('.deleteComment');
    deleteCommentButtons.forEach(button => {
        button.addEventListener('click', function() {
            let comment_id = this.getAttribute('data-comment-id');
            let post_id = this.getAttribute('data-post-id');
            let profile_id = this.getAttribute('data-profile-id');
            confirmDelete(post_id, comment_id, profile_id);
        });
    });
});

$(document).ready(function() {
  $('#commentForm').submit(function(event) {
    event.preventDefault(); // Prevent the default form submission

    // Retrieve the comment content and post ID
    let commentContent = $('#commentInput').val();
    let post_id = postId; // Replace with the actual post ID
    let profile_id = userId;

    // Send an AJAX request to the comment creation URL
    $.ajax({

      method: 'POST',
      data: {
        'content': commentContent,
        'post_id': post_id,
        'profile_id': profile_id
      },
      success: function(response) {
        window.location.reload();
      }
    });
  });
});
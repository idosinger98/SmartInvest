    document.addEventListener('DOMContentLoaded', function () {
        const deleteLinks = document.querySelectorAll('.delete-link');

        deleteLinks.forEach(function (link) {
            link.addEventListener('click', function (event) {
                const deleteUrl = link.getAttribute('data-delete-url');
                const confirmed = window.confirm('Are you sure you want to delete this analysis?');

                if (!confirmed) {
                    event.preventDefault();
                } else {
                    window.location.href = deleteUrl;
                }
            });
        });
    });
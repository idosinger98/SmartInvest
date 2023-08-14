  function showConfirmation() {
            if (confirm("Are you sure you want to delete your account?")) {
                document.getElementById("delete-account-form").submit();
            }
        }

    $(document).ready(function() {
        $('#uploadBtn').click(function() {
            $('#fileInput').click();
        });

        // When a new file is selected, update the profile image with the selected file (optional).
        $('#fileInput').change(function() {
            var file = this.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function(event) {
                    $('#profileImage').attr('src', event.target.result);
                };
                reader.readAsDataURL(file);
            }
        });

        // Form submission event handling
        $('#updateProfileForm').submit(function(event) {
            // Prevent the default form submission behavior
            event.preventDefault();

            // Optionally, you can add code here to handle form submission via AJAX if needed.
            // For now, I'll assume you want to submit the form traditionally.
            this.submit();
        });
    });
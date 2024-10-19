document.addEventListener('DOMContentLoaded', function() {
    // Confirm task deletion
    document.querySelectorAll('.btn-danger').forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm("Are you sure you want to delete this task?")) {
                event.preventDefault();
            }
        });
    });

    // Confirm task status update
    document.querySelectorAll('.btn-success, .btn-warning, .btn-info').forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm(`Mark this task as "${this.textContent.trim()}"?`)) {
                event.preventDefault();
            }
        });
    });
});

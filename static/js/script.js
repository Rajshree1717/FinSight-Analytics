// Confirm delete
function confirmDelete(message = "Are you sure you want to delete this record?") {
    return confirm(message);
}

// Show current year in footer (optional)
document.addEventListener("DOMContentLoaded", function () {
    const year = document.getElementById("currentYear");
    if (year) {
        year.textContent = new Date().getFullYear();
    }
});
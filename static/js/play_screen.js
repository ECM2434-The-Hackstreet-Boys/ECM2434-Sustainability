document.addEventListener('DOMContentLoaded', function () {
    // will open a qr scanner in the future
    document.getElementById('my-button').addEventListener('click', function () {
        alert("Open Camera button clicked!");
    });
});

// Function to handle the quiz link click event
function quizClicked(e) {
    console.log(e.detail.message);
    // Redirect to the quiz page
    window.location.assign("/quiz");
}

// Add event listener for the custom event
document.addEventListener('quizLinkClicked', quizClicked);
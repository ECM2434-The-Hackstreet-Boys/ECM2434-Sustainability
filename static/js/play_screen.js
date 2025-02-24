
// Function to handle the quiz link click event
function quizClicked(e) {
    console.log(e.detail.message);
    // Redirect to the quiz page
    window.location.assign("/quiz");
}

// Add event listener for the custom event
document.addEventListener('quizLinkClicked', quizClicked);
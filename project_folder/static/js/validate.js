document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const signupPage = document.querySelector(".signup-page");

    signupPage.style.backgroundImage = "url('/static/webimages/image1.png')";
    signupPage.style.backgroundSize = "cover";  // Ensures the background covers the entire container
    signupPage.style.backgroundPosition = "center";  // Centers the background image
    signupPage.style.backgroundAttachment = "fixed";

    form.addEventListener("submit", (event) => {
        const name = document.querySelector("#name").value.trim();
        const email = document.querySelector("#email").value.trim();
        const password = document.querySelector("#password").value.trim();

        // Clear previous error messages
        const errorDiv = document.querySelector("#error-message");
        if (errorDiv) errorDiv.textContent = "";

        if (!name || !email || !password) {
            displayError("All fields are required.", event);
        } else if (!validateEmail(email)) {
            displayError("Please enter a valid email address.", event);
        } else if (password.length < 6) {
            displayError("Password must be at least 6 characters long.", event);
        }
    });

    function displayError(message, event) {
        event.preventDefault();
        const errorDiv = document.querySelector("#error-message") || createErrorDiv();
        errorDiv.textContent = message;
    }

    function createErrorDiv() {
        const errorDiv = document.createElement("div");
        errorDiv.id = "error-message";
        errorDiv.style.color = "red";
        form.insertAdjacentElement("beforebegin", errorDiv);
        return errorDiv;
    }

    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
});


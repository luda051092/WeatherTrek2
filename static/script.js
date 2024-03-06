document.addEventListener('DOMContentLoaded', function () {
    // Add event listeners when the DOM is fully loaded

    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            // Perform login form validation
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (!username || !password) {
                event.preventDefault();
                alert('Please fill in both username and password fields.');
            }
        });
    }

    if (signupForm) {
        signupForm.addEventListener('submit', function (event) {
            // Perform signup form validation
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            if (!username || !password) {
                event.preventDefault();
                alert('Please fill in both username and password fields.');
            }
        });
    }
});

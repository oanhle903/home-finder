'use strict';

// fetch('/check_login')
//   .then((response) => response.text())
//   .then((responseData) => {
//     console.log(responseData);
//     if (responseData === 'logged_in') {
//       document.querySelector('#sign-up').style.display = 'none'; // hide signup button
//       document.querySelector('#sign-in').style.display = 'none'; // hide signin button
//     }
//     else {
//       document.querySelector('#my-profile').style.display = 'none'; // hide profile
//       // TODO if user is not logged in and user click on the save button then display the login from
//     }
//   });


// show the login form when the button is clicked, and to add an overlay effect
document.getElementById('signin-button').addEventListener('click', () => {
  document.querySelector('.login-container').style.display = 'block';
  document.body.style.overflow = 'hidden'; // disable scrolling on the body
});

// hide the login form and remove the overlay when the close button is clicked
document.getElementById('in-close-button').addEventListener('click', () => {
  document.querySelector('.login-container').style.display = 'none';
});
  
// show the signup form when the button is clicked, and to add an overlay effect
document.getElementById('signup-button').addEventListener('click', () => {
  document.querySelector('.signup-container').style.display = 'block';
  document.body.style.overflow = 'hidden'; // disable scrolling on the body
});

// hide the signup form and remove the overlay when the close button is clicked
document.getElementById('up-close-button').addEventListener('click', () => {
  document.querySelector('.signup-container').style.display = 'none';
});




  
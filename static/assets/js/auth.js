

let showSignup = true;

function toggleForm() {
  const signupForm = document.getElementById('signupForm');
  const loginForm = document.getElementById('loginForm');

  if (showSignup) {
    signupForm.style.display = 'none';
    loginForm.style.display = 'block';
  } else {
    signupForm.style.display = 'block';
    loginForm.style.display = 'none';
  }

  showSignup = !showSignup;
}

async function signupFormSubmit(event) {
    event.preventDefault();
  
    const form = event.target;
    const formData = new FormData(form);
    const url = '/register';
    
    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
      });
  
      if (response.ok) {
        const result = await response.json();
        if (result.status === 'success') {
          showPopup('green', result.message);
        } else {
          showPopup('red', result.message);
        }
      } else {
        const errorResult = await response.json();
        showPopup('red', errorResult.message);  
        console.error('Server error:', response.statusText);
    }
    } catch (error) {
      showPopup('red', 'Error during fetch. Please try again.');
      console.error('Error during fetch:', error);
    }
  }
  
  function showPopup(color, message) {
    const popupWrapper = document.querySelector(`.wrapper.${color}`);
    const popupHeader = popupWrapper.querySelector('h1');
    const popupText = popupWrapper.querySelector('p');
    const popupContainer = document.getElementById('popupContainer');
    const authForm = document.getElementById("authForm");
  
    popupHeader.textContent = message ? message : 'Oops';
    popupText.textContent = message ? '' : 'Something went wrong, please try again.';

    popupContainer.style.display = 'block';
    popupWrapper.style.display = 'block';

  
    const dismissButton = popupWrapper.querySelector('button');
    dismissButton.addEventListener('click', () => {
      popupWrapper.style.display = 'none';
      popupContainer.style.display = 'none';
    });
  }

async function loginFormSubmit(event) {
event.preventDefault();

const form = event.target;
const formData = new FormData(form);
const url = '/login';

try {
  const response = await fetch(url, {
    method: 'POST',
    body: formData,
  });

  if (response.ok) {
    const result = await response.json();
    if (result.status === 'success') {
      showPopup('green', result.message);
      window.location.href = '/dashboard';
    } else {
      showPopup('red', result.message);
    }
  } else {
    const errorResult = await response.json();
    showPopup('red', errorResult.message);  
    console.error('Server error:', response.statusText);
}
} catch (error) {
  showPopup('red', 'Error during fetch. Please try again.');
  console.error('Error during fetch:', error);
}
}



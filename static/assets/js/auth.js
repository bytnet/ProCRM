

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
        showPopup('green', result.message);
      } else {
        const errorResult = await response.json();
        showPopup('red', errorResult.error);
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
  
    popupHeader.textContent = message ? message : 'Oops';
    popupText.textContent = message ? '' : 'Something went wrong, please try again.';
  
    popupWrapper.style.display = 'block';
  
    const dismissButton = popupWrapper.querySelector('button');
    dismissButton.addEventListener('click', () => {
      popupWrapper.style.display = 'none';
    });
  }

// document.getElementById('loginForm').addEventListener('submit',function(e){
//     e.preventDefault();

//     const username = document.getElementById('username').value;
//     const password = document.getElementById('password').value;

//     fetch('/login',{

//         method: 'POST',
//         headers:{
//             'Content-Type':'application/json',

//         },
//         body: JSON.stringify({
//             username: username,
//             password: password,

//         }),
//     })
// .then(Response => Response.json())
// .then(data => {
//     if(data.success){
//         console.log('Login Successful');
//     }else{
//         console.log('Login failed')
//     }

// })
// .catch((error)=>{
//     console.error('Error:',error);
// });
// });
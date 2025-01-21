const emailEl = document.getElementById('email');
const lastNameEl = document.getElementById('lastName');
const firstNameEl = document.getElementById('firstName');
const submitEl = document.getElementById('submit');
const resultEl = document.getElementById('result');
const responseEl = document.getElementById('response');

const classNameHidden = 'hidden';
const classNameSuccess = 'success';
const classNameFailure = 'failure';

function displaySuccessMessage (text) {
  resultEl.classList.remove(classNameHidden);
  resultEl.classList.remove(classNameFailure);
  resultEl.classList.add(classNameSuccess);
  responseEl.textContent = text;
}

function displayFailureMessage (text) {
  resultEl.classList.remove(classNameHidden);
  resultEl.classList.remove(classNameSuccess);
  resultEl.classList.add(classNameFailure);
  responseEl.textContent = text;
}

submitEl.addEventListener('click', () => {
  fetch('https://{API_ENDPOINT_FQDN}/contact', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: emailEl.value,
      lastName: lastNameEl.value,
      firstName: firstNameEl.value,
    }),
  }).then(response => response.text())
    .then(displaySuccessMessage)
    .catch(displayFailureMessage);
});

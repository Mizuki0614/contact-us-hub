const emailEl = document.getElementById('email');
const lastNameEl = document.getElementById('lastName');
const firstNameEl = document.getElementById('firstName');
const inquiryContentEl = document.getElementById('inquiryContent'); // 新しい入力フィールド
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
  fetch('https://00704.engineed-exam.com/contact', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'x-cloudfront-auth': 'e4c1ec56-300a-40ef-bcaa-ae55138de0b4'
    },
    body: JSON.stringify({
      email: emailEl.value,
      lastName: lastNameEl.value,
      firstName: firstNameEl.value,
      inquiry_content: inquiryContentEl.value,
    }),
  })
    .then(response => response.text())
    .then(displaySuccessMessage)
    .catch(displayFailureMessage);
});
var form = document.getElementById('create_guest_form')

var first_name = document.getElementById('id_first_name')
var last_name = document.getElementById('id_last_name')
var email = document.getElementById('id_email')
var phone_number = document.getElementById('id_phone_number')
var next_of_kin_number = document.getElementById('id_next_of_kin_number')

var csrf_token = document.getElementsByName('csrfmiddlewaretoken')


// This adds the event listener for the keyup event
first_name.addEventListener('keyup', (e)=> {
	// This gets the event value
	var firstNameValue = e.target.value;
	var feedbackArea = document.querySelector('.invalid-feedback-fn')

	// This clears the error before making an api call
	first_name.classList.remove("is-invalid");
	feedbackArea.style.display = 'none';

	// This makes sure something is beign typed in before it starts making the request
	if (firstNameValue.length > 0) {
		fetch('../validate-first-name', {
			body: JSON.stringify({'first_name': firstNameValue}),
			method: 'POST'
		})
		.then((response) => response.json())
		.then((data) => {
			// If there is a 'name_error', it adds the invalid class, makes it visible and displays the error
			if (data.name_error) {
				first_name.classList.add("is-invalid");
				feedbackArea.style.display = 'block';
				feedbackArea.innerHTML = `<p>${data.name_error}</p>`
			}
		});
	}
})

last_name.addEventListener('keyup', (e)=> {
	var lastNameValue = e.target.value;
	var feedbackArea = document.querySelector('.invalid-feedback-ln')

	last_name.classList.remove("is-invalid");
	feedbackArea.style.display = 'none';

	if (lastNameValue.length > 0) {
		fetch('../validate-last-name', {
			body: JSON.stringify({'last_name': lastNameValue}),
			method: 'POST'
		})
		.then((response) => response.json())
		.then((data) => {
			if (data.name_error) {
				last_name.classList.add("is-invalid")
				feedbackArea.style.display = 'block';
				feedbackArea.innerHTML = `<p>${data.name_error}</p>`
			}
		});
	}
})

email.addEventListener('keyup', (e)=> {
	var emailValue = e.target.value;
	var feedbackArea = document.querySelector('.invalid-feedback-em')

	email.classList.remove("is-invalid");
	feedbackArea.style.display = 'none';

	if (emailValue.length > 0) {
		fetch('../validate-email', {
			body: JSON.stringify({'email': emailValue}),
			method: 'POST'
		})
		.then((response) => response.json())
		.then((data) => {
			if (data.mail_error) {
				email.classList.add("is-invalid")
				feedbackArea.style.display = 'block';
				feedbackArea.innerHTML = `<p>${data.mail_error}</p>`
			}
		});
	}
})

phone_number.addEventListener('keyup', (e)=> {
	var phoneNumberValue = e.target.value;
	var feedbackArea = document.querySelector('.invalid-feedback-ph')

	phone_number.classList.remove("is-invalid");
	feedbackArea.style.display = 'none';

	setTimeout(checkPhoneNumber, 5000)
	function checkPhoneNumber() {
		fetch('../validate-phone-number', {
		body: JSON.stringify({'phone_number': phoneNumberValue}),
		method: 'POST'
		})
		.then((response) => response.json())
		.then((data) => {
			if (data.phone_number_error) {
				phone_number.classList.add("is-invalid")
				feedbackArea.style.display = 'block';
				feedbackArea.innerHTML = `<p>${data.phone_number_error}, ${data.length_of_string}</p>`
			}
		});
	};

})


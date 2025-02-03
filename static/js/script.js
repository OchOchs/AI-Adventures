document.addEventListener('DOMContentLoaded', function () {
    let step = 1;
    function navigateTo(path, input="", feedback="") {
        console.log('Navigiere zu', path);
        console.log('Input:', input);
        console.log('Feedback:', feedback);
        const submitBtn = document.getElementById('submit-btn');
        const optionResults = document.getElementById('option-results');
        const inputField = document.getElementById('player-input');
        
        submitBtn.disabled = true;
        optionResults.style.display = 'none';
        inputField.placeholder = "Loading...";
        
        fetch(`/${path}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `input=${encodeURIComponent(input)}&feedback=${encodeURIComponent(feedback)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.response.options) {
                optionResults.style.display = 'block';
                displayOptions(data.response.options, data.step);
                displayText(data.response.text, data.step);
                submitBtn.disabled = false;
            }
            else {
                console.error('Error: Keine Optionen erhalten');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    

    function submit() {
        const input = document.getElementById('player-input').value;
        if (step === 1) {
            navigateTo(`submit/${step}`, input);
        } else if (step === "1" || step === "2") {
            if (input !== "") {
                navigateTo(`submit/${parseInt(step) + 1}`, input, feedback=input);
            }
        }
    }

    function displayOptions(options, newStep) {
        step = newStep;
        console.log('Step:', step);
        globalOptions = options;
        const optionOptionsContainer = document.getElementById('option-options');
        optionOptionsContainer.innerHTML = '';
    
        options.forEach((option, index) => {
            const optionDiv = document.createElement('div');
            optionDiv.classList.add('option-option');
            optionDiv.innerHTML = `
                <div class="option-content">
                    <div class="option-header">
                        <h3 class="option-title">${option.title}</h3>
                    </div>
                    <div class="option-image-container">
                        <img src="${option.imageUrl}" alt="${option.title}" class="option-image">
                    </div>
                    <div class="option-description-container">
                        <p class="option-description">${option.description}</p>
                    </div>
                </div>
                <div class="option-button-container">
                    <button class="choose-option-btn" onclick="selectOption(${index})">Choose this Option</button>
                </div>
            `;
            optionOptionsContainer.appendChild(optionDiv);
        });
    }

    function displayText(text, newStep=0) {
        const textContainer = document.getElementById('story');
        const inputField = document.getElementById('player-input');
        textContainer.innerHTML += "\n\n" + text;
        if (newStep >= 3) {
            textContainer.innerHTML += "\n\n" + "You can now either choose one of these options or write your own, to continue the story.";
            inputField.placeholder = "Enter your own choice here...";
        } else {
            inputField.placeholder = "Enter your feedback here...";
        }
    }

    window.selectOption = function(index) {
        const selectedOption = globalOptions[index];
        const optionData = selectedOption.title
        displayText("You chose: " + selectedOption.title + "\n\n" + selectedOption.description);
        navigateTo(`submit/${parseInt(step) + 1}`, JSON.stringify(optionData));
    };

    document.getElementById('submit-btn').addEventListener('click', submit);
    document.getElementById('home').addEventListener('click', function(event) {
        window.location.href = '/';
    });
});
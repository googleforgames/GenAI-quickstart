const socket = io();
// global
const pageHero = document?.querySelector('.hero')
const exitBtn = document?.getElementById('exitGame')
const startGameBtn = document?.getElementById('startGame')
const loaderContainer = document?.querySelector('.loader-container')
// prompts vars
const prompts = document?.getElementById('prompts')
const promptsForms = prompts?.querySelectorAll('form')
const promptsHeader = prompts?.querySelector('.prompts__header')
// guesses vars
const guesses = document?.getElementById('guesses')
const guessesForms = guesses?.querySelectorAll('form')
const guessesHeader = guesses?.querySelector('.guesses__header')
// results vars
const results = document?.getElementById('results')
const playAgainBtn = document?.getElementById('playAgain')

// If Start Game btn exists, run click event
if(startGameBtn) {
  startGameBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const container = document.querySelector('.intro')
    const content = container.querySelector('.intro__content')
    const loader = container.querySelector('.loader')
    const playerTag = container.querySelector('.player-tag')
    const steps = document.querySelector('.intro__steps')

    // Set loading state
    container.classList.add('loading')
    content.classList.add('hidden')
    loader.classList.remove('hidden')
    playerTag.classList.remove('hidden')
    steps.classList.add('hidden')

    // Socket message
    socket.emit('startGame', 'true')

    // Set redirect
    setTimeout(() => {
      window.location.href = './index.html'
    }, 2000)
  })
}

// If Exit button exists, run click event
if(exitBtn) {
  exitBtn.addEventListener('click', (e) => {
    e.preventDefault();
    // Socket message
    socket.emit('exitGame', 'true')
    // Redirect to start page
    // window.location.href = './start.html'
  })
}

// If Play Again button exists, run click event
if(playAgainBtn) {
  playAgainBtn.addEventListener('click', (e) => {
    e.preventDefault();
    // Socket message
    socket.emit('playAgain', 'true') 
  })
}

// Prompts submit events
// If prompts form exists, run submit event for each
if(promptsForms?.length > 0) {
  promptsForms.forEach((form, index) => {
    const keyboardBtn = form.querySelector('#keyboard')
    const button = form?.querySelector('.prompts__caption-submit button')
    const input = form?.querySelector('.prompts__caption-input input[type="text"]')

    // text input control
    input.addEventListener('keyup', (e) => {
      if(e.target.value.length > 0) {
        input.parentNode.classList.add('active')
        button.removeAttribute('disabled')
      } else {
        input.parentNode.classList.remove('active')
        button.setAttribute('disabled', '')
      }
    })

    // Keyboard icon click, bring up keyboard
    if(keyboardBtn) {
      keyboardBtn?.addEventListener('click', (e) => {
        // focus and click to trigger keyboard
        e.target.nextElementSibling.focus()
        e.target.nextElementSibling.click()
      })
    }

    // Submit event on each caption
    form.addEventListener('submit', (e) => {
      e.preventDefault()
      // add submitted class
      e.target.classList.add('submitted')
      // set value
      const value = form.querySelector('input[type="text"]').value
      // emit socket message
      socket.emit('prompt', { message: value, round: index + 1 })

      // Controls states
      if (form.classList.contains('submitted')) {
        const nextEl = form.nextElementSibling
        const inputField = form.querySelector('input[type="text"]')
        const submitBtn = form.querySelector('button[type="submit"]')
        const captionNote = form.querySelector('.prompts__caption-note')

        // set disabled after submitted successfully
        form.setAttribute('disabled', '')
        inputField.setAttribute('disabled', '')
        submitBtn.setAttribute('disabled', '')
        captionNote.classList.add('hidden')

        // If next for is not submitted, remove disable
        if (nextEl !== null && !nextEl.classList.contains('submitted')) {
          const nextInputField = nextEl.querySelector('input[type="text"]')
          const nextSubmitBtn = nextEl.querySelector('button[type="submit"]')
          const nextCaptionNote = nextEl.querySelector('.prompts__caption-note')

          // Remove disable attributes
          nextEl.removeAttribute('disabled')
          nextInputField?.removeAttribute('disabled')
          nextSubmitBtn?.removeAttribute('disabled')
          nextCaptionNote?.classList.remove('hidden')
        } else {
          // Set loading state
          document.querySelector('body').classList.add('prompts-submitted')
          prompts.classList.add('hidden')
          pageHero.classList.add('hidden')
          loaderContainer.querySelector('p').innerHTML = 'Sketching and waiting for other player...'
          loaderContainer.classList.remove('hidden')
        }
      }
    })
  })
}

// If guesses form exists, run submit event for each
if(guessesForms?.length > 0) {
  guessesForms.forEach((form, index) => {
    const input = form?.querySelector('.guesses__input input[type="text"]')
    const button = form?.querySelector('.guesses__submit button')
    const keyboardBtn = form?.querySelector('#keyboard')

    // Keyboard icon click, bring up keyboard
    if(keyboardBtn) {
      keyboardBtn?.addEventListener('click', (e) => {
        // focus and click to trigger keyboard
        e.target.nextElementSibling.focus()
        e.target.nextElementSibling.click()
      })
    }

    // text input control
    input.addEventListener('keyup', (e) => {
      if(e.target.value.length > 0) {
        button.removeAttribute('disabled')
      } else {
        button.setAttribute('disabled', '')
      }
    })

    // form submit event
    form?.addEventListener('submit', (e) => {
      const nextEl = form.nextElementSibling
      const value = form.querySelector('input[type="text"]').value
      e.preventDefault()
      // set current to hidden and show next form
      e.target.classList.add('hidden')
      // emit socket message
      socket.emit('guess', { message: value, opponentId: document.getElementById('opponentId').textContent, round: document.getElementById('round').textContent});
      // if next element is hidden, show it
      // else show loading state
      if(nextEl !== null && nextEl.classList.contains('hidden')) {
        nextEl.classList.remove('hidden')
      } else {
        // set loading state
        document.querySelector('body').classList.add('guesses-submitted')
        guesses.classList.add('hidden')
        pageHero.classList.add('hidden')
        loaderContainer.querySelector('p').innerHTML = 'Calculating results and waiting for other player ...'
        loaderContainer.classList.remove('hidden')
        
        let intervalId = setInterval(checkDivValue, 200)
        function checkDivValue() {
          const getAllMyPrompts = document.getElementById('getAllMyPrompts').value;
          const getAllMyGuesses = document.getElementById('getAllMyGuesses').value;
          const getAllMyScores = document.getElementById('getAllMyScores').value;
          const getAllOpponentPrompts = document.getElementById('getAllOpponentPrompts').value;
          const getAllOpponentGuesses = document.getElementById('getAllOpponentGuesses').value;
          const getAllOpponentScores = document.getElementById('getAllOpponentScores').value;
          const myTotalScore = document.getElementById('myTotalScore').textContent;
          const opponentTotalScore = document.getElementById('opponentTotalScore').textContent;
        
          if (getAllMyPrompts === 'true' && getAllMyGuesses === 'true' && getAllMyScores === 'true' && getAllOpponentPrompts === 'true' && getAllOpponentGuesses === 'true' && getAllOpponentScores === 'true' && myTotalScore !== null && opponentTotalScore !== null) {
            if (parseFloat(myTotalScore) > parseFloat(opponentTotalScore)) {
              document.getElementById('currentPlayerResultsText').textContent = 'You won!';
            } else if (parseFloat(myTotalScore) < parseFloat(opponentTotalScore)) {
              document.getElementById('currentPlayerResultsText').textContent = 'You lost!';
            } else {
              document.getElementById('currentPlayerResultsText').textContent = 'It\'s a tie!';
            }

            document.querySelector('body').classList.remove('guesses-submitted')
            document.querySelector('body').classList.add('has-results')
            loaderContainer.classList.add('hidden')
            pageHero.classList.remove('hidden')
            results.classList.remove('hidden')
            
            clearInterval(intervalId)
          }
        }
      }
    })
  })
}

socket.on('guess_sketch_response', (data) => {
  document.querySelector('body').classList.remove('prompts-submitted')
  loaderContainer.classList.add('hidden')
  pageHero.classList.remove('hidden')
  guesses.classList.remove('hidden')
  document.getElementById('opponentId').textContent = data.opponentId;
  document.getElementById('round').textContent = data.round;
  const formId = 'guess' + data.round;
  const guessesImgDiv = document.getElementById(formId).querySelector('.guesses__img');
  const guessImage = guessesImgDiv.querySelector('img');
  guessesImgDiv.style.width = 'auto';  // Example - adjust as needed
  guessesImgDiv.style.height = 'auto';  // Optionally maintain aspect ratio
  guessesImgDiv.style.margin = '0 auto';  // Center the image
  guessImage.src = 'data:image/jpeg;base64,' + data.image;

  // polulate the prompt image for opponent
  const promptDivId = 'opponentPlayerPrompt' + data.round;
  const promptImgDivId = 'opponnentPlayerPromptImg' + data.round;
  const promptDiv = document.getElementById(promptDivId);
  const promptImgDiv = document.getElementById(promptImgDivId);

  promptDiv.textContent = data.prompt;
  promptImgDiv.style.width = 'auto';  // Example - adjust as needed
  promptImgDiv.style.height = 'auto';  // Optionally maintain aspect ratio
  promptImgDiv.style.margin = '0 auto';  // Center the image
  promptImgDiv.src = 'data:image/jpeg;base64,' + data.image;
  if (data.round === 3) {
    document.getElementById('getAllOpponentPrompts').value = 'true';
  }
});

socket.on('prompt_response', (data) => {
  const promptDivId = 'currentPlayerPrompt' + data.round;
  const promptImgDivId = 'currentPlayerPromptImg' + data.round;
  const promptDiv = document.getElementById(promptDivId);
  const promptImgDiv = document.getElementById(promptImgDivId);

  promptDiv.textContent = data.prompt;
  promptImgDiv.style.width = 'auto';  // Example - adjust as needed
  promptImgDiv.style.height = 'auto';  // Optionally maintain aspect ratio
  promptImgDiv.style.margin = '0 auto';  // Center the image
  promptImgDiv.src = 'data:image/jpeg;base64,' + data.image;
  if (data.round === 3) {
    document.getElementById('getAllMyPrompts').value = 'true';
  }
});

socket.on('guess_response', (data) => {
  const currentPlayerGuessImgDivId = 'currentPlayerGuessImg' + data.round;
  const opponentPlayerGuessImgDivId = 'opponnentPlayerGuessImg' + data.round;
  const currentPlayerGuessParagraphDivId = 'currentPlayerGuess' + data.round;
  const opponentPlayerGuessParagraphDivId = 'opponnentPlayerGuess' + data.round;

  let guessImgDiv;
  let guessParagraphDiv;
  if (data.from === 'myself') {
    guessImgDiv = document.getElementById(currentPlayerGuessImgDivId);
    guessParagraphDiv = document.getElementById(currentPlayerGuessParagraphDivId);
    if (data.round === 3) {
      document.getElementById('getAllMyGuesses').value = 'true';
    }
  } else {
    guessImgDiv = document.getElementById(opponentPlayerGuessImgDivId);
    guessParagraphDiv = document.getElementById(opponentPlayerGuessParagraphDivId);
    if (data.round === 3) {
      document.getElementById('getAllOpponentGuesses').value = 'true';
    }
  }

  guessParagraphDiv.textContent = data.guess;
  guessImgDiv.style.width = 'auto';  // Example - adjust as needed
  guessImgDiv.style.height = 'auto';  // Optionally maintain aspect ratio
  guessImgDiv.style.margin = '0 auto';  // Center the image
  guessImgDiv.src = 'data:image/jpeg;base64,' + data.image;
});

socket.on('score_response', (data) => {
  const currentPlayerGuessPercentageDivId = 'currentPlayerGuessPercentage' + data.round;
  const opponentPlayerGuessPercentageDivId = 'opponnentPlayerGuessPercentage' + data.round;

  let guessPercentDiv;
  if (data.from === 'myself') {
    guessPercentDiv = document.getElementById(currentPlayerGuessPercentageDivId);
  } else {
    guessPercentDiv = document.getElementById(opponentPlayerGuessPercentageDivId);
  }

  const constPerctage = data.score * 100;
  guessPercentDiv.textContent = constPerctage + "%";

  if (data.from === 'myself') {
    if (data.round === 3) {
      document.getElementById('getAllMyScores').value = 'true';
      let myTotalScore = 0.0;
      for (let i = 1; i <= 3; i++) {
        const currentPlayerGuessPercentageDivId = 'currentPlayerGuessPercentage' + i;
        const currentScoreString = document.getElementById(currentPlayerGuessPercentageDivId).textContent.slice(0, -1);
        const currentScore = parseFloat(currentScoreString);
        myTotalScore += currentScore;
      }
      document.getElementById('myTotalScore').textContent = myTotalScore;
    }
  } else {
    if (data.round === 3) {
      document.getElementById('getAllOpponentScores').value = 'true';
      let opponentTotalScore = 0.0;
      for (let i = 1; i <= 3; i++) {
        const opponnentPlayerGuessPercentageDivId = 'opponnentPlayerGuessPercentage' + i;
        const currentScoreString = document.getElementById(opponnentPlayerGuessPercentageDivId).textContent.slice(0, -1);
        const currentScore = parseFloat(currentScoreString);
        opponentTotalScore += currentScore;
      }
      document.getElementById('opponentTotalScore').textContent = opponentTotalScore;
    }
  }
});

socket.on('frontend_url', (data) => {
  // Redirect to start page
  window.location.href = "http://" + data.frontendURL; 
});
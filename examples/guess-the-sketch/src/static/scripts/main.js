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
    // Redirect to start page
    // window.location.href = './start.html'
  })
}

socket.on('llm_response', (data) => {
  document.querySelector('body').classList.remove('prompts-submitted')
  loaderContainer.classList.add('hidden')
  pageHero.classList.remove('hidden')
  guesses.classList.remove('hidden')
  document.getElementById('opponentId').textContent = data.opponentId;
  document.getElementById('round').textContent = data.round;
  const formId = 'guess' + data.round;
  const guessesImgDiv = document.getElementById(formId).querySelector('.guesses__img');
  while (guessesImgDiv.firstChild) {
    guessesImgDiv.removeChild(guessesImgDiv.firstChild);
  }
  const img = new Image();
  img.src = 'data:image/jpeg;base64,' + data.image;
  img.style.width = '900px';  // Example - adjust as needed
  img.style.height = 'auto';  // Optionally maintain aspect ratio
  guessesImgDiv.appendChild(img);

  // polulate the prompt image for opponent
  const divId = '.results__item' + data.round;
  const otherPlayerPromptDivParagraph = document.querySelector('.results__prompts-them').querySelector(divId).querySelector('.results__item-img p');
  const otherPlayerPromptDivImgArea = document.querySelector('.results__prompts-them').querySelector(divId).querySelector('.results__item-img');
  const image = otherPlayerPromptDivImgArea.querySelector('img');
  otherPlayerPromptDivParagraph.textContent = data.prompt;
  otherPlayerPromptDivImgArea.style.width = 'auto';  // Example - adjust as needed
  otherPlayerPromptDivImgArea.style.height = 'auto';  // Optionally maintain aspect ratio
  image.src = 'data:image/jpeg;base64,' + data.image;
});

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
          loaderContainer.querySelector('p').innerHTML = 'Sketching...'
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
        loaderContainer.querySelector('p').innerHTML = 'Calculating results...'
        loaderContainer.classList.remove('hidden')
        
        // NOTE: Will need to update based on actual callback
        // Remove of loading state, goes to next phase 
        setTimeout(() => {
          document.querySelector('body').classList.remove('guesses-submitted')
          document.querySelector('body').classList.add('has-results')
          loaderContainer.classList.add('hidden')
          pageHero.classList.remove('hidden')
          results.classList.remove('hidden')
        }, 2000);
      }
    })
  })
}

// socket.on('guess_input_finish', (data) => {
//   document.querySelector('body').classList.remove('guesses-submitted')
//   document.querySelector('body').classList.add('has-results')
//   loaderContainer.classList.add('hidden')
//   pageHero.classList.remove('hidden')
//   results.classList.remove('hidden')

// });

socket.on('prompt_response', (data) => {
  const divId = '.results__item' + data.round;
  const promptsImgDivParagraph = document.querySelector('.results__prompts-you').querySelector(divId).querySelector('.results__item-img p');
  const promptsImgDivImgArea = document.querySelector('.results__prompts-you').querySelector(divId).querySelector('.results__item-img');
  promptsImgDivParagraph.textContent = data.prompt
  const image = promptsImgDivImgArea.querySelector('img');
  promptsImgDivImgArea.style.width = 'auto';  // Example - adjust as needed
  promptsImgDivImgArea.style.height = 'auto';  // Optionally maintain aspect ratio
  image.src = 'data:image/jpeg;base64,' + data.image;
});

socket.on('guess_response', (data) => {
  const divId = '.results__item' + data.round;
  let guessImgDiv;
  if (data.from === 'myself') {
    guessImgDiv = document.querySelector('.results__guesses-you').querySelector(divId);
  } else {
    guessImgDiv = document.querySelector('.results__guesses-them').querySelector(divId);
  }
  const guessImgDivParagraph = guessImgDiv.querySelector('.results__item-img p');
  const guessImgDivImgArea = guessImgDiv.querySelector('.results__item-img');

  guessImgDivParagraph.textContent = data.guess;
  const image = guessImgDivImgArea.querySelector('img');
  guessImgDivImgArea.style.width = 'auto';  // Example - adjust as needed
  guessImgDivImgArea.style.height = 'auto';  // Optionally maintain aspect ratio
  image.src = 'data:image/jpeg;base64,' + data.image;
});
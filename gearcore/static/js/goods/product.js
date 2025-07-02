function getCsrfToken(form) {
    const csrfTokenInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
    return csrfTokenInput ? csrfTokenInput.value : null;
}

async function makeRequest(url, data, csrfToken) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP помилка! статус: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Помилка запиту:', error);
        throw error;
    }
}


function updateImagesPreview(newSrcs) {
  const wrapperImages = document.querySelector('.carousel-inner');
  const currentItems = wrapperImages.querySelectorAll('.carousel-item');

  // Обновляем существующие слайды
  newSrcs.forEach((src, index) => {
    if (currentItems[index]) {
      const img = currentItems[index].querySelector('img');
      if (img) img.src = src;
    } else {
      // Добавляем новые слайды, если не хватает
      const item = document.createElement('div');
      item.classList.add('carousel-item');
      if (index === 0 && currentItems.length === 0) {
        item.classList.add('active');
      }

      const img = document.createElement('img');
      img.src = src;
      img.className = 'd-block w-100';
      img.alt = `Image ${index + 1}`;

      item.appendChild(img);
      wrapperImages.appendChild(item);
    }
  });

  // Видалення зайвих слайдів, якщо такі є
  if (newSrcs.length < currentItems.length) {
    for (let i = newSrcs.length; i < currentItems.length; i++) {
        if(currentItems[i].classList.contains('active')){ //  Якщо раптом "зайвий" слайд виявиться "active"
            currentItems[0].classList.add('active')
        }
      wrapperImages.removeChild(currentItems[i]);
    }
  }
}

function changeBtnActive(activeBtn){
    document.querySelectorAll('.color-btn')?.forEach(btn=>{
        btn.classList.remove('active')
    })

    activeBtn.classList.add('active')
}

const form = document.querySelector('#colorForm')

form?.addEventListener('submit', async function (event) {
    event.preventDefault()

    const form = event.target;
    const csrfToken = getCsrfToken(form);
    const variantId = event.submitter?.dataset?.variantId


    const action = form.getAttribute('action')
    const response = await makeRequest(action, {"variantId": variantId}, csrfToken)
    changeBtnActive(event.submitter)
    updateImagesPreview(response.data)
})




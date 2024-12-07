document.addEventListener("DOMContentLoaded", () => {
  const directionFormsContainer = document.querySelector("#direction-forms")
  const addButton = document.querySelector("#add-direction-button")
  const totalForms = document.querySelector("#id_directions-TOTAL_FORMS")

  if (directionFormsContainer && addButton && totalForms) {
    addButton.addEventListener("click", (event) => {
      event.preventDefault()

      const formIndex = totalForms.value
      const lastItem = directionFormsContainer.querySelector(".direction-item:last-child")
      const newForm = lastItem ? lastItem.cloneNode(true) : null

      if (!newForm) return

      newForm.innerHTML = newForm.innerHTML.replace(/-\d+-/g, `-${formIndex}-`)

      newForm.querySelectorAll("input, textarea").forEach((input) => {
        if (input.type !== "hidden") {
          input.value = ""
        }
      })

      directionFormsContainer.querySelector("#sortable-directions").appendChild(newForm)
      totalForms.value = parseInt(formIndex) + 1
      updateStepNumbers()
    })

    directionFormsContainer.addEventListener("click", (event) => {
      if (event.target.classList.contains("remove-direction-button")) {
        event.preventDefault()
        const formToRemove = event.target.closest(".direction-item")
        const hasValue = Array.from(formToRemove.querySelectorAll("input, textarea")).some((input) => input.value.trim() !== "")

        if (!hasValue || confirm("This step has content. Are you sure you want to remove it?")) {
          formToRemove.remove()
          totalForms.value = parseInt(totalForms.value) - 1
          updateStepNumbers()
        }
      }
    })

    function updateStepNumbers() {
      const allForms = directionFormsContainer.querySelectorAll(".direction-item")
      allForms.forEach((item, index) => {
        const stepLabel = item.querySelector(".step-label")
        const stepInput = item.querySelector('input[name*="step_number"]')

        if (stepLabel) stepLabel.textContent = `Step ${index + 1}`

        if (stepInput) stepInput.value = index + 1

        const inputs = item.querySelectorAll("input, textarea")
        inputs.forEach((input) => {
          const name = input.getAttribute("name")
          if (name) {
            const newName = name.replace(/directions-\d+-/, `directions-${index}-`)
            input.setAttribute("name", newName)
          }
        })
      })

      totalForms.value = directionFormsContainer.querySelectorAll(".direction-item").length
    }

    const sortableList = document.getElementById("sortable-directions")
    if (sortableList) {
      new Sortable(sortableList, {
        animation: 150,
        onEnd: function () {
          const items = sortableList.querySelectorAll(".direction-item")
          items.forEach((item, index) => {
            const stepLabel = item.querySelector(".step-label")
            const stepInput = item.querySelector('input[name*="step_number"]')

            if (stepLabel) stepLabel.textContent = `Step ${index + 1}`
            if (stepInput) stepInput.value = index + 1

            const inputs = item.querySelectorAll("input, textarea")
            inputs.forEach((input) => {
              const name = input.getAttribute("name")
              if (name) {
                const newName = name.replace(/directions-\d+-/, `directions-${index}-`)
                input.setAttribute("name", newName)
              }
            })
          })

          totalForms.value = items.length
        },
      })
    }
  }
})

document.addEventListener("DOMContentLoaded", () => {
  const ingredientFormsContainer = document.querySelector("#ingredient-forms")
  const addIngredientButton = document.querySelector("#add-ingredient-button")
  const totalIngredientForms = document.querySelector("#id_ingredients-TOTAL_FORMS")

  if (ingredientFormsContainer && addIngredientButton && totalIngredientForms) {
    addIngredientButton.addEventListener("click", (event) => {
      event.preventDefault()

      const formIndex = totalIngredientForms.value
      const newForm = ingredientFormsContainer.querySelector("li:last-child").cloneNode(true)

      newForm.innerHTML = newForm.innerHTML.replace(/-\d+-/g, `-${formIndex}-`)

      newForm.querySelectorAll("input").forEach((input) => {
        input.value = ""
      })

      ingredientFormsContainer.appendChild(newForm)
      totalIngredientForms.value = parseInt(formIndex) + 1
    })

    ingredientFormsContainer.addEventListener("click", (event) => {
      if (event.target.classList.contains("remove-ingredient-button")) {
        event.preventDefault()
        const formToRemove = event.target.closest("li")
        formToRemove.remove()
        totalIngredientForms.value = parseInt(totalIngredientForms.value) - 1
      }
    })
  }
})

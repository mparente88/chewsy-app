document.addEventListener("DOMContentLoaded", () => {
  const directionFormsContainer = document.querySelector("#direction-forms")
  const addButton = document.querySelector("#add-direction-button")
  const totalForms = document.querySelector("#id_directions-TOTAL_FORMS")

  if (directionFormsContainer && addButton && totalForms) {
    // Add a new direction form
    addButton.addEventListener("click", (event) => {
      event.preventDefault()

      // Clone the last form and update its index
      const formIndex = totalForms.value
      const newForm = directionFormsContainer.lastElementChild.cloneNode(true)

      // Update the form index in input names and IDs
      newForm.innerHTML = newForm.innerHTML.replace(/-__prefix__-/g, `-${formIndex}-`)

      // Clear the values of inputs in the cloned form
      newForm.querySelectorAll("input").forEach((input) => {
        input.value = ""
      })

      directionFormsContainer.appendChild(newForm)
      totalForms.value = parseInt(formIndex) + 1 // Increment the total forms count
    })

    // Enable removing a direction form
    directionFormsContainer.addEventListener("click", (event) => {
      if (event.target.classList.contains("remove-direction-button")) {
        event.preventDefault()

        // Only remove if more than one form remains
        const allForms = directionFormsContainer.querySelectorAll(".direction-form")
        if (allForms.length > 1) {
          event.target.closest(".direction-form").remove()
          totalForms.value = parseInt(totalForms.value) - 1 // Decrement the total forms count
        }
      }
    })
  }
})

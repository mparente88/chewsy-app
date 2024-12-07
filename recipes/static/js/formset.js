// static/js/formset.js

document.addEventListener("DOMContentLoaded", () => {
  const directionFormsContainer = document.querySelector("#direction-forms")
  const addDirectionButton = document.querySelector("#add-direction-button")
  const totalForms = document.querySelector("#id_directions-TOTAL_FORMS")
  const sortableList = document.getElementById("sortable-directions")

  if (directionFormsContainer && addDirectionButton && totalForms && sortableList) {
    // Function to create a new direction form
    function createNewDirectionForm(index) {
      const newForm = document.createElement("li")
      newForm.classList.add("direction-item")
      newForm.innerHTML = `
        <div class="direction-form">
          <span class="step-label">Step ${index + 1}</span>
          <textarea name="directions-${index}-description" id="id_directions-${index}-description"></textarea>
          <input type="hidden" name="directions-${index}-id" id="id_directions-${index}-id" />
          <input type="hidden" name="directions-${index}-step_number" id="id_directions-${index}-step_number" value="${index + 1}" />
          <input type="hidden" name="directions-${index}-DELETE" id="id_directions-${index}-DELETE" />
          <button type="button" class="remove-direction-button">Remove</button>
        </div>
      `
      return newForm
    }

    // Add a new direction form
    addDirectionButton.addEventListener("click", (event) => {
      event.preventDefault()

      const formIndex = parseInt(totalForms.value, 10)
      const newForm = createNewDirectionForm(formIndex)

      sortableList.appendChild(newForm)
      totalForms.value = formIndex + 1
      updateStepNumbers()
    })

    // Remove a direction form
    directionFormsContainer.addEventListener("click", (event) => {
      if (event.target.classList.contains("remove-direction-button")) {
        event.preventDefault()

        const formToRemove = event.target.closest(".direction-item")
        const hasValue = formToRemove.querySelector("textarea").value.trim() !== ""

        if (!hasValue || confirm("This step has content. Are you sure you want to remove it?")) {
          const deleteInput = formToRemove.querySelector('input[name*="DELETE"]')
          if (deleteInput) {
            // Existing form: mark for deletion and hide
            deleteInput.checked = true
            formToRemove.style.display = "none"
          } else {
            // New form: remove from DOM
            formToRemove.remove()
            totalForms.value = parseInt(totalForms.value, 10) - 1
          }
          updateStepNumbers()
        }
      }
    })

    // Update step numbers and form indices, skipping deleted forms
    function updateStepNumbers() {
      const allForms = Array.from(sortableList.querySelectorAll(".direction-item"))
      let activeFormIndex = 0 // Counter for active (non-deleted) forms

      allForms.forEach((item, index) => {
        const deleteInput = item.querySelector('input[name*="DELETE"]')
        if (deleteInput && deleteInput.checked) {
          // Skip forms marked for deletion
          return
        }

        // Update step number display
        const stepLabel = item.querySelector(".step-label")
        if (stepLabel) {
          stepLabel.textContent = `Step ${activeFormIndex + 1}`
        }

        // Update the hidden step_number input
        const stepInput = item.querySelector('input[name*="step_number"]')
        if (stepInput) {
          stepInput.value = activeFormIndex + 1
        }

        // Update textarea name and id
        const textarea = item.querySelector("textarea")
        if (textarea) {
          textarea.name = `directions-${activeFormIndex}-description`
          textarea.id = `id_directions-${activeFormIndex}-description`
        }

        // Update hidden id field
        const idInput = item.querySelector('input[name*="id"]')
        if (idInput) {
          idInput.name = `directions-${activeFormIndex}-id`
          idInput.id = `id_directions-${activeFormIndex}-id`
        }

        // Update hidden DELETE field
        const deleteField = item.querySelector('input[name*="DELETE"]')
        if (deleteField) {
          deleteField.name = `directions-${activeFormIndex}-DELETE`
          deleteField.id = `id_directions-${activeFormIndex}-DELETE`
        }

        activeFormIndex += 1
      })

      // Update the total number of forms to only count active forms
      totalForms.value = activeFormIndex
    }

    // Initialize Sortable.js for drag-and-drop reordering
    new Sortable(sortableList, {
      animation: 150,
      onEnd: function () {
        updateStepNumbers()
      },
    })

    // Initial update to ensure form indices are correct on page load
    updateStepNumbers()
  } else {
    console.warn("Required elements for managing direction forms are missing.")
  }
})

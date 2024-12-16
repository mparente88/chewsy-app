document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".delete-tag-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const tagId = this.getAttribute("data-id")
      if (confirm("Are you sure you want to delete this tag?")) {
        fetch(`/superuser/tags/delete/${tagId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              document.getElementById(`tag-${tagId}`).remove()
              alert(data.message)
            } else {
              alert(data.message)
            }
          })
      }
    })
  })

  document.querySelectorAll(".edit-tag-btn").forEach((button) => {
    button.addEventListener("click", function () {
      const tagId = this.getAttribute("data-id")
      const tagName = this.getAttribute("data-name")
      const tagCategory = this.getAttribute("data-category")

      const newName = prompt("Edit tag name:", tagName)
      const newCategory = prompt("Edit tag category:", tagCategory)

      if (newName && newCategory) {
        fetch(`/superuser/tags/edit/${tagId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: new URLSearchParams({
            name: newName,
            category: newCategory,
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              const tagElement = document.getElementById(`tag-${tagId}`)
              tagElement.querySelector(".tag-name").textContent = newName
              alert(data.message)
            } else {
              alert(data.message)
            }
          })
      }
    })
  })

  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";")
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }
})

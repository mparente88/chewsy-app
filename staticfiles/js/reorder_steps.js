document.addEventListener("DOMContentLoaded", function () {
  let list = document.getElementById("instruction-list")
  if (!list) return

  let sortable = Sortable.create(list, {
    animation: 150,
    handle: ".drag-handle",
  })

  document.getElementById("reorder-form").addEventListener("submit", function (e) {
    e.preventDefault()
    let order = []
    let items = list.querySelectorAll("li")
    items.forEach(function (item) {
      order.push(item.getAttribute("data-id"))
    })

    let existingInputs = document.querySelectorAll('input[name="order[]"]')
    existingInputs.forEach(function (input) {
      input.remove()
    })

    order.forEach(function (id) {
      let input = document.createElement("input")
      input.type = "hidden"
      input.name = "order[]"
      input.value = id
      this.appendChild(input)
    }, this)

    this.submit()
  })
})

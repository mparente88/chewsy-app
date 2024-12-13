document.addEventListener("DOMContentLoaded", function () {
  const filterToggle = document.getElementById("filter-toggle")
  const filterContainer = document.getElementById("filter-container")

  filterToggle.addEventListener("click", function () {
    if (filterContainer.style.display === "none" || filterContainer.style.display === "") {
      filterContainer.style.display = "block"
    } else {
      filterContainer.style.display = "none"
    }
  })
})

document.addEventListener("DOMContentLoaded", function () {
  const tagField = document.querySelector("#id_tags")
  if (tagField) {
    $(tagField).select2({
      placeholder: "Select tags",
      allowClear: true,
      width: "100%",
    })
  }
})

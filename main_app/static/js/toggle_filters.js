document.addEventListener("DOMContentLoaded", function () {
  const filterToggle = document.getElementById("filter-toggle")
  const filterContainer = document.getElementById("filter-container")

  if (filterToggle && filterContainer) {
    filterToggle.addEventListener("click", function () {
      if (filterContainer.style.display === "none" || filterContainer.style.display === "") {
        filterContainer.style.display = "block"
      } else {
        filterContainer.style.display = "none"
      }
    })
  } else {
    console.log("Filter elements not found")
  }
})

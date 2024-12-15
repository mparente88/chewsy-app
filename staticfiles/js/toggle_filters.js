document.addEventListener("DOMContentLoaded", function () {
  const filterToggle = document.getElementById("filter-toggle")
  const filterContainer = document.getElementById("filter-container")
  const filterIcon = document.getElementById("filter-icon")

  if (filterToggle && filterContainer && filterIcon) {
    filterToggle.addEventListener("click", function () {
      const isShowing = filterContainer.classList.contains("show")
      filterContainer.classList.toggle("show", !isShowing)
      filterToggle.setAttribute("aria-expanded", !isShowing)
      filterIcon.style.transform = !isShowing ? "rotate(180deg)" : "rotate(0deg)"
    })
  } else {
    console.log("Filter elements not found")
  }
})

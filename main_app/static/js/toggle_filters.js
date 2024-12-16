document.addEventListener("DOMContentLoaded", function () {
  const filterToggle = document.getElementById("filter-toggle")
  const filterContainer = document.getElementById("filter-container")
  const filterIcon = document.getElementById("filter-icon")

  if (filterToggle && filterContainer && filterIcon) {
    filterContainer.classList.remove("show")
    filterToggle.setAttribute("aria-expanded", "false")
    filterIcon.style.transform = "rotate(0deg)"

    filterToggle.addEventListener("click", function () {
      const isShowing = filterContainer.classList.contains("show")

      filterContainer.classList.toggle("show", !isShowing)

      filterToggle.setAttribute("aria-expanded", !isShowing)

      if (!isShowing) {
        filterIcon.style.transform = "rotate(180deg)"
      } else {
        filterIcon.style.transform = "rotate(0deg)"
      }
    })
  } else {
    console.error("Filter elements not found: filter-toggle, filter-container, or filter-icon is missing.")
  }
})

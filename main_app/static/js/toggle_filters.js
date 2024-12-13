document.addEventListener("DOMContentLoaded", function () {
  const filterToggle = document.getElementById("filter-toggle")
  const filterContainer = document.getElementById("filter-container")
  const filterIcon = document.getElementById("filter-icon")

  if (filterToggle && filterContainer && filterIcon) {
    filterToggle.addEventListener("click", function () {
      const isHidden = filterContainer.style.display === "none" || filterContainer.style.display === ""
      filterContainer.style.display = isHidden ? "block" : "none"
      filterToggle.setAttribute("aria-expanded", isHidden)
      filterIcon.style.transform = isHidden ? "rotate(180deg)" : "rotate(0deg)"
    })
  } else {
    console.log("Filter elements not found")
  }
})

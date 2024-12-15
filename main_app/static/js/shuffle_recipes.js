document.addEventListener("DOMContentLoaded", function () {
  const shuffleButton = document.getElementById("shuffle-featured-btn")
  const featuredRecipeContainer = document.querySelector(".featured-recipe .recipe-card.featured")

  if (shuffleButton && featuredRecipeContainer) {
    shuffleButton.addEventListener("click", function () {
      fetch("/shuffle-recipes/")
        .then((response) => response.json())
        .then((data) => {
          const recipe = data.recipe
          if (recipe) {
            const img = featuredRecipeContainer.querySelector("img")
            const titleLink = featuredRecipeContainer.querySelector(".recipe-info h3 a")
            const infoPara = featuredRecipeContainer.querySelector(".recipe-info p")

            img.src = recipe.image
            img.alt = recipe.title
            titleLink.href = `/recipe/${recipe.id}/`
            titleLink.textContent = recipe.title
            infoPara.textContent = `Prep: ${recipe.prep_time} mins | Cook: ${recipe.cook_time} mins`
          } else {
            featuredRecipeContainer.innerHTML = `<p>No featured recipe available. Add recipes to your cookbook.</p>`
          }
        })
        .catch((error) => console.error("Error:", error))
    })
  }
})

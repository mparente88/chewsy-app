document.addEventListener("DOMContentLoaded", function () {
  const shuffleButton = document.querySelector(".shuffle-btn")
  const recipeGrid = document.querySelector(".recipe-grid")

  if (shuffleButton && recipeGrid) {
    shuffleButton.addEventListener("click", function () {
      fetch("/shuffle-recipes/")
        .then((response) => response.json())
        .then((data) => {
          recipeGrid.innerHTML = ""
          data.recipes.forEach((recipe) => {
            const recipeCard = `
                <div class="recipe-card">
                  <img src="${recipe.image}" alt="${recipe.title}" />
                  <div class="recipe-info">
                    <h2><a href="/recipe/${recipe.id}/">${recipe.title}</a></h2>
                    <p>Prep: ${recipe.prep_time} mins | Cook: ${recipe.cook_time} mins</p>
                  </div>
                </div>
              `
            recipeGrid.insertAdjacentHTML("beforeend", recipeCard)
          })
        })
        .catch((error) => console.error("Error:", error))
    })
  }
})

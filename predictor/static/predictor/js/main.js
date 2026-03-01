const form = document.querySelector("form");
    const spinner = document.getElementById("spinner");

    if (form && spinner) {
    form.addEventListener("submit", () => {
        spinner.classList.remove("d-none");
    });
}
const themeToggle = document.getElementById("themeToggle");

// if (themeToggle) {
//     themeToggle.addEventListener("click", () => {
//         document.body.classList.toggle("dark-mode");
//     });
// }
// on load
if (localStorage.getItem("theme") === "dark") {
  document.body.classList.add("dark-mode");
}

// toggle
themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  localStorage.setItem(
    "theme",
    document.body.classList.contains("dark-mode") ? "dark" : "light"
  );
});





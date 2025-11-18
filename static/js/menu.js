document.addEventListener("DOMContentLoaded", () => {
  // 🔍 Search filter
  window.searchFood = function() {
    const query = document.getElementById("searchBar").value.toLowerCase();
    document.querySelectorAll(".food-card").forEach(card => {
      const name = card.dataset.name.toLowerCase();
      card.style.display = name.includes(query) ? "block" : "none";
    });
  };

  // 📱 Navbar toggle
  window.toggleMenu = function() {
    document.querySelector('.nav-links').classList.toggle('show');
  };

  // ⬆ Scroll to top button
  const scrollBtn = document.getElementById("scrollTopBtn");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 200) scrollBtn.style.display = "block";
    else scrollBtn.style.display = "none";
  });
  scrollBtn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  // 💬 Redirect to comment page
  window.goToComment = function(itemName) {
    const encoded = encodeURIComponent(itemName);
    window.location.href = `/comment?item=${encoded}`;
  };
});

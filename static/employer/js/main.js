document.addEventListener("DOMContentLoaded", function () {
  const menuButton = document.querySelector("#open-menu");
  const closeButton = document.querySelector("#close-menu");
  const mobileMenu = document.querySelector("#mobile-menu");
  const backdrop = document.querySelector("#menu-backdrop");

  // Function to open the mobile menu
  function openMenu() {
    mobileMenu.classList.remove("hidden");
    backdrop.classList.remove("hidden");
  }

  // Function to close the mobile menu
  function closeMenu() {
    mobileMenu.classList.add("hidden");
    backdrop.classList.add("hidden");
  }

  // Event listeners for opening and closing the menu
  menuButton.addEventListener("click", openMenu);
  closeButton.addEventListener("click", closeMenu);
  

  // User drop down
  document
    .getElementById("user-dropdown")
    .addEventListener("click", function () {
      var dropdownMenu = document.getElementById("dropdown-menu");
      dropdownMenu.classList.toggle("hidden");
    });

  // Close the dropdown when clicking outside
  window.addEventListener("click", function (e) {
    var dropdownMenu = document.getElementById("dropdown-menu");
    if (!e.target.closest("#user-dropdown")) {
      dropdownMenu.classList.add("hidden");
    }
  });

  // User mobile drop down
  document.getElementById('user-mobile-dropdown').addEventListener('click', function() {
    var dropdownMenu = document.getElementById('mobile-dropdown-menu');
    dropdownMenu.classList.toggle('hidden');
  });

  // Close the dropdown when clicking outside
  window.addEventListener('click', function(e) {
    var dropdownMenu = document.getElementById('mobile-dropdown-menu');
    if (!e.target.closest('#user-mobile-dropdown')) {
      dropdownMenu.classList.add('hidden');
    }
  });
});

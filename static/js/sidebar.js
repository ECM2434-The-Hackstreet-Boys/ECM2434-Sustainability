// Author: Ethan Clapham
//
// dynamically display the navbar from the left side

document.addEventListener("DOMContentLoaded", function () {
    const menuIcon = document.getElementById("menu-icon");
    const sidebar = document.getElementById("sidebar");
    const closeBtn = document.getElementById("close-btn");

    // Open Sidebar
    menuIcon.addEventListener("click", function () {
        sidebar.classList.add("sidebar-open");
    });

    // Close Sidebar
    closeBtn.addEventListener("click", function () {
        sidebar.classList.remove("sidebar-open");
    });
});
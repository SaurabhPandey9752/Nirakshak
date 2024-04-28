document.addEventListener("DOMContentLoaded", function () {
    var slideIndex = 0;
    showSlides();
  
    function showSlides() {
      var i;
      var slides = document.getElementById("auto-slider").getElementsByTagName("img");
      for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
      }
      slideIndex++;
      if (slideIndex > slides.length) { slideIndex = 1 }
      slides[slideIndex - 1].style.display = "block";
      setTimeout(showSlides, 3000); // Change slide every 3 seconds
    }
  });
  
// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();

      const targetId = this.getAttribute('href').substring(1);
      const targetElement = document.getElementById(targetId);

      if (targetElement) {
        targetElement.style.display = 'block';
        targetElement.scrollIntoView({
          behavior: 'smooth'
        });
      }
    });
  });
});
const sliderContainer = document.querySelector('.homebtm_quicklinks');
let slideIndex = 0; // Current slide index

function showNextSlide() {
  const totalSlides = sliderContainer.children.length;
  slideIndex = (slideIndex + 1) % totalSlides; // Loop to the beginning when reaching the end
  const translateX = -slideIndex * 100; // Shift to the next slide
  sliderContainer.style.transform = `translateX(${translateX}%)`;
}

function showPreviousSlide() {
  const totalSlides = sliderContainer.children.length;
  slideIndex = (slideIndex - 1 + totalSlides) % totalSlides; // Loop to the last slide if going backward at the start
  const translateX = -slideIndex * 100; // Shift to the previous slide
  sliderContainer.style.transform = `translateX(${translateX}%)`;
}

// Event listeners for navigation buttons (if you have buttons for navigation)
document.querySelector('.next-button').addEventListener('click', showNextSlide);
document.querySelector('.prev-button').addEventListener('click', showPreviousSlide);


  // Interval for automatic scrolling in milliseconds
  const scrollInterval = 3000;

  // Amount to scroll by (based on item width)
  const scrollDistance = 150;

  function autoScroll() {
    // Calculate if we've reached the end
    const atEnd = quicklinksContainer.scrollLeft + quicklinksContainer.clientWidth >= quicklinksContainer.scrollWidth;

    if (atEnd) {
      // If at the end, reset to the beginning
      quicklinksContainer.scrollTo({ left: 0, behavior: 'smooth' });
    } else {
      // Otherwise, scroll by the specified distance
      quicklinksContainer.scrollBy({ left: scrollDistance, behavior: 'smooth' });
    }
  }
  function showSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.add('show'); // Add the 'show' class to display the sidebar
  }
  
  function hideSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.remove('show'); // Remove the 'show' class to hide the sidebar
  }
  // Set interval to auto-scroll every few seconds
  document.addEventListener("DOMContentLoaded", function () {
    const menuButton = document.querySelector('.menu-button'); // Hamburger menu
    const sidebar = document.querySelector('.sidebar'); // Sidebar
  
    // Event listener for menu button click to toggle sidebar visibility
    menuButton.addEventListener('click', function () {
      sidebar.classList.toggle('show'); // Add/remove the 'show' class to toggle sidebar
    });
  });
  

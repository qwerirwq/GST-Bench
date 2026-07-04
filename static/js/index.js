document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".self-localization-images .self-current-view").forEach(function (dragTarget) {
    var container = dragTarget.closest(".self-localization-images");
    var dragState = null;

    if (!container) {
      return;
    }

    function moveInset(clientX, clientY) {
      var containerRect = container.getBoundingClientRect();
      var targetRect = dragTarget.getBoundingClientRect();
      var nextLeft = clientX - containerRect.left - dragState.offsetX;
      var nextTop = clientY - containerRect.top - dragState.offsetY;
      var maxLeft = containerRect.width - targetRect.width;
      var maxTop = containerRect.height - targetRect.height;

      dragTarget.style.left = Math.max(0, Math.min(nextLeft, maxLeft)) + "px";
      dragTarget.style.top = Math.max(0, Math.min(nextTop, maxTop)) + "px";
      dragTarget.style.right = "auto";
    }

    dragTarget.addEventListener("pointerdown", function (event) {
      var targetRect = dragTarget.getBoundingClientRect();
      dragState = {
        offsetX: event.clientX - targetRect.left,
        offsetY: event.clientY - targetRect.top
      };

      dragTarget.classList.add("is-dragging");
      dragTarget.setPointerCapture(event.pointerId);
      event.stopPropagation();
    });

    dragTarget.addEventListener("pointermove", function (event) {
      if (!dragState) {
        return;
      }

      moveInset(event.clientX, event.clientY);
      event.stopPropagation();
    });

    function stopDragging(event) {
      if (!dragState) {
        return;
      }

      dragState = null;
      dragTarget.classList.remove("is-dragging");
      event.stopPropagation();
    }

    dragTarget.addEventListener("pointerup", stopDragging);
    dragTarget.addEventListener("pointercancel", stopDragging);
  });

  document.querySelectorAll("[data-examples-carousel]").forEach(function (carousel) {
    var track = carousel.querySelector(".examples-track");
    var slides = Array.prototype.slice.call(carousel.querySelectorAll(".example-slide"));
    var prevButton = carousel.querySelector(".carousel-prev");
    var nextButton = carousel.querySelector(".carousel-next");
    var dots = Array.prototype.slice.call(carousel.querySelectorAll(".examples-dots button"));
    var videos = Array.prototype.slice.call(carousel.querySelectorAll("video"));
    var currentIndex = 0;
    var pointerStartX = null;

    if (!track || slides.length === 0) {
      return;
    }

    function setSlide(nextIndex) {
      currentIndex = (nextIndex + slides.length) % slides.length;
      track.style.transform = "translateX(" + (-currentIndex * 100) + "%)";

      slides.forEach(function (slide, index) {
        slide.setAttribute("aria-hidden", index === currentIndex ? "false" : "true");
      });

      dots.forEach(function (dot, index) {
        var isActive = index === currentIndex;
        dot.classList.toggle("is-active", isActive);
        dot.setAttribute("aria-current", isActive ? "true" : "false");
      });

      videos.forEach(function (video) {
        if (!slides[currentIndex].contains(video)) {
          video.pause();
        }
      });
    }

    if (prevButton) {
      prevButton.addEventListener("click", function () {
        setSlide(currentIndex - 1);
      });
    }

    if (nextButton) {
      nextButton.addEventListener("click", function () {
        setSlide(currentIndex + 1);
      });
    }

    dots.forEach(function (dot, index) {
      dot.addEventListener("click", function () {
        setSlide(index);
      });
    });

    carousel.addEventListener("pointerdown", function (event) {
      pointerStartX = event.clientX;
    });

    carousel.addEventListener("pointerup", function (event) {
      if (pointerStartX === null) {
        return;
      }

      var deltaX = event.clientX - pointerStartX;
      pointerStartX = null;

      if (Math.abs(deltaX) < 45) {
        return;
      }

      setSlide(deltaX < 0 ? currentIndex + 1 : currentIndex - 1);
    });

    carousel.addEventListener("pointercancel", function () {
      pointerStartX = null;
    });

    setSlide(0);
  });
});

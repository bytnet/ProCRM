let allowRotation = true;
window.addEventListener("mousemove", (mouseEvent) => {
  const { clientX, clientY } = mouseEvent;

  blobFollowMouse(clientX, clientY); // Animation

  const videoContainer = document.querySelector("#video-container");

  const rect = videoContainer.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  const distanceX = (clientX - centerX) / rect.width;
  const distanceY = (clientY - centerY) / rect.height;

  if (allowRotation) {
    // To prevent conflicting animations
    rotateVideo3D(distanceX, distanceY); // Animation
  }
});

// Button Reactivity
let btnPlayed = false;
const button = document.querySelector("#replay");


button.addEventListener("mouseover", () => {
  buttonGrow(button); // Animation
  buttonTextIn();
  if (!btnPlayed) {
    buttonColorsWave();
    btnPlayed = true;
  }
});

button.addEventListener("mouseout", () => {
  buttonShrink(button); // Animation
  btnPlayed = false;
});

button.addEventListener("click", () => {
  window.location.href = "/auth";  
});

// initial animations
titleSlideIn();
videoButtonPopIn();

/* -- GSAP ANIMATIONS -- */

// Blob

function blobRotate() {
  const tl = gsap
    .timeline({ repeat: -1, ease: "none" })
    .to("#blob", { rotation: 180, scaleX: 1.6 })
    .to("#blob", { rotation: 360, scaleX: 1 })
    .totalDuration(17);
  tl.play();
}
blobRotate();

function blobFollowMouse(x, y) {
  gsap.to("#blob", {
    left: x,
    top: y,
    duration: 2
  });
}

// 3D Video

function rotateVideo3D(distanceX, distanceY) {
  gsap.to("#video-container", {
    rotateX: -20 * distanceY,
    rotateY: 20 * distanceX,
    duration: 0.5,
    ease: "power1.out"
  });
}

function videoButtonPopIn() {
  allowRotation = false;

  gsap.fromTo(
    "#replay, #video-container",
    { scale: 0 },
    {
      scale: 1,
      ease: "elastic.out(1, 0.8)",
      duration: 0.8,
      delay: 0.4,
      onComplete: () => {
        allowRotation = true;
      }
    }
  );
}

// Title Text

function titleSlideIn() {
  document.querySelectorAll(".word").forEach((word, wordIdx) => {
    Array.from(word.children).forEach((char, charIdx) => {
      gsap.fromTo(
        char,
        {
          opacity: 0,
          x: 0
        },
        {
          opacity: 1,
          x: -300,
          ease: "elastic.out(1.1, 0.7)",
          duration: 1.2,
          delay: wordIdx * 0.2 + charIdx * 0.03
        }
      );
    });
  });
}

// Button

function buttonColorsWave() {
  gsap.fromTo(
    "#purple",
    {
      scale: 0
    },
    {
      scale: 1
    }
  );
  gsap.fromTo(
    "#turquois",
    {
      scale: 0
    },
    {
      scale: 1,
      delay: 0.1
    }
  );
  gsap.fromTo(
    "#yellow",
    {
      scale: 0
    },
    {
      scale: 1,
      delay: 0.2
    }
  );
}

function buttonTextIn() {
  gsap.fromTo(
    ".text",
    {
      y: 9
    },
    {
      y: -8
    }
  );
  gsap.fromTo(
    "#text-static",
    {
      opacity: 1
    },
    {
      opacity: 0
    }
  );
  gsap.fromTo(
    "#text-reveal",
    {
      opacity: 0
    },
    {
      opacity: 1
    }
  );
}

function buttonGrow(button) {
  gsap.to(button, {
    width: 170,
    height: 46
  });
}

function buttonShrink(button) {
  gsap.to(button, {
    width: 180,
    height: 50
  });
}
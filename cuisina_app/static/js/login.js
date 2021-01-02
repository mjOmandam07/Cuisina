const navshow = () => {
  var nav = document.querySelector(".navbar");

  window.onscroll = function () {
    if (window.pageYOffset > 50) {
      nav.classList.add("solid");
    } else {
      nav.classList.remove("solid");
      nav.classList.add("not-solid");
    }
  };
};

navshow();

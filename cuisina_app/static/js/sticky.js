const sticky = () => {
  var nav = document.querySelector(".profile-sidebar");

  window.onscroll = function () {
    if (window.pageYOffset > 250) {
      nav.classList.add("fix");
    } else {
      nav.classList.remove("fix");
    }
  };
};

sticky()
function tinyMCEX(editor, skin, type, height, toolbarStatus) {
  tinymce.init({
    selector: editor,
    // toolbar: 'undo redo styleselect bold italic alignleft aligncenter alignright bullist numlist outdent indent code',
    //   plugins: 'code',

    plugins: 'advlist autolink lists link image charmap preview anchor pagebreak',
    // toolbar_mode: 'floating',
    skin: skin, //'oxide-dark', 'oxide-light'
    //   width : 300, //min_width, max_width
    height: height,
    content_css: type, //default,  dark,  document,  writer
    branding: false,
    toolbar: toolbarStatus,
    browser_spellcheck: true,
    contextmenu: false,
    mobile: {
      menubar: true
    }
    // inline: true,
    // menubar:false
  });


}

/** SWITCH THEMES BLOCK */
$("#default").click(() => {
  setTheme(['theme-default', 'fa-circle-half-stroke', 'Default']);
})

$("#light").click(() => {
  setTheme(['theme-light', 'fa-sun', 'Light']);
})

$("#dark").click(() => {
  setTheme(['theme-dark', 'fa-moon', 'Dark']);
})

function setTheme(arrayList) {
  $('#main-menu-theme').removeClass('fa-circle-half-stroke fa-sun fa-moon');
  localStorage.setItem('theme', arrayList);
  $('#main-menu-theme').addClass(arrayList[1]);
  $('#main-menu-theme > span').text(arrayList[2]);
  document.documentElement.className = arrayList[0];
}

function getTheme() {
  if (window && document.documentElement) {
    $('#main-menu-theme').removeClass('fa-circle-half-stroke fa-sun fa-moon');
    document.documentElement.className = window.localStorage.getItem("theme").split(',')[0];
    $('#main-menu-theme').addClass(window.localStorage.getItem("theme").split(',')[1]);
    $('#main-menu-theme > span').html(window.localStorage.getItem("theme").split(',')[2]);
  }
}

// Immediately invoked function to set the theme on initial load
(function () {
  //THEME IN MY CSS FILE = theme-default 
  //CLASS ICON = fontwasome
  //ICON TEXT = name of the theme
  setTheme(['theme-default', 'fa-moon', 'Dark']);
  
});
/** END SWITCH THEMES BLOCK */

$(document).ready(function () {
  //FROM THEME BLOCK
  getTheme();

  //show and hide the backtotop button
  $(window).scroll(function () {

    let position = $(window).scrollTop();

    if (position > $(window).height()) {
      $('#backtotop').css({ 'display': 'block' })
    } else {
      $('#backtotop').css({ 'display': 'none' })
    }
  });
})

/* When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar */
let prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  let currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("scroll-mn").style.top = "0";
    $(".cont-menu").css({'top' :"46px"});
  } else {
    document.getElementById("scroll-mn").style.top = "-50px";
    $(".cont-menu").css({'top' :"-100px"});
  }
  prevScrollpos = currentScrollPos;
}


  function follow_unfollow(iduser, btn, couter){
      $.ajax({
          url:"/follow",
          type:'post',
          data:{ 'profile': iduser },
          success:function(data){
              $(btn).text(data['text']);
              $(couter).text(data['followers']);
          }
      })
  }
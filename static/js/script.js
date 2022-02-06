$(document).ready(function(){
    $(".sidenav").sidenav({edge: "left"});
    $('.modal').modal();
    $('#welcomeModal').modal();
    $('#welcomeModal').modal('open');
    $('.datepicker').datepicker({
      format: "dd mmmm yyyy",
      yearRange: [1900, 2021],
      showClearBtn: true,
      i18n: {
        done: "Select"
      }
    });
    $('select').formSelect();
    $("#copyright").text(new Date().getFullYear());
  });
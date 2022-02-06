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
    $('.collapsible').collapsible();
    $('.tabs').tabs();
    $("#copyright").text(new Date().getFullYear());
  });
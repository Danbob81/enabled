$(document).ready(function(){
    $(".sidenav").sidenav({edge: "left"});
    $(".dropdown-trigger").dropdown();
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
    $('#due_date').datepicker({
      format: "dd mmmm yyyy",
      yearRange: 0,
      setDefaultDate: true,
      minDate: new Date(),
      disableWeekends: true,
      showClearBtn: false,
      i18n: {
        done: "Select"
      }
    });
    $('#comp_date').datepicker({
      format: "dd mmmm yyyy",
      yearRange: 1,
      setDefaultDate: true,
      maxDate: new Date(),
      disableWeekends: true,
      showClearBtn: false,
      i18n: {
        done: "Select",
      }
    });
    $('select').formSelect();
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    $("#copyright").text(new Date().getFullYear());
  });
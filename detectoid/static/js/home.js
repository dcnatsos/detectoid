/**
 *
 */

$(document).ready(function() {
  var $form = $("form");
  var $loading = $("#loading");
  var $error = $("#error");
  var $stream = $("#stream");

  $form.submit(function(e) {
    var name = $(this).find("input").val();

    $loading.show();
    $stream.hide();
    $error.hide();

    $.getJSON("/"+name, function() {
    })
    .done(function(data) {
      stream(data["stream"]);
    })
    .fail(function(jqxhr, textStatus, error) {
      $error.html(error).show();
    })
    .always(function() {
      $loading.hide();
    });

    e.preventDefault();
  });


  function stream(data) {
    // nice data binding
    // lmao jquery lol gg DansGame
    $stream.find(".name").html(data["name"]);
    $stream.find(".viewers .value").html(data["viewers"]);
    $stream.find(".chatters .value").html(data["chatters"]);
    $stream.find(".followers .value").html(data["followers"]);
    $stream.find(".views .value").html(data["views"]);
    $stream.show();
  };
});

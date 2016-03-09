/**
 *
 */

$(document).ready(function() {
  var $form = $("form");
  var $loading = $("#loading");
  var $error = $("#error");
  var $stream = $("#stream");
  var $chatters = $("#chatters");
  var $table = $("#chatters > table");
  var $details = $table.find("tbody");
  var $dig = $("#dig");

  $form.submit(function(e) {
    var name = $(this).find("input").val();

    $loading.show();
    $stream.hide();
    $error.hide();
    $chatters.hide();
    $table.hide();

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

  $dig.click(function(e) {
    var name = $form.find("input").val();

    $loading.show();
    $error.hide();
    $details.html();

    $.getJSON("/"+name+"/chatters", function() {
    })
    .done(function(data) {
      chatters(data["chatters"]);
    })
    .fail(function(jqxhr, textStatus, error) {
      $error.html(error).show();
    })
    .always(function() {
      $loading.hide();
    });
  });

  function stream(data) {
    $stream.find(".name").html(data["name"]);
    $stream.find(".viewers .value").html(data["viewers"]);
    $stream.find(".chatters .value").html(data["chatters"]);
    $stream.find(".followers .value").html(data["followers"]);
    $stream.find(".views .value").html(data["views"]);

    $stream.show();
    $chatters.show();
    $table.hide();
  };

  function chatters(data) {

    data.forEach(function(chatter) {
      console.log(chatter);

      $details.append(
        "<tr>" +
        "  <td>"+ chatter["name"] +"</td>" +
        "  <td>"+ chatter["created"] +"</td>" +
        "  <td>"+ chatter["updated"] +"</td>" +
        "</tr>");
    });

    $table.show();
  };
});

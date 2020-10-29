var outputArea = $("#chat-output");

$("#user-input-form").on("submit", function (e) {

  e.preventDefault();

  var message = $("#user-input").val();

  outputArea.append(`
    <div class='bot-message'>
      <div class='message'>
        ${message}
      </div>
    </div>
  `);

  let url = "sendBotMessage"
  $.ajax({
    url: url,
    data: {
      message: message
    },
    success: (resp) => {
        outputArea.append("<div class = 'user-message'><div class = 'message'>"+resp+"</div></div>")
      },
    error: () => {
      alert("Something went wrong...")
    }
  })

  $("#user-input").val("");

});
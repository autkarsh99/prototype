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

  // setTimeout(function () {
  //   outputArea.append(`
  //     <div class='user-message'>
  //       <div class='message'>
  //         I'm like 20 lines of JavaScript I can't actually talk to you.
  //       </div>
  //     </div>
  //   `);
  // }, 250);

  let url = "sendBotMessage"
  $.ajax({
    url: url,
    data: {
      message: message
    },
    success: (resp) => {
      console.log(resp)
    },
    error: () => {
      alert("Something went wrong...")
    }
  })

  $("#user-input").val("");

});
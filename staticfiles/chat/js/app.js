let currentRecipient = '';
let test;
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');
let atchBtn=$('#btn-attach');
let curr_time=$('#curr-time');

function updateUserList() {
    $.getJSON('/chat/user/', function (data) {
        userList.children('.usernodes').remove();
        for (let i = 0; i < data.length; i++) {
            const userItem = `<li class="user-nodes">
                               <a href="#" class="user">
                                <div class="d-flex bd-highlight">
                                    <div class="img_cont">
                                        <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg"
                                             class="rounded-circle user_img">
                                         <span class="online_icon"></span>
                                    </div>
                                    <div class="user_info">
                                        <span class="user_name">${data[i]['username']}</span>
                                        <p></p>
                                    </div>
                                </div>
                                </a>
                            </li>`;
            //  const userItem = `<a class="list-group-item user">${data[i]['username']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function (event) {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentRecipient(selected.innerText);
        });
    });
}

function drawMessage(message) {
    let position = 'left';
    const date_full = new Date(message.timestamp);
    const date_str = date_full.toString();
    const date = date_str.split(' ');
    const date1 = [date[1], date[2], date[3], date[4]];
    const date_str1 = date1.join(" ");
    if (message.user === currentUser) {
        const chatItem = `<div class="d-flex justify-content-start mb-4 message ">
                            <div class="img_cont_msg">
                                <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg"
                                     class="rounded-circle user_img_msg">
                            </div>
                            <div class="msg_cotainer">
                                ${message.body}
                                <span class="msg_time">${date_str1}</span>
                            </div>
                            
                              <br>
                                <div id="attachment" > <span > <a href='download/${message.attachmentName}' download> ${message.attachmentName}</a></span>${message.size}</div>
                                    
                                  
                        </div>`
        $(chatItem).appendTo('#messages');
    } else {
        const chatItem = `<div class="d-flex justify-content-end mb-4 message">
                            <div class="msg_cotainer_send">
                                ${message.body}
                                <span class="msg_time_send">${date_str1}</span>
                            </div>
                            <div class="img_cont_msg">
                                <img src="https://static.turbosquid.com/Preview/001292/481/WV/_D.jpg"
                                     class="rounded-circle user_img_msg">
                            </div>
                            <br>
                                <div id="attachment" >  <span> <a href='download/${message.attachmentName}' download> ${message.attachmentName}</a></span>${message.size}</div>
                                    
                                
                        </div>`
        $(chatItem).appendTo('#messages');

    }

}

function getConversation(recipient) {
    $.getJSON(`/chat/message/?target=${recipient}`, function (data) {
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });

}

function getMessageById(message) {
    id = JSON.parse(message).message
    $.getJSON(`/chat/message/${id}/`, function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body, filepath, filename) {
    $.post('/chat/message/', {
        recipient: recipient,
        filepath: filepath,
        filename: filename,
        body: body
    }).fail(function () {
        alert('Error! Check console!');
    });
}

function setCurrentRecipient(username) {
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}
function getBase64(file) {
   var reader = new FileReader();
   reader.readAsDataURL(file);
   reader.onload = function () {
     console.log(reader.result);
   };
   reader.onerror = function (error) {
     console.log('Error: ', error);
   };
}
const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
});
async function Main() {
   const file = document.querySelector('#theFileInput').files[0];
   console.log(await toBase64(file));
}

$(document).ready(function () {
      $('.progress').hide();
    updateUserList();
    disableInput();
    var now =new Date();
    const now_str = now.toString();
    const now_date = now_str.split(' ');
    var  now_date_1 = now_date[4];
    console.log(now_date_1)
    now_date_1 =now_date_1.split(":");
    const now_date_2=[now_date_1[0],now_date_1[1]];
    const now_date_str=now_date_2.join(":");
    curr_time.text(now_date_str);
    console.log(now_date_str);

//   // let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
     var wss_protocol = (window.location.protocol == 'https:') ? 'wss://': 'ws://';
    var socket = new WebSocket(
       wss_protocol + window.location.host +
        '/ws?session_key=${sessionKey}')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0 || $('#theFileInput').prop('files')[0]) {
            if ($('#theFileInput').prop('files')[0])
         {
                 var input = $('#theFileInput').prop('files')[0];
                console.log(input)
                $('.progress').show();
                  var url =  "/chat/upload_file"
                  var fileName = input.name
                  console.log(input)
                  var fd = new FormData();
                  fd.append("theFileInput", input, fileName);
                 console.log(fd)
               //   fd.append("csrfmiddlewaretoken", '{{ csrf_token }}');
                  $.ajax({
                        xhr : function(){
                        $('.progress').css("display",'block');
                        $('#percent').text('0%');
                        var xhr = new window.XMLHttpRequest();
                        xhr.upload.addEventListener('progress', function(e){
                            if (e.lengthComputable) {
                                console.log('Bytes loaded: ' + e.loaded);
                                console.log('Total ' + e.total);
                                console.log('Percetage uploaded ' + (e.loaded / e.total));
                                var percentComplete = e.loaded / e.total;
                                 $('.progress-bar').css('width', (percentComplete)*100+'%');
                                $('#percent').text(Math.floor((percentComplete)*100)+'%');
   
                            }
                        });
                        return xhr;
                    },
                    type: "POST",                    
                    url: url,                    
                    data: fd,
                    cache: false,
                    contentType: false, 
                    processData: false, 
                    success: function (data) {
                      console.log(data)
                      var filepath = data['filepath']
                      var filename = data['filename']
                      sendMessage(currentRecipient, chatInput.val(), filepath, filename);
                    chatInput.val('');
                    $('#preview').html("");
                        $('.progress').hide();
                      $("#theFileInput").val(null);
                    return true
                    },
                  });
                
        
        }
           else
            {
            sendMessage(currentRecipient, chatInput.val(), '', '');
          $('#preview').html("");
            chatInput.val('');
           $("#theFileInput").val(null);
                }
        }

    });
 
    var b64;
    atchBtn.click(function(){
        $('#theFileInput').trigger('click');
         console.log( $('#theFileInput').prop('files')[0])
        
        //$('#theFileInput').files[0];
   //     console.log(file.length,file);


        // file = document.querySelector('#theFileInput > input[type="file"]').files[0];
     //  getBase64(file);
        // fileReader.onload = function (EventFileLoaded) {
        //     b64 = EventFileLoaded.target.result;
        //     console.log(b64)
        //
        // }
    }
    );

    socket.onmessage = function (e) {
        getMessageById(e.data);
    };
});

$("#theFileInput").change(function(){
         var file = $('#theFileInput').prop('files')[0]
         document.getElementById('preview').innerHTML = file.name
 });
function uploadFile(input) { 
        //reader.readAsDataURL(input.files[0]);
        
    }



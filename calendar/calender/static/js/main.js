$(document).ready(function(){
  //var socketEndPoint = "http://localhost:3002"
  var socketEndPoint = "https://sockets.mitrarobot.com"
  var socket = io.connect(socketEndPoint);
  //check if the page is token is valid
  var token = localStorage.getItem("token");
  if(token =="" || token == null)
    window.location.replace("/");
 
  $.ajax({
    type: 'POST',
    url: '/user/verify',
    data: JSON.stringify({}),
    headers: {
      "Authorization": "Bearer " + token
    },
    success: function(data,status,xhr) { 
        //if(xhr.status != 200) window.location.replace("/");
    },error: function(data, status,xhr){
        console.error(status);
        //window.location.replace("/");
    },
    contentType: "application/json",
    dataType: 'json'
});

/**
 *  socket on receive the current patient session
 * {data}  - {"mobile":"","robotname":""}
 */
socket.on("patient_session", function(data){
  getUserSession(data["mobile"]);
});

socket.on("occupancy", function(data){
  console.log(data);
  localStorage.setItem("currentRobot",data.robot_name)
});

/**
 * @param {*} mobile - string
 */
var getUserSession = function(mobile){
  var settings = {
    "url": "/user/session?mobile="+ mobile,
    "method": "GET",
    "timeout": 0,
  };
  
  $.ajax(settings).done(function (data) {
    loadChatWindow(data.data["session"]);
  });
}

var call_next_patient = function(){
  var settings = {
    "url": "/queue/getLast/",
    "method": "POST",
    "timeout": 0,
    "headers": {"Content-Type": "application/json"},
  };
  
  $.ajax(settings).done(function (response) {
    let data  = response["data"][0];
    if(data == null || data == undefined)return;
    data["robotname"] = localStorage.getItem("name")
    data["message"] = "Please wait for 15 mins"
    data["subject"] = "Wait Pls"
    emitSocketMessage('next_patient', data);
  });

}

/**
 * @param {*} channel - channel name 
 * @param {*} message - message for the channel
 */
var emitSocketMessage = function(channel, message){
  console.log(channel,message)
  socket.emit(channel, message)
}
/**
 * @param {*} message : string (command name ~ command)
 */
var getSocketsMessage = function(message){
  return {"robotname":localStorage.getItem("name"),"command":message}; 
}
  
  /**
   * 
   */
  var loadRoomName = function(){
      try {
          $("#room-name").val(localStorage.getItem("name"));
          setTimeout(function() {
              console.log("trigger click")
              $('#button-join').trigger('click');
          }, 2000);
        }
        catch(err) {
          console.warn("its a open room");
        }
  }
  // $(".dpad").click(function(){
  //   var val = $(this).attr("command");
  //   if(val != ""){
  //     emitSocketMessage('video_message', val);
  //   }
  // });

  var test = function(json){
    $.ajax({
      type: 'POST',
      url: '/generateReport',
      data: JSON.stringify(json),
      success: function(data,status,xhr) { 
          //if(xhr.status != 200) window.location.replace("/");
      },error: function(data, status,xhr){
          console.error(status);
          //window.location.replace("/");
      },
      contentType: "application/json",
      dataType: 'json'
  });
  }

  $(".button-stop").click(function(){
      emitSocketMessage('video_message', getSocketsMessage("navigation~403"));
  });

  // send image queries
  $(".send-sockets-image").click(function(){
    
    var val = $("#image").val();
    if(val != ""){
      val = "mitra:image:"+val
      emitSocketMessage('video_message', getSocketsMessage(val));
    }
    $("#image").val('');
  });
  // send speak queries
  $(".send-sockets-speak").click(function(){
    var val = $("#speak").val();
    if(val != ""){
      val = "mitra:speak:"+val;
      emitSocketMessage('video_message', getSocketsMessage(val));
    }
    $("#speak").val("");
  });
  // send general queries
  $(".send-sockets-general").click(function(){
    var val = $("#general").val();
    if(val != ""){
      emitSocketMessage('video_message', getSocketsMessage(val));
    }
    $("#general").val("");
  });
  // send general queries
  $(".send-sockets-home").click(function(){
    clearPresciption();
    $("#chat_window").html('');
    emitSocketMessage('video_message', getSocketsMessage("actions:disconnect~."));
    // call next patient
    call_next_patient()
  });

  $(".button-stop").tapstart(function(event) { 
    $(".button-stop").addClass("active-stop");
  });
  $('.button-stop').tapend(function(event) { 
    $(".button-stop").removeClass("active-stop");
  });
  //touch events
  $('.dpad').tapstart(function(event) { 
      $(this).addClass("active-dpad");
      event.preventDefault();
      emitSocketMessage('video_message', getSocketsMessage($(this).attr("command")));
      
  });
  $('.dpad').tapend(function(event) { 
    $(this).removeClass("active-dpad");
      event.preventDefault();
      emitSocketMessage('video_message', getSocketsMessage("navigation~403"));
  });

  $('.center-stop').tapstart(function(event) { 
    $(this).addClass("active-stop");
    event.preventDefault();
  });

  $('.center-stop').tapend(function(event) { 
      $(this).removeClass("active-stop");
      event.preventDefault();
      //emitSocketMessage('video_message', "mitra:nav:403");
  });
  // Load the room name
  
  /**
   * 
   */
  var addFields = function(){
    var html = '<div class="form-group">'+
    '<label class="col-lg-3 col-sm-2" for="pwd" contenteditable="true">Others:</label>'+
    '<div class="col-lg-9 col-sm-10">'+
      '<input type="text" class="form-control"  placeholder="medicine">'+
    '</div>'+
  '</div>';
    $("#additional").append(html);
  }

  $("#addFields").click(function(){
    addFields();
  })
  /**
   * 
   * @param {*} oList 
   */
  var formulateData =  function(oList){
    var json = {};
    for (var i=0;i<oList.length;i++){
      json[oList[i]["name"]] = oList[i]["value"]
    }
    return json;
  }
  $("#printForm").click(function(e){  
    //window.print()
    var json = {"bp":$("#bp").val(),"temperature":$("#temperature").val(),"others":$("#others").val(),"robotname":$("#room-name").val()}
    var prescription = getPrescriptionDetails()
    var patient_data = formulateData($("#patient_form").serializeArray())
    var patient = {"prescription":prescription,"patient_data":patient_data}
    console.log(patient)
    patient["robotname"] = localStorage.getItem("currentRobot")//$("#room-name").val()
    emitSocketMessage("prescription",patient)
  })

  var clearPresciption = function(){
    $(".user_pass").addClass("hide");
    $(".prescription").val('')
    $('.user_details').html('');
    $("#patient_name").html('');
  }
  $("#clearFields").click(function(e){
    clearPresciption();
  })

 /**
  * 
  * @param {*} session 
  */
  function loadChatWindow(session){
    console.log(session);

    var settings = {
      "url": "/user/data?session="+ session,
      "method": "GET",
      "timeout": 0,
    };
    
    $.ajax(settings).done(function (response) {
      $(".user_pass").removeClass("hide");
      var patientData = response['data']['data']
      $("#user_name,#patientprint_name").html(patientData["name"]);
      $("#user_img").attr("src", patientData["face"]);
      $("#user_mobile").html(patientData["mobile"]);
      $("#user_mobile_validate").html(patientData["isPhoneNumberValidated"])
      $("#user_screening_result").html(patientData["screeningResult"])
      $("#user_purpose").html(patientData["purpose"])
      $("#user_is_fever").html(patientData["feverStatus"]);
      $("#user_temperature").html(patientData["temperature"]+"degrees")
      $("#user_time").html(patientData["time"]);
      $("#user_other_symtoms").html(patientData["otherSymptoms"]);
      //
      // var chat = response['data'];
      // for (var i=0;i<chat.length;i++){
      //   $("#chat_window").append(constructChat(chat[i]['question'],chat[i]['query'],chat[i]['time'] ))
      // }
    });
}
/**
 * @param {*} question 
 * @param {*} answer 
 * @param {*} time 
 */
var constructChat = function(question,answer, time){
    var html =  '<div class="bubbleWrapper">'+
        '<div class="inlineContainer">'+
        '<img class="inlineIcon" src="https://cdn1.iconfinder.com/data/icons/ninja-things-1/1772/ninja-simple-512.png">'+
        '<div class="otherBubble other">'+
        question+
        '</div>'+
        '</div><span class="other">'+time+'</span>'+
        '</div>'+
        '<div class="bubbleWrapper">'+
        '<div class="inlineContainer own">'+
        '<img class="inlineIcon" src="https://www.pinclipart.com/picdir/middle/205-2059398_blinkk-en-mac-app-store-ninja-icon-transparent.png">'+
        '<div class="ownBubble own">'+
        answer+
        '</div>'+
        '</div><span class="own">'+time+'</span>'+
    '</div>';
    return html;
}
//loadChatWindow()
  loadRoomName(); 
  /**
   * 
   */
  $(".add_prescription_field").click(function(){
    var len =  $("#precription tbody tr").length +1;
    var html = '<tr>';
    html += '<td>'+len+'</td>';
    html += '<td><input type ="text" id ="medicine_'+len+'"/></td>';
    html += '<td><input type ="text" id ="dosage_'+len+'"/></td>';
    html += '<td><input type ="text" id ="instructions_'+len+'"/></td>';
    html += '</tr>';
    
    $("#precription tbody").append(html);
  });

  /**
   * 
   */
  var getPrescriptionDetails = function(){
    var prescription = [];
    var len =  $("#precription tbody tr").length;
    for (i=1;i<=len;i++){
      var json = {"medicine":"","dosage":"","instructions":""}
      json["instructions"] = $("#instructions_"+i+"").val();
      json["medicine"] = $("#medicine_"+i+"").val();
      json["dosage"] = $("#dosage_"+i+"").val();
      console.log(json)
      prescription.push(json);
    }
    return prescription;
  }

});
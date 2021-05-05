$(document).ready(function(){


    var getPatientPhi = function(url, pId, callback){
        let json = {"url":url, "pId":pId}
        $.ajax({
            type: 'POST',
            url: '/doctor/patient',
            data: JSON.stringify(json),
            success: function(data,status,xhr) { 
                console.log(data)
                callback(JSON.parse(data))
            },error: function(data, status,xhr){
                console.error(status);
                
            },
            contentType: "application/json",
            dataType: 'json'
        });
    }

    var getPatientPII = function(url, pId, callback){
        let json = {"url":url, "pId":pId}
        $.ajax({
            type: 'POST',
            url: '/patient/data',
            data: JSON.stringify(json),
            success: function(data,status,xhr) { 
                console.log(data)
                callback(JSON.parse(data))
            },error: function(data, status,xhr){
                console.error(status);
                
            },
            contentType: "application/json",
            dataType: 'json'
        });
    }
    
    var populatePatientDetails = (json) => {
        
        //$("#patient_name").html(patient_basic['full_name']);
        //$("#patient_id").html(patient_basic['id']);
        $("#patient_age").html(json.age);
        let sex ="Female"
        if(json.sex == "m") sex = "Male"
        $("#patient_gender").html(sex);
        $("#blood").html(json.blood_group);
        $("#hereditary_conditions").html(json.hereditary_conditions)
        $("#medical_history").html(json.medical_history +" , Allergies "+ json.allergies)
        let smoking = "No"
        if(json.smoker) smoking = "yes"
        $("#smoking").html(smoking);
        let drinking = "No"
        if(json.drinker) drinking = "yes"
        $("#drinking").html(drinking);
    }
    var populatePatientPii = (patient_basic) => {
        
        $("#patient_name").html(patient_basic['full_name']);
        $("#patient_id").html(patient_basic['id']);
        
    }
    

    let fetchData = function(url, id){
        getPatientPhi(url || "http://localhost:8000",  
        id || "e62e0f43-ffd9-4223-9038-9092d96a69c2", (data)  => {
            populatePatientDetails(data.patient_phi);
        });

        getPatientPII(url || "http://localhost:8000",  
        id || "e62e0f43-ffd9-4223-9038-9092d96a69c2", (data)  => {
            populatePatientPii(data);
        });
    }
    fetchData();

});
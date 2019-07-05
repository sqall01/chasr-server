function console_log(text) {
    console.log(text);
    var text_area = document.getElementById("log_output");
    var date = new Date();
    var dateString = ("0" + date.getUTCHours()).slice(-2) + ":" +
                     ("0" + date.getUTCMinutes()).slice(-2) + ":" +
                     ("0" + date.getUTCSeconds()).slice(-2);
    var output = dateString + ": " + text + "\n";
    output += text_area.value;
    text_area.value = output;
}

function console_error(text) {
    console.error(text);
    var text_area = document.getElementById("log_output");
    var date = new Date();
    var dateString = ("0" + date.getUTCHours()).slice(-2) + ":" +
                     ("0" + date.getUTCMinutes()).slice(-2) + ":" +
                     ("0" + date.getUTCSeconds()).slice(-2);
    var output = dateString + " Error: " + text + "\n";
    output += text_area.value;
    text_area.value = output;
}

// Is called after "callbackGpsPosition()" if it is a start GPS position.
function callbackStartGpsPosition(gps_point) {
}

// Is called after "callbackGpsPosition()" if it is an end GPS position.
function callbackEndGpsPosition(gps_point) {
}

// Is called after a GPS position is placed on the map.
function callbackGpsPosition(gps_point) {
}

function showDevicesData(devices_data) {

    var select_form = document.forms["device_form"]["device"];

    // Clear select from.
    var to_remove = [];
    for(var i = 0; i < select_form.length; i++) {
        to_remove.push(select_form[i]);
    }
    for(var i = 0; i < to_remove.length; i++) {
        select_form.remove(to_remove[i]);
    }

    // Add all received options.
    var device_exists = false;
    var device_option;
    for(var i = 0; i < devices_data["devices"].length; i++) {
        var new_device = devices_data["devices"][i];

        var option = document.createElement("option");
        option.text = new_device["device_name"];
        option.value = new_device["device_name"];
        select_form.add(option);

        // Search device we want to use.
        if(new_device["device_name"] === device_name) {
            device_option = option;
        }
    }

    // Select our device if it exists.
    if(device_name && device_option) {
        device_option.selected = "selected";
    }

    // Get available device slots on the server and display them.
    var device_slots = devices_data["avail_slots"];
    var left_device_slots = device_slots - devices_data["devices"].length;
    var device_slots_p = document.getElementById("device_slots");
    device_slots_p.textContent = "Device slots left: " + left_device_slots

    show();
}

function showStatusDevice() {
    // Show what device is set.
    if(device_name) {
        document.getElementById("device_set").textContent =
                                        "Device '" + device_name + "' set.";
    }
    else {
        document.getElementById("device_set").textContent = "No device set.";
    }
}

function showStatusMode() {
    // Show what device is set.
    if(mode) {
        document.getElementById("mode_set").textContent =
                                        "Mode '" + mode + "' set.";

        // Show start and end date field.
        if(mode === "view") {
            document.getElementById("start_end_date").style.display = "block";
        }
        else {
            document.getElementById("start_end_date").style.display = "none";
        }
    }
    else {
        document.getElementById("mode_set").textContent = "No mode set.";
        document.getElementById("start_end_date").style.display = "none";
    }
}

function showStatusSecret() {

    // Show if secret is locally set.
    if(secret_hash) {
        document.getElementById("secret_set").textContent = "Secret set.";
    }
    else {
        document.getElementById("secret_set").textContent = "No secret set.";
    }

    // Show if secret is locally stored.
    if(localStorage.getItem("secret_hash")) {
        document.getElementById("secret_stored").textContent =
                                                        "Secret stored in browser.";
    }
    else {
        document.getElementById("secret_stored").textContent =
                                                        "No secret stored in browser.";
    }
}

// Sets the selected device.
function setDevice() {
    var select_form = document.forms["device_form"]["device"];
    device_name = select_form[select_form.selectedIndex].value;

    clearGps();
    addGpsPositionsToMapClear([]);
    show();
}

// Sets the selected device.
function setMode() {
    var select_form = document.forms["mode_form"]["mode"];
    mode = select_form[select_form.selectedIndex].value;

    clearGps();
    addGpsPositionsToMapClear([]);
    show();
}

// Sets start and end date.
function setStartEndDate() {
    start = new Date(document.getElementById("start_date").value);
    end = new Date(document.getElementById("end_date").value);

    start_date = start.getTime()/1000; 
    end_date = end.getTime()/1000 + 86400; 

    show();
}

async function setSecret() {

    // Set if we should store the secret/key.
    store_secret = document.forms["secret_form"]["store_secret"].checked;

    // Set the new secret.
    var new_secret = document.forms["secret_form"]["secret"].value;
    document.forms["secret_form"]["secret"].value = "";
    if(!await setSecretHash(new_secret)) {
        console_error("No secret set. Please set a secret.");
        return;
    }

    // If we should store the secret hash in the browser, we store it.
    if(store_secret) {
        localStorage.setItem("secret_hash", byteArrayToHexstring(secret_hash));
    }

    show();
}

function show() {

    // Clear timer if user had changed something in between.
    if(live_timer) {
        clearTimeout(live_timer);
    }

    showStatusSecret();
    showStatusDevice();
    showStatusMode();

    if(mode && device_name) {
        if(mode === "live") {
            requestLastData();
        }
        else {
            requestViewData();
        }
    }  
}

// Initialize page.
function init() {
    new TinyPicker({
            firstBox:document.getElementById("start_date"),
            lastBox: document.getElementById("end_date"),
            startDate: new Date(),
            endDate: new Date(),
            allowPast: true,
            success: function(){ setStartEndDate(); }
    }).init();

    parseHashVars();
    requestDevicesData();
    createNewMap();
    
    if(!mode) {
        console_log("Please select a mode.");
    }
    if(!device_name) {
        console_log("Please select a device.");
    }
    if(!secret_hash) {
        console_log("Please set a secret.");
    }
}

init();
show();
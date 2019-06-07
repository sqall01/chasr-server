function console_log(text) {
    Android.console_log(text);
}

function console_error(text) {
    Android.console_error(text);
}

// Is called after "callbackGpsPosition()" if it is a start GPS position.
function callbackStartGpsPosition(gps_point) {
}

// Is called after "callbackGpsPosition()" if it is an end GPS position.
function callbackEndGpsPosition(gps_point) {
}

// Is called after a GPS position is placed on the map.
function callbackGpsPosition(gps_point) {
    var lon = gps_point["lon"];
    var lat = gps_point["lat"];
    var alt = gps_point["alt"];
    var speed = gps_point["speed"];
    var utctime = gps_point["utctime"];
    Android.addGpsPosition(lat, lon, alt, speed, utctime);
}

function showDevicesData(devices_data) {
}

function showStatusDevice() {
}

function showStatusMode() {
}

function showStatusSecret() {
}

function show() {

    // Clear timer if user had changed something in between.
    if(live_timer) {
        clearTimeout(live_timer);
    }

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
    parseHashVars();
    createNewMap();
    setAESKey();
    
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
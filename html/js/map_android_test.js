// Used "callbackStartDecryptGpsPosition()" to display state of decryption.
var callback_gps_enc_pos = 0;

function console_log(text) {
    Android.console_log(text);
}

function console_error(text) {
    Android.console_error(text);
}

// Is called after "callbackGpsPosition()" if it is a start GPS position.
function callbackStartGpsPosition(gps_point) {
    var lon = gps_point["lon"];
    var lat = gps_point["lat"];
    var alt = gps_point["alt"];
    var speed = gps_point["speed"];
    var utctime = gps_point["utctime"];
    Android.startGpsPosition(lat, lon, alt, speed, utctime);
}

// Is called after "callbackGpsPosition()" if it is an end GPS position.
function callbackEndGpsPosition(gps_point) {
    var lon = gps_point["lon"];
    var lat = gps_point["lat"];
    var alt = gps_point["alt"];
    var speed = gps_point["speed"];
    var utctime = gps_point["utctime"];
    Android.endGpsPosition(lat, lon, alt, speed, utctime);
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

// Is called before the newly received GPS positions are decrypted.
function callbackStartDecryptAllGpsPositions(gps_data) {
    callback_gps_enc_ctr = 0;
    Android.startDecryptAllGpsPositions(gps_data.length);
}

// Is called after the newly received GPS positions were decrypted.
function callbackEndDecryptAllGpsPositions(gps_data) {
    Android.endDecryptAllGpsPositions(gps_data.length);
}

// Is called before the single GPS position is decrypted.
function callbackStartDecryptGpsPosition(gps_data) {
    Android.startDecryptGpsPosition(callback_gps_enc_pos);

}

// Is called after the single GPS position was decrypted.
function callbackEndDecryptGpsPosition(gps_data) {
    Android.endDecryptGpsPosition(callback_gps_enc_pos);
    callback_gps_enc_pos++;
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
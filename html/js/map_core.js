var request_data = new XMLHttpRequest();
var request_devices = new XMLHttpRequest();
var global_gps_data = [];
var global_enc_gps_data = [];
var secret_hash;
var final_aes_key;
var final_hmac_key;
var store_secret = false;
var map;
var vector_layer;
var live_limit = 20;
var live_timeout = 10000;
var set_zoom = 16;
var mode;
var device_name;
var start_date = 0;
var end_date = 0;
var live_timer = null;


async function createAESKey(secret_hash) {
    return window.crypto.subtle.importKey("raw",
                                          secret_hash,
                                          {name: "AES-CBC",},
                                          false,
                                          ["decrypt"]);
}

async function createHMACKey(secret_hash) {
    return window.crypto.subtle.importKey("raw",
                                          secret_hash,
                                          {name:"HMAC", "hash":"SHA-256"},
                                          false,
                                          ["verify"]);
}

async function decryptData(iv_var, dec_key, enc_data) {
    return window.crypto.subtle.decrypt({name: "AES-CBC",
                                        iv: iv_var,},
                                        dec_key,
                                        enc_data);
}

async function verifyData(hmac_key, authtag, data) {
    return window.crypto.subtle.verify("HMAC",
                                     hmac_key,
                                     authtag,
                                     data);
}

// Clears the secret and key.
function clearSecret() {
    localStorage.removeItem("secret_hash");
    secret_hash = null;
    final_aes_key = null;
    final_hmac_key = null;

    show();
}

function clearGps() {
    global_enc_gps_data = [];
    global_gps_data = [];
}

async function setSecretHash(secret) {
    // Create sha-256 hash from the given secret.
    var temp_buffer = [];
    for(var i = 0; i < secret.length; i++) {
        temp_buffer.push(secret.charCodeAt(i));
    }
    var array_buffer = new Uint8Array(temp_buffer);

    try {
        var hash = await window.crypto.subtle.digest({name: "SHA-256"},
                                                     array_buffer);
    }
    catch(err) {
        console.error(err.message);
        return false;
    }
    secret_hash = new Uint8Array(hash);

    // Set AES and HMAC key.
    await setCryptoKey();

    return true;
}

async function setCryptoKey() {

    // Load stored secret hash if it exists
    // and if no secret hash was set yet.
    var stored_secret_hash = localStorage.getItem("secret_hash");
    if(stored_secret_hash !== null && !secret_hash) {
        secret_hash = hexstringToByteArray(stored_secret_hash);
    }

    showStatusSecret();

    // If we do not know the hash of the secret,
    // create it before creating the AES key.
    if(!secret_hash) {
        return false;
    }

    // If we already now the hash of the secret, just create the AES key.
    else {
        try {
            final_aes_key = await createAESKey(secret_hash);
            final_hmac_key = await createHMACKey(secret_hash);
        }
        catch(err) {
            console_error(err.message);
            console_error("Did you set the correct secret?");
            return false;
        }
    }

    return true;
}

function hexstringToByteArray(input_str) {
    var hex  = input_str.toString();
    var str_buffer = [];
    for (var i = 0; i < hex.length; i += 2) {
        str_buffer.push(parseInt(hex.substr(i, 2), 16));
    }
    return new Uint8Array(str_buffer);
}

function byteArrayToHexstring(byte_array) {
    var str = "";
    for (var i = 0; i < byte_array.length; i++) {
        str += ('0' + (byte_array[i] & 0xFF).toString(16)).slice(-2);
    }
    return str;
}

async function processNewGpsData(new_gps_data) {

    // If the key is not available yet, return.
    if(!final_aes_key || !final_hmac_key) {
        console_log("Decryption key not yet available.");
        console_log("Did you set a secret?");

        // Store encrypted GPS data as long as we do not
        // have any key to decrypt.
        for(var i = 0; i < new_gps_data["locations"].length; i++) {
            global_enc_gps_data.push(new_gps_data["locations"][i]);
        }

        return;
    }

    // If we have stored encrypted gps positions (because we did
    // not have a decryption key yet), copy them in front of the
    // currently received data before processing it.
    if(global_enc_gps_data.length > 0) {
        for(var i = global_enc_gps_data.length-1; i >= 0; i--) {
            new_gps_data["locations"].unshift(global_enc_gps_data[i]);
        }
        global_enc_gps_data = [];
    }

    // Process received gps data.
    for(var i = 0; i < new_gps_data["locations"].length; i++) {
        var new_data = new_gps_data["locations"][i];

        // Only proceed if received gps position is
        // newer than our last known position.
        if(global_gps_data.length > 0) {
            old_data = global_gps_data[global_gps_data.length-1];
            if(new_data["utctime"] <= old_data["utctime"]) {
                continue;
            }
        }

        // Create new decrypted gps object.
        var new_dec_data = {};
        new_dec_data["utctime"] = new_data["utctime"];
        var str_to_verify = new_data["device_name"];
        str_to_verify += new_data["utctime"].toString();
        var curr_iv = hexstringToByteArray(new_data["iv"]);
        var keys = ["lat", "lon", "alt", "speed"];
        for(var j = 0; j < keys.length; j++) {
            var key = keys[j];

            // Decrypt data.
            var data_to_dec = hexstringToByteArray(new_data[key]);
            try {
                var temp_data = await decryptData(curr_iv,
                                                  final_aes_key,
                                                  data_to_dec);
            }
            catch(err) {
                console_error(err.message);
                console_error("Did you set the correct secret?");
                break;
            }
            var dec_data = new Uint8Array(temp_data);
            var temp_str = "";
            for(var k = 0; k < dec_data.length; k++) {
                temp_str += String.fromCharCode(dec_data[k]);
            }
            str_to_verify += temp_str;
            var final_float = parseFloat(temp_str);

            new_dec_data[key] = final_float;
        }

        // Authenticate received GPS data.
        var data_to_verify = new TextEncoder("utf-8").encode(str_to_verify);
        var authtag = hexstringToByteArray(new_data["authtag"]);
        try {
            var is_auth = await verifyData(final_hmac_key,
                                           authtag,
                                           data_to_verify);
            if(!is_auth) {
                console_error("Authentication of GPS data failed. "
                              + "It seems something nasty is going on.");
                continue;
            }
        }
        catch(err) {
            console_error(err.message);
            console_error("Did you set the correct secret?");
        }
        
        // Add new gps position to our global gps data.
        global_gps_data.push(new_dec_data);
    }

    // Add all gps positions to the map.
    if(mode === "live") {
        // Remove gps positions if we have reached our limit.
        while(global_gps_data.length > live_limit) {
            global_gps_data.shift();
        }
        addGpsPositionsToMapClear(global_gps_data);
    }
    else if(mode === "view") {
        addGpsPositionsToMapClear(global_gps_data);
    }
    else {
        console.error("No 'mode' set.");
    }

    // Center map on last gps position.
    if(global_gps_data.length > 0) {
        centerMapToGpsPosition(global_gps_data[global_gps_data.length-1]);
    }
}

function processDevicesData(devices_data) {
    showDevicesData(devices_data);
}

// Process response of devices data request.
function processResponseDevicesData() {
    if(request_devices.readyState == 4) {
        var response = request_devices.responseText;
        var response_data = JSON.parse(response);

        // Check if we have received an error.
        if(response_data["code"] === 0) {
            if(response_data["data"]["devices"].length == 0) {
                console_log("No devices available.");
            }
            processDevicesData(response_data["data"]);
        }
        else {
            console_error("Received error code '"
                          + response_data["code"].toString()
                          + "' from server.");
        }
    }
}

// Process response of last data request.
function processResponseData() {

    if(request_data.readyState == 4) {
        var response = request_data.responseText;
        var response_data = JSON.parse(response);

        // Check if we have received an error.
        if(response_data["code"] === 0) {
            if(response_data["data"]["locations"].length > 0) {
                processNewGpsData(response_data["data"]);
            }
            else {
                console_log("No GPS data available.");
            }
        }
        else {
            console_error("Received error code '"
                          + response_data["code"].toString()
                          + "' from server.");
        }
    }

    // If we are in live tracking mode, request next data in
    // configured timeout.
    if(mode === "live" && !live_timer) {
        live_timer = setTimeout(requestLastDataTimer, live_timeout);
    }
}

// Request last data from server.
function requestLastData() {

    if(!device_name) {
        console_log("No device set. Please select a device.");
        return;
    }

    var url = "./get.php?mode=last&device=" + device_name;
    requestData(url, processResponseData);
}

// Request last data from server and resets the timer variable.
function requestLastDataTimer() {
    live_timer = null;
    requestLastData();
}

// Request data from server.
function requestData(url, callback) {
    request_data.open("GET", url, true);
    request_data.onreadystatechange = callback;
    request_data.send(null);
}

// Request devices data from server.
function requestDevicesData() {
    var url = "./get.php?mode=devices";
    request_devices.open("GET", url, true);
    request_devices.onreadystatechange = processResponseDevicesData;
    request_devices.send(null);
}

// Request view data from server.
function requestViewData() {

    if(!device_name) {
        console_log("No device set. Please select a device.");
        return;
    }

    if(start_date === 0 || end_date === 0) {
        console_log("No start/end date set. Please select a date.");
        return;
    }

    var url = "./get.php?mode=view&device="
            + device_name
            + "&start="
            + start_date
            + "&end="
            + end_date;
    requestData(url, processResponseData);
}

// Creates a new map object (if no old one exists).
function createNewMap() {

    var style = {
        "StartIcon": new ol.style.Style({
            image: new ol.style.Icon({
                anchor: [0.5, 1],
                src: "img/icons/start_pos.png"
            })
        }),
        "EndIcon": new ol.style.Style({
            image: new ol.style.Icon({
                anchor: [0.5, 1],
                src: "img/icons/end_pos.png"
            })
        }),
        "Point": new ol.style.Style({
            image: new ol.style.Circle({
                fill: new ol.style.Fill({
                    color: 'rgba(39,116,240,0.8)'
                }),
                radius: 5,
                stroke: new ol.style.Stroke({
                    color: "#000000",
                    width: 1
                })
            })
        }),
        "LineString": new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: "#2774dc",
                width: 2
            })
        })
    }

    if(!map) {
        var source_var = new ol.source.Vector({features: []})
        vector_layer = new ol.layer.Vector({
            source: source_var,
            style: function(feature) {
                   return style[feature.get("type")];
            }
        });
        var center = [13.413215, 52.521918]; // Berlin
        map = new ol.Map({target: 'map_id',
                         layers: [new ol.layer.Tile({
                                                    source: new ol.source.OSM()
                                  }),
                                  vector_layer],
                         view: new ol.View({
                                            center: ol.proj.fromLonLat(center),
                                            zoom: set_zoom
                         }),
        });
    }
}

// Adds one new marker to the map.
function addMarkerToMap(lon_var,
                        lat_var,
                        alt_var,
                        speed_var,
                        utctime_var,
                        type_var="Point") {

    var transformed_coord = ol.proj.transform([lon_var, lat_var],
                                              'EPSG:4326',     
                                              'EPSG:3857')

    var marker = new ol.Feature({
                                geometry: new ol.geom.Point(transformed_coord),
                                type: type_var,
                                lon: lon_var,
                                lat: lat_var,
                                alt: alt_var,
                                speed: speed_var,
                                utctime: utctime_var
    });

    var source = vector_layer.getSource();
    source.addFeature(marker);
}

// Adds one new marker to the map.
function addGpsPositionToMap(gps_point, type_var="Point") {
    addMarkerToMap(gps_point["lon"],
                   gps_point["lat"],
                   gps_point["alt"],
                   gps_point["speed"],
                   gps_point["utctime"],
                   type_var);
    callbackGpsPosition(gps_point);
    if(type_var === "StartIcon") {
        callbackStartGpsPosition(gps_point);
    }
    else if(type_var === "EndIcon") {
        callbackEndGpsPosition(gps_point);
    }
}

// Center the map to the given coordinates.
function centerMapToCoord(lon, lat) {
    var view = map.getView();
    view.setCenter(ol.proj.fromLonLat([lon, lat]))
}

// Center the map to the given coordinates.
function centerMapToGpsPosition(gps_point) {
    centerMapToCoord(gps_point["lon"], gps_point["lat"]);
}

// Clear map and add all gps positions to the map given by the parameter.
function addGpsPositionsToMapClear(gps_points) {
    var source = vector_layer.getSource();
    source.clear();
    var last_gps_point;
    for(var i = 0; i < gps_points.length; i++) {
        var curr_gps_point = gps_points[i];

        // Decide how to draw the point.
        if(i === 0) {
            addGpsPositionToMap(curr_gps_point, "StartIcon");
        }
        else if(i === gps_points.length-1) {
            addGpsPositionToMap(curr_gps_point, "EndIcon");
        }
        else {
            addGpsPositionToMap(curr_gps_point);
        }

        // Draw a line between the last gps point and the current one.
        if(last_gps_point) {

            // Create feature.
            var last_point = ol.proj.transform([last_gps_point["lon"],
                                                last_gps_point["lat"]],
                                               'EPSG:4326',
                                               'EPSG:3857');
            var curr_point = ol.proj.transform([curr_gps_point["lon"],
                                                curr_gps_point["lat"]],
                                               'EPSG:4326',
                                               'EPSG:3857');
            var line = new ol.geom.LineString([last_point, curr_point]);
            var feature_line = new ol.Feature({geometry: line,
                                               type: "LineString"});

            // Add feature.
            var source = vector_layer.getSource();
            source.addFeature(feature_line);
        }

        last_gps_point = curr_gps_point;
    }
}

// Parses the variables given behind the hash parameter
// and sets them (if they are valid).
function parseHashVars() {
    // Parse hash variables.
    var hash_vars = {};
    var hash_vars_str = window.location.hash.substr(1);
    var vars_array = hash_vars_str.split("&");
    for (var i=0; i < vars_array.length; i++) {
           var pair = vars_array[i].split("=");
           hash_vars[pair[0]] = pair[1];
    }

    // Set zoom value.
    if(hash_vars.hasOwnProperty("zoom")) {
        var temp_zoom = parseInt(hash_vars["zoom"]);
        if(temp_zoom > 0 && temp_zoom < 20) {
            set_zoom = temp_zoom;
        }
    }

    // Set secret hash if given via hash variable.
    if(hash_vars.hasOwnProperty("secret_hash")) {
        var temp_hash = hash_vars["secret_hash"];
        var re = new RegExp("^[A-Fa-f0-9]+$");
        if(temp_hash.length === 64
           && re.test(temp_hash)) {
            secret_hash = hexstringToByteArray(temp_hash);
        }
    }

    // Set mode if given via hash variable.
    if(hash_vars.hasOwnProperty("mode")) {
        var temp_mode = hash_vars["mode"];
        if(temp_mode === "live" || temp_mode === "view") {
            mode = temp_mode;
        }
    }

    // Set device_name if given via hash variable.
    if(hash_vars.hasOwnProperty("device_name")) {
        var temp_device_name = hash_vars["device_name"];
            device_name = temp_device_name;
    }

    // Set live_timeout value.
    if(hash_vars.hasOwnProperty("live_timeout")) {
        var temp_live_timeout = parseInt(hash_vars["live_timeout"]);
        if(temp_live_timeout > 0) {
            live_timeout = temp_live_timeout;
        }
    }

    // Set start and end date value if mode is view.
    if(mode === "view") {
        if(hash_vars.hasOwnProperty("start")) {
            var temp_date = parseInt(hash_vars["start"]);
            if(temp_date > 0) {
                start_date = temp_date;
            }
        }
        if(hash_vars.hasOwnProperty("end")) {
            var temp_date = parseInt(hash_vars["end"]);
            if(temp_date > 0) {
                end_date = temp_date;
            }
        }
    }
}


<?php

// written by sqall
// twitter: https://twitter.com/sqall01
// blog: https://h4des.org/blog
// github: https://github.com/sqall01
// 
// Licensed under the GNU Affero General Public License, version 3.

require_once(__DIR__ . "/config/config.php");
require_once(__DIR__ . "/lib/helper.php");
require_once(__DIR__ . "/lib/objects.php");

// Set global settings.
header("Content-type: application/json");
date_default_timezone_set("UTC");

// Start session.
$cookie_conf = session_get_cookie_params();
session_set_cookie_params($cookie_conf["lifetime"], // lifetime
                          $cookie_conf["path"], // path
                          $cookie_conf["domain"], // domain
                          TRUE, // secure
                          TRUE); // httponly
session_start();

// Check if needed data is given.
if(!isset($_GET["mode"])) {
    $result = array();
    $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
    $result["msg"] = "Mode not set.";
    die(json_encode($result));
}
if($_GET["mode"] !== "devices"
   && !isset($_GET["device"])) {
    $result = array();
    $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
    $result["msg"] = "Device is not set.";
    die(json_encode($result));
}

$mysqli = new mysqli(
    $config_mysql_server,
    $config_mysql_username,
    $config_mysql_password,
    $config_mysql_database,
    $config_mysql_port);

if($mysqli->connect_errno) {
    $result = array();
    $result["code"] = ErrorCodes::DATABASE_ERROR;
    $result["msg"] = $mysqli->connect_error;
    die(json_encode($result));
}

// Get user id.
$user_id = auth_user($mysqli);
if($user_id === -1 || $user_id === -4) {
    chasr_session_destroy();
    $result = array();
    $result["code"] = ErrorCodes::AUTH_ERROR;
    $result["msg"] = "Wrong user or password.";
    die(json_encode($result));
}
else if($user_id === -2) {
    chasr_session_destroy();
    $result = array();
    $result["code"] = ErrorCodes::DATABASE_ERROR;
    $result["msg"] = "Database error during authentication.";
    die(json_encode($result));
}
else if($user_id === -3) {
    chasr_session_destroy();
    $result = array();
    $result["code"] = ErrorCodes::SESSION_EXPIRED;
    $result["msg"] = "Authenticated session expired.";
    die(json_encode($result));
}

// Check if the mode is supported.
switch($_GET["mode"]) {
    case "last":
    case "view":
    case "devices":
        break;
    default:
        $result = array();
        $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
        $result["msg"] = "Mode unknown.";
        die(json_encode($result));
}

// Fetch data.
$fetched_data_result = NULL;
$device_name = NULL;
if(isset($_GET["device"])) {
    $device_name = $_GET["device"];
}
switch($_GET["mode"]) {
    case "last":

        // Get limit of gps positions.
        $limit = 1;
        if(isset($_GET["limit"])) {
            $limit = intval($_GET["limit"]);
        }
        if($limit < 1) {
            $limit = 1;
        }
        if($limit > 1000) {
            $limit = 1000;
        }

        // Get id of device.
        $device_id = get_device_id($mysqli, $user_id, $_GET["device"]);
        if($device_id === -1) {
            $result = array();
            $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
            $result["msg"] = "Device does not exist.";
            die(json_encode($result));
        }
        else if($device_id === -2) {
            $result = array();
            $result["code"] = ErrorCodes::DATABASE_ERROR;
            $result["msg"] = "Error while fetching device id.";
            die(json_encode($result));
        }

        // Get gps positions.
        $select_gps = "SELECT "
                      . "utctime,"
                      . "iv,"
                      . "latitude,"
                      . "longitude,"
                      . "altitude,"
                      . "speed "
                      . "FROM chasr_gps "
                      . "WHERE users_id="
                      . intval($user_id)
                      . " AND device_id="
                      . intval($device_id)
                      . " ORDER BY utctime DESC"
                      . " LIMIT "
                      . $limit;

        $fetched_data_result = $mysqli->query($select_gps);
        if(!$fetched_data_result) {
            $result = array();
            $result["code"] = ErrorCodes::DATABASE_ERROR;
            $result["msg"] = $mysqli->error;
            die(json_encode($result));
        }
        break;

    case "view":

        // Check if the time interval is given.
        if(!isset($_GET["start"])
           || !isset($_GET["end"])) {

            $result = array();
            $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
            $result["msg"] = "Time interval not set.";
            die(json_encode($result));
        }

        // Get id of device.
        $device_id = get_device_id($mysqli, $user_id, $_GET["device"]);
        if($device_id === -1) {
            $result = array();
            $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
            $result["msg"] = "Device does not exist.";
            die(json_encode($result));
        }
        else if($device_id === -2) {
            $result = array();
            $result["code"] = ErrorCodes::DATABASE_ERROR;
            $result["msg"] = "Error while fetching device id.";
            die(json_encode($result));
        }

        // Get gps positions.
        $select_gps = "SELECT "
                      . "utctime,"
                      . "iv,"
                      . "latitude,"
                      . "longitude,"
                      . "altitude,"
                      . "speed "
                      . "FROM chasr_gps "
                      . "WHERE users_id="
                      . intval($user_id)
                      . " AND device_id="
                      . intval($device_id)
                      . " AND utctime >= "
                      . intval($_GET["start"])
                      . " AND utctime <= "
                      . intval($_GET["end"])
                      . " ORDER BY utctime ASC";
        $fetched_data_result = $mysqli->query($select_gps);
        if(!$fetched_data_result) {
            $result = array();
            $result["code"] = ErrorCodes::DATABASE_ERROR;
            $result["msg"] = $mysqli->error;
            die(json_encode($result));
        }
        break;

    case "devices":
        // Get all devices positions.
        $select_devices = "SELECT DISTINCT "
                          . "name "
                          . "FROM chasr_device "
                          . "WHERE users_id="
                          . intval($user_id)
                          . " ORDER BY name ASC";
        $fetched_data_result = $mysqli->query($select_devices);
        if(!$fetched_data_result) {
            $result = array();
            $result["code"] = ErrorCodes::DATABASE_ERROR;
            $result["msg"] = $mysqli->error;
            die(json_encode($result));
        }
        break;

    default:
        $result = array();
        $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
        $result["msg"] = "Mode unknown.";
        die(json_encode($result));
}

if($fetched_data_result === NULL) {
    $result = array();
    $result["code"] = ErrorCodes::DATABASE_ERROR;
    $result["msg"] = "No data.";
    die(json_encode($result));
}

// Get users acls.
$acls = get_user_acl($mysqli, $user_id);
if($acls === -1) {
    $result = array();
    $result["code"] = ErrorCodes::DATABASE_ERROR;
    $result["msg"] = "Error while fetching user acls.";
    die(json_encode($result));
}

// Determine how many device slots a user has.
$num_device_slots = $config_chasr_num_min_devices;
if(in_array(AclCodes::CHASR_MID_DEVICES, $acls)) {
    $num_device_slots = $config_chasr_num_mid_devices;
}
if(in_array(AclCodes::CHASR_MAX_DEVICES, $acls)) {
    $num_device_slots = $config_chasr_num_max_devices;
}

// Prepare data array to return.
switch($_GET["mode"]) {
    case "devices":
        $devices_data = array();
        while($row = $fetched_data_result->fetch_assoc()) {
            $element = array("device_name" => $row["name"]);
            // Append element to array.
            $devices_data[] = $element;
        }
        $output_data = array();
        $output_data["devices"] = $devices_data;
        $output_data["avail_slots"] = $num_device_slots;
        break;

    default:
        $location_data = array();
        while($row = $fetched_data_result->fetch_assoc()) {
            $element = array("device_name" => $device_name,
                "utctime" => intval($row["utctime"]),
                "iv" => $row["iv"],
                "lat" => $row["latitude"],
                "lon" => $row["longitude"],
                "alt" => $row["altitude"],
                "speed" => $row["speed"]);
            // Append element to array.
            $location_data[] = $element;
        }
        $output_data = array();
        $output_data["locations"] = $location_data;
}

$result = array();
$result["code"] = ErrorCodes::NO_ERROR;
$result["data"] = $output_data;
$result["msg"] = "Success.";
echo json_encode($result);

?>
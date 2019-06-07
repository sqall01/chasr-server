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

// Adds gps data to the database. Dies if we have database error.
function add_gps_data($mysqli, $user_id, $gps_data) {

    foreach($gps_data as $data) {

        // Ignore duplicated entries.
        $select_gps = "SELECT users_id FROM chasr_gps WHERE "
            . "users_id="
            . intval($user_id)
            . " AND "
            . "device_name='"
            . $mysqli->real_escape_string($data["device_name"])
            . "' "
            . " AND "
            . "utctime="
            . intval($data["utctime"]);
        $result = $mysqli->query($select_gps);
        if(!$result) {
            $result = array();
            $result["code"] = ErrorCodes::DATABASE_ERROR;
            $result["msg"] = $mysqli->error;
            die(json_encode($result));
        }
        $row = $result->fetch_assoc();
        if (count($row) != 0) {
            continue;
        }

        // Insert gps data.
        $insert_gps = "INSERT INTO chasr_gps ("
            . "users_id,"
            . "device_name,"
            . "utctime,"
            . "iv,"
            . "latitude,"
            . "longitude,"
            . "altitude,"
            . "speed) "
            . " VALUES ("
            . intval($user_id) . ","
            . "'" . $mysqli->real_escape_string($data["device_name"]) ."',"
            . intval($data["utctime"]) . ","
            . "'" . $mysqli->real_escape_string($data["iv"]) . "',"
            . "'" . $mysqli->real_escape_string($data["lat"]) . "',"
            . "'" . $mysqli->real_escape_string($data["lon"]) . "',"
            . "'" . $mysqli->real_escape_string($data["alt"]) . "',"
            . "'" . $mysqli->real_escape_string($data["speed"]) . "'"
            . ")";

        $result = $mysqli->query($insert_gps);
        if(!$result) {
            $result = array();
            $result["code"] = ErrorCodes::DATABASE_ERROR;
            $result["msg"] = $mysqli->error;
            die(json_encode($result));
        }
    }
}

// Checks the received GPS data for validity.
// Returns an array with (TRUE, "msg string") if the
// data is valid, otherwise an array wtih (FALSE, "msg string").
// The function dies if we have a database error.
function check_gps_data($mysqli, $gps_data) {
    if(!is_array($gps_data)) {
        return array(FALSE, "gps_data container malformed.");
    }

    foreach($gps_data as $data) {
        if(!is_array($data)) {
            return array(FALSE, "gps_data entries malformed.");
        }

        // Check string values.
        foreach(array("iv",
                      "device_name",
                      "lat",
                      "lon",
                      "alt",
                      "speed") as $key) {

            if(!array_key_exists($key, $data)) {
                return array(FALSE, "Key " . $key . " needed.");
            }
            if(!is_string($data[$key])) {
                return array(FALSE, $key . " has to be a string.");
            }
        }
        // Check length of encrypted fields.
        foreach(array("iv",
                      "lat",
                      "lon",
                      "alt",
                      "speed") as $key) {
            if(strlen($data[$key]) != 32) {
                return array(FALSE, $key . " size needs to be 32.");
            }
        }

        // Check length of device_name.
        if(strlen($data["device_name"]) > 255) {
            return array(FALSE, "device_name longer than 255 characters.");
        }

        // Check integer values.
        if(!array_key_exists("utctime", $data)) {
            return array(FALSE, "Key utctime needed.");
        }
        if(!is_int($data["utctime"])) {
            if(is_string($data["utctime"]) && is_numeric($data["utctime"])) {
                $data["utctime"] = intval($data["utctime"]);
            }
            else {
                return array(FALSE, "utctime has to be an integer.");
            }
        }
    }

    return array(TRUE, "Success.");
}

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

if(isset($_POST["gps_data"])) {

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

    // Authenticate user..
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

    // json decode gps data.
    $gps_data = json_decode($_POST["gps_data"],
                            TRUE,
                            3);

    if(!$gps_data) {
        $result = array();
        $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
        $result["msg"] = "gps_data could not be decoded.";
        die(json_encode($result));
    }
    list($error, $msg) = check_gps_data($mysqli, $gps_data);
    if(!$error) {
        $result = array();
        $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
        $result["msg"] = $msg;
        die(json_encode($result));
    }

    add_gps_data($mysqli, $user_id, $gps_data);
}

// We do not have all data that we need, output error.
else {
    $result = array();
    $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
    $result["msg"] = "gps_data missing.";
    die(json_encode($result));
}

$result = array();
$result["code"] = ErrorCodes::NO_ERROR;
$result["msg"] = "Success.";
echo json_encode($result);

?>

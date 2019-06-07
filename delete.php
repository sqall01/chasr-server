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
if(!isset($_GET["mode"])
   || !isset($_GET["device"])) {
    $result = array();
    $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
    $result["msg"] = "Mode or device not set.";
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
    case "device":
    case "position":
        break;
    default:
        $result = array();
        $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
        $result["msg"] = "Mode unknown.";
        die(json_encode($result));
}

switch($_GET["mode"]) {

    // Delete whole device and all its data.
    case "device":

        $delete_gps = "DELETE FROM chasr_gps WHERE "
                      . "users_id = "
                      . intval($user_id)
                      . " AND "
                      . "device_name = '"
                      . $mysqli->real_escape_string($_GET["device"])
                      . "'";

        $result = $mysqli->query($delete_gps);
        if(!$result) {
            $result = array();
            $result["code"] = ErrorCodes::DATABASE_ERROR;
            $result["msg"] = $mysqli->error;
            die(json_encode($result));
        }

        break;

    // Delete single position.
    case "position":

        // Check if the time is given.
        if(!isset($_GET["utctime"])) {

            $result = array();
            $result["code"] = ErrorCodes::ILLEGAL_MSG_ERROR;
            $result["msg"] = "Time not set.";
            die(json_encode($result));
        }

        $delete_gps = "DELETE FROM chasr_gps WHERE "
                      . "users_id = "
                      . intval($user_id)
                      . " AND "
                      . "device_name = '"
                      . $mysqli->real_escape_string($_GET["device"])
                      . "' AND "
                      . "utctime = "
                      . intval($_GET["utctime"]);

        $result = $mysqli->query($delete_gps);
        if(!$result) {
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

$result = array();
$result["code"] = ErrorCodes::NO_ERROR;
$result["msg"] = "Success.";
echo json_encode($result);

?>
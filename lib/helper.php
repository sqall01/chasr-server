<?php

// written by sqall
// twitter: https://twitter.com/sqall01
// blog: https://h4des.org/blog
// github: https://github.com/sqall01
// 
// Licensed under the GNU Affero General Public License, version 3.

require_once(__DIR__ . "/../config/config.php");
require_once(__DIR__ . "/objects.php");

// Authenticates the user. Returns the user id when successful,
// returns -1 if user authentication fails,
// returns -2 if the database connection fails,
// returns -3 if the session expired,
// returns -4 if no authentication data was given.
function auth_user($mysqli) {
    global $config_session_expire;

    $user_id = -1;

    // Authenticate use via username and password.
    if(isset($_POST["user"]) 
       && isset($_POST["password"])) {

        // Check authentication.
        $user_id = auth_user_password($mysqli,
                                      $_POST["user"],
                                      $_POST["password"]);

        $_SESSION["chasr_user_id"] = $user_id;

        // Set time when the session expires.
        $_SESSION["chasr_expires"] = time() + $config_session_expire; 
    }

    // Use session for authentication.
    else if(isset($_SESSION["chasr_user_id"])
            && isset($_SESSION["chasr_expires"])) {

        // Session expired.
        if($_SESSION["chasr_expires"] < time()) {
            chasr_session_destroy();
            return -3;
        }

        // Session is valid, renew it.
        else {
            $user_id = $_SESSION["chasr_user_id"];

            // Get user id from database.
            $select_active = "SELECT active FROM users WHERE id="
                             . intval($user_id);
            $result = $mysqli->query($select_active);
            if(!$result) {
                return -2;
            }

            $row = $result->fetch_assoc();

            // Check if we have a result.
            if (count($row) != 1) {
                return -1;
            }

            // Check if the user account is activated.
            if(!$row["active"]) {
                return -1;
            }

            // Set time when the session expires.
            $_SESSION["chasr_expires"] = time() + $config_session_expire;
        }
    }

    // No authentication data given.
    else {
        return -4;
    }

    return $user_id;
}

// Authenticates the user. Returns the user id when successful,
// returns -1 if user authentication fails,
// returns -2 if the database connection fails.
function auth_user_password($mysqli, $user, $password) {

    // Get user id from database.
    $select_id = "SELECT id, active FROM users WHERE email='"
                  . $mysqli->real_escape_string($user)
                  . "'";
    $result = $mysqli->query($select_id);
    if(!$result) {
        return -2;
    }

    $row = $result->fetch_assoc();

    // Check if we have a result.
    if (count($row) != 2) {
        return -1;
    }

    // Check if the user account is activated.
    if(!$row["active"]) {
        return -1;
    }

    $user_id = $row["id"];

    // Get hash from database.
    $select_hash = "SELECT password_hash FROM passwords WHERE users_id="
                   . intval($user_id);
    $result = $mysqli->query($select_hash);
    if(!$result) {
        return -2;
    }

    $row = $result->fetch_assoc();
    if (count($row) == 0) {
        return -1;
    }

    $hash = $row["password_hash"];

    // Verify user password.
    if(!password_verify($password, $hash)) {
        $user_id = -1;
    }

    return $user_id;
}

// Destroys the ChasR part of the session.
function chasr_session_destroy() {
    if(isset($_SESSION["chasr_user_id"])) {
        unset($_SESSION["chasr_user_id"]);
    }
    if(isset($_SESSION["chasr_expires"])) {
        unset($_SESSION["chasr_expires"]);
    }
}

// Gets device id from database for given device,
// returns -1 if device does not exist,
// returns -2 if the database connection fails.
function get_device_id($mysqli, $user_id, $device_name) {
    // Get id of device.
    $select_device = "SELECT id, "
                     . "name "
                     . "FROM chasr_device "
                     . "WHERE users_id="
                     . intval($user_id)
                     . " AND name='"
                     . $mysqli->real_escape_string($device_name)
                     . "'";
    $result = $mysqli->query($select_device);
    if(!$result) {
        return -2;
    }
    $row = $result->fetch_assoc();
    if(!$row) {
        return -1;
    }
    $device_id = $row["id"];
    return $device_id;
}

// Gets users acls from database,
// returns -1 if the database connection fails,
// returns array with acls of user.
function get_user_acl($mysqli, $user_id) {
    // Get id of device.
    $select_acl = "SELECT acl "
                  . "FROM acl "
                  . "WHERE users_id="
                  . intval($user_id);
    $result = $mysqli->query($select_acl);
    if(!$result) {
        return -1;
    }

    $acls = array();
    while($row = $result->fetch_assoc()) {
        $acls[] = $row["acl"];
    }
    return $acls;
}

?>
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
require_once(__DIR__ . "/lib/output.php");

// Set global settings.
date_default_timezone_set("UTC");

// Start session.
$cookie_conf = session_get_cookie_params();
session_set_cookie_params($cookie_conf["lifetime"], // lifetime
                          $cookie_conf["path"], // path
                          $cookie_conf["domain"], // domain
                          TRUE, // secure
                          TRUE); // httponly
session_start();

$mysqli = new mysqli(
    $config_mysql_server,
    $config_mysql_username,
    $config_mysql_password,
    $config_mysql_database,
    $config_mysql_port);

if($mysqli->connect_errno) {
    die("Database error.");
}

// Logout user if we should do it.
if(isset($_GET["logout"]) && $_GET["logout"] === "1") {
    chasr_session_destroy();
}

// Authenticate user.
$user_id = auth_user($mysqli);

// User authentication failed.
if($user_id === -1) {
    chasr_session_destroy();
    output_login_form(ErrorCodes::AUTH_ERROR);
}

// Database error.
else if($user_id === -2) {
    chasr_session_destroy();
    die("Database error.");
}

// Session expired.
else if($user_id === -3) {
    chasr_session_destroy();
    output_login_form(ErrorCodes::SESSION_EXPIRED);
}

// No authentication data given.
else if($user_id === -4) {
    chasr_session_destroy();
    output_login_form(ErrorCodes::NO_ERROR);
}

// User is authenticated.
else {
    output_authenticated();
}

?>
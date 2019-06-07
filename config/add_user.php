<?php

// written by sqall
// twitter: https://twitter.com/sqall01
// blog: https://h4des.org/blog
// github: https://github.com/sqall01
// 
// Licensed under the GNU Affero General Public License, version 3.

// Include connection data for mysql db.
require_once("./config.php");

// Configuration to create a user.
$activated = FALSE;
$user_to_create = "test_user@alertr.de";
$pass_to_create = "<SECRET>";

// Check if user creation is activated.
if($activated == FALSE) {
	die("Script deactivated.");
}

$mysqli = new mysqli(
    $config_mysql_server,
    $config_mysql_username,
    $config_mysql_password,
    $config_mysql_database,
    $config_mysql_port);

if($mysqli->connect_errno) {
    die("Error: Database connection failed: " . $mysqli->connect_error);
}

date_default_timezone_set("UTC");

// Add user.
$insert_user_sql = "INSERT INTO users (email, active) "
	. "VALUES ('"
	. $mysqli->real_escape_string($user_to_create)
	. "', 1)";
$result = $mysqli->query($insert_user_sql);
if(!$result) {
	die($mysqli->error);
}

// Create hash.
$hash = password_hash($pass_to_create, PASSWORD_BCRYPT);
if($hash === FALSE) {
	die("Error during hash creation.");
}

$insert_pass_sql = "INSERT INTO passwords (users_id, password_hash) VALUES "
	. "("
	. intval($mysqli->insert_id)
	. ", '"
	. $mysqli->real_escape_string($hash)
	. "')";
$result = $mysqli->query($insert_pass_sql);
if(!$result) {
	die($mysqli->error);
}

echo "User '" . $user_to_create . "'' created.";

?>

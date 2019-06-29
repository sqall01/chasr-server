<?php

// written by sqall
// twitter: https://twitter.com/sqall01
// blog: https://h4des.org/blog
// github: https://github.com/sqall01
// 
// Licensed under the GNU Affero General Public License, version 3.

// Include connection data for mysql db.
require_once("./config.php");

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

// Create tables.
$create_users_table = "CREATE TABLE IF NOT EXISTS users ("
    . "id INTEGER PRIMARY KEY AUTO_INCREMENT,"
    . "email VARCHAR(255) NOT NULL UNIQUE,"
    . "active BOOLEAN NOT NULL"
    . ");";

$create_acl_table = "CREATE TABLE IF NOT EXISTS acl ("
    . "users_id INTEGER NOT NULL,"
    . "acl INTEGER NOT NULL,"
    . "PRIMARY KEY(users_id, acl),"
    . "FOREIGN KEY(users_id) REFERENCES users(id)"
    . ");";

$create_tokens_table = "CREATE TABLE IF NOT EXISTS tokens ("
    . "users_id INTEGER PRIMARY KEY,"
    . "token VARCHAR(255) NOT NULL,"
    . "timestamp INTEGER NOT NULL,"
    . "expiration INTEGER NOT NULL,"
    . "FOREIGN KEY(users_id) REFERENCES users(id)"
    . ");";

$create_passwords_table = "CREATE TABLE IF NOT EXISTS passwords (" 
    . "users_id INTEGER PRIMARY KEY,"
    . "password_hash VARCHAR(255) NOT NULL,"
    . "FOREIGN KEY(users_id) REFERENCES users(id)"
    . ");";

$create_device_table = "CREATE TABLE IF NOT EXISTS chasr_device ("
    . "id INTEGER PRIMARY KEY AUTO_INCREMENT,"
    . "users_id INTEGER NOT NULL,"
    . "name VARCHAR(255) NOT NULL,"
    . "FOREIGN KEY(users_id) REFERENCES users(id)"
    . ");";

$create_gps_table = "CREATE TABLE IF NOT EXISTS chasr_gps ("
    . "users_id INTEGER NOT NULL,"
    . "device_id INTEGER NOT NULL,"
    . "utctime INTEGER NOT NULL,"
    . "iv CHAR(32) NOT NULL,"
    . "latitude CHAR(32) NOT NULL,"
    . "longitude CHAR(32) NOT NULL,"
    . "altitude CHAR(32) NOT NULL,"
    . "speed CHAR(32) NOT NULL,"
    . "authtag CHAR(64) NOT NULL,"
    . "PRIMARY KEY(users_id, device_id, utctime),"
    . "FOREIGN KEY(device_id) REFERENCES chasr_device(id),"
    . "FOREIGN KEY(users_id) REFERENCES users(id)"
    . ");";

if($mysqli->query($create_users_table) !== TRUE) {
    die("Error: Creating 'users' table failed.");
}
if($mysqli->query($create_acl_table) !== TRUE) {
    die("Error: Creating 'acl' table failed.");
}
if($mysqli->query($create_tokens_table) !== TRUE) {
    die("Error: Creating 'tokens' table failed.");
}
if($mysqli->query($create_passwords_table) !== TRUE) {
    die("Error: Creating 'passwords' table failed.");
}
if($mysqli->query($create_device_table) !== TRUE) {
    die("Error: Creating 'chasr_device' table failed.");
}
if($mysqli->query($create_gps_table) !== TRUE) {
    die("Error: Creating 'chasr_gps' table failed.");
}

echo "Installation done."

?>

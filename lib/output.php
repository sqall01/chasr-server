<?php

// written by sqall
// twitter: https://twitter.com/sqall01
// blog: https://h4des.org/blog
// github: https://github.com/sqall01
// 
// Licensed under the GNU Affero General Public License, version 3.

require_once(__DIR__ . "/../lib/objects.php");

function output_login_form($reason) {

    include("./html/header.html");

    switch($reason) {
        case ErrorCodes::AUTH_ERROR:
            echo "Authentication failed.";
            break;

        case ErrorCodes::SESSION_EXPIRED:
            echo "Session expired.";
            break;

        default:
            break;
    }

    include("./html/login_form.html");
    include("./html/footer.html");
}

function output_authenticated() {

    include("./html/header.html");
    include("./html/login_authenticated.html");
    include("./html/footer.html");
}

function output_map() {
    // Differentiate between browser and Android App.
    if (strpos($_SERVER["HTTP_USER_AGENT"], "ChasR Map Test") !== FALSE) {
        include("./html/map_android_test.html");
    }
    else if (strpos($_SERVER["HTTP_USER_AGENT"], "ChasR Map") !== FALSE) {
        include("./html/map_android.html");
    }
    else {
        include("./html/map_browser.html");
    }
}

function output_login_redirect() {
    include("./html/login_redirect.html");
}

?>
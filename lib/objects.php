<?php

// written by sqall
// twitter: https://twitter.com/sqall01
// blog: https://h4des.org/blog
// github: https://github.com/sqall01
// 
// Licensed under the GNU Affero General Public License, version 3.

abstract class ErrorCodes {
    const NO_ERROR = 0;
    const DATABASE_ERROR = 1;
    const AUTH_ERROR = 2;
    const ILLEGAL_MSG_ERROR = 3;
    const SESSION_EXPIRED = 4;
    const ACL_ERROR = 5;
}

abstract class AclCodes {
    const ALERTR_NOTIFICATION_CHANNEL = 0;
    const CHASR_MID_DEVICES = 1;
    const CHASR_MAX_DEVICES = 2;
}

?>
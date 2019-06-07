![ChasR Logo](img/chasr_logo_black.png)

[ChasR is an open-source end-to-end encrypted GPS tracking system](https://alertr.de/chasr). It can be used directly as [service](https://alertr.de/chasr) or hosted by oneself. The goal of ChasR is to offer a privacy protecting GPS tracking service by using end-to-end encryption. This means that the sensitive location data of a user is directly encrypted on the device before it is sent to the server. Since the server does not know the key for the encryption, it cannot see the location data. The stored location data can be accessed either via Android App or web interface. Again, the location data is decrypted on the device and hence the server has no way of knowing the location of the user. All you need to use ChasR is a free account and a logging application (on Android or Linux).

The ChasR GPS Tracking System is separated into multiple components:

* ChasR Server ([Github](https://github.com/sqall01/chasr-server) | [Service](https://alertr.de/chasr))
* ChasR Android Logger ([Github](https://github.com/sqall01/chasr-android-logger))
* ChasR Android Map ([Github](https://github.com/sqall01/chasr-android-map))

Additionally, the ChasR GPS Tracking System can be used as part of the [AlertR Alarm and Monitoring System](https://alertr.de) (for example as a car alarm system).


# ChasR Server

This is the server component of the ChasR GPS Tracking System. Its task is to store the encrypted GPS data, providing access to it via a well defined [API](https://github.com/sqall01/chasr-server/wiki) and to give the user access to the data via a map view. The server uses a MySQL database as backend to store the GPS data and OpenLayer with OpenStreetMap to provide a map view.


## Install

Installing the server is rather simple. It needs a MySQL server and PHP 7. You have to create a MySQL user for the server and a database for it. Rename the configuration template file `config/config.php.template` to `config/config.php` and insert the needed information into it. Afterwards, execute `config/install.php` to create the needed database layout.

To create a user you can use the `config/add_user.php` file. You have to set the values in this file to create the corresponding user.

All clients are written to use HTTPS for security reasons. Therefore, if you want to host the server yourself you have to configure your webserver to serve HTTPS with a valid certificate.


# Supporting ChasR
<a name="supporting_chasr"/>

If you like this project you can help to support it by contributing to it. You can contribute by writing tutorials, creating and documenting exciting new ideas to use ChasR (for example on [reddit](https://www.reddit.com/r/AlertR/)), writing code for it, and so on.

If you do not know how to do any of it or do not have the time, you can support the project by [donating](https://alertr.de/donations.php) or support me on [Patreon](https://www.patreon.com/sqall). Since the service has a monthly upkeep, the donation helps to keep these services free for everyone.

### Patreon
[![Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/sqall)

### Paypal
[![Donate](https://www.paypalobjects.com/en_US/DE/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=TVHGG76JVCSGC)


# Bugs and Feedback
<a name="bugs_and_feedback"/>

For questions, bugs and discussion please use the Github issues.
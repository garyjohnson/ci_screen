# ci_screen
Native QT5 app for showing build status from one or multiple Jenkins CI servers. Uses PyQt5 for Python bindings.

Supports unauthenticated and HTTP basic auth using username & token. `cc.xml must be available via these means (some Jenkins plugins allow granular access control to cc.xml).

## Configuration
Configuration is handled in ci_screen.cfg. 

### general

#### poll_rate_seconds
Number of seconds that each CI server will be polled for updates. Default is 10 seconds.

#### rotation
Degrees of rotation. Used for rotating the screen for TVs or displays mounted sideways. This is a preferrable alternative to using /boot/config.txt on the Raspberry Pi, as that method causes severe performance issues. Default is 0 degrees.

#### holiday
When enabled, shows animations on certain days of the year provided that all jobs have passed. Default is true.

### ci_servers

#### sections
A comma-seperated list of sections. Each name must match a section in the config file.

### {ci_server_section}
A section defined in the sections property of the ci_servers section.

#### url
A required url of the Jenkins server (e.g., http://ci.server.com)

#### username
Username to be used if HTTP basic auth is required to access cc.xml.

#### token
Auth token to be used if HTTP basic auth is required to access cc.xml.

### ci_servers Example
In this example, ci_screen is configured to pull from two CI servers. The first, ci.foo.com, exposes cc.xml without authentication. The second, ci.bar.net, has HTTP basic auth enabled and provides a username and token. Both foo and bar sections are defined using the `sections` property.

```
[ci_servers]
sections=foo,bar

[foo]
url=http://ci.foo.com

[bar]
url=https://ci.bar.net
username=myusername
token=1042081038133300184013931000109138
```

## Prerequisites

QT5, sip, and PyQt5 must be installed.

### OSX Install

Install QT5 using the installer from [qt.io](qt.io).
Use homebrew to install python3, sip, and pyqt5. Alternatively you can build sip and pyqt from source.

### Raspbian Install

To run fullscreen using eglfs (without the overhead of a windowing system) you can follow [this gist](https://gist.github.com/garyjohnson/f041d2274dccd6641c51).

## Running

Install python requirements using `pip install -r requirements.txt` and run `./main.py`.

## Running tests

`pip install tox` and run `tox`. To run tests. Currently they target python 3.4 or 3.5.

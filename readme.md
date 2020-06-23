<div align="center">

  <img src="https://github.com/jakebrehm/multitooner/blob/master/img/logo.png" alt=" MultiTooner Logo"/>

  <br>
  <br>

  <h1>A Toontown Rewritten companion for MacOS.</h1>

  <br>

  <img src="https://img.shields.io/github/last-commit/jakebrehm/multitooner?style=for-the-badge&color=yellow" alt="Last Commit"></img>
  <img src="https://img.shields.io/github/commit-activity/w/jakebrehm/multitooner?style=for-the-badge&color=yellow" alt="Commit Activity"></img>
  <img src="https://img.shields.io/github/license/jakebrehm/multitooner?style=for-the-badge&color=yellow" alt="MIT License"></img>
  <br>
  <img src="https://img.shields.io/badge/Made%20With-Python%203.7-violet.svg?style=for-the-badge&logo=Python" alt="Made with Python 3.7"></img>

  <!-- <img src="https://github.com/jakebrehm/multitooner/blob/master/img/demo.gif" alt="MultiTooner Demo"></img> -->

</div>

<br>

## What does it do?

A companion to *[Toontown Rewritten](https://www.toontownrewritten.com)*, **MultiTooner** allows you to store login information for an unlimited amount of accounts and start playing them from the menu bar.

You are also able to receive notifications for new invasions.

## What do I need?

Whether you are using the frozen application or the source code, [**Toontown Rewritten**](https://www.toontownrewritten.com/play) is a requirement for launching sessions. This is because *MultiTooner* does not include any game-related files.

If you are running the app via the source code, **MultiTooner** uses the following third-party packages:
- **[rumps](https://github.com/jaredks/rumps)** to actually build the menu bar app
- **[pyobjc-framework-LaunchServices](https://pypi.org/project/pyobjc-framework-LaunchServices/)** to help with login on startup functionality
- **[tooner](http://github.com/jakebrehm/tooner)**, my own package, to launch a Toontown Rewritten session

However, note that this application **only supports MacOS**.

Please note that, in order to launch a sessions, you must grant the application **Input Monitoring** permissions in **System Preferences > Security & Privacy**. Similarly, if you want to receive invasion notifications, you must allow the application to send you notifications.

## How can I get this set up?

See the [latest release](https://github.com/jakebrehm/multitooner/releases/latest) of this project for a download of the standalone application.

If you want to take the harder route, you can also clone this repository via the command

```
git clone https://github.com/jakebrehm/multitooner.git
```

and then navigate to the cloned directory in a terminal. Make sure you are in the outer **multitooner** folder, and not the nested folder with the same name, and then you can build the application using [py2app](https://github.com/ronaldoussoren/py2app). Run the command

```
python script/setup.py py2app
```

and the application will then appear in the **dist** folder.

## Issues and future plans

- As described by the *Toontown Rewritten* team, the [Invasion API](https://github.com/ToontownRewritten/api-doc/blob/master/invasions.md) is typically not up to date. Unfortunately, there's nothing that can be done about this in *MultiTooner*.
- Login info for each account is stored in a plain text configuration file. This shouldn't be a problem assuming no one has access to your computer, but I'd still like to improve on it in the future.
- Currently, the windows for adding and removing accounts are very clunky. As useful as it is, I'm limited by what *rumps* has to offer. I'd like to look into this more eventually, or find an alternative solution.

## Authors
- **Jake Brehm** - *Initial Work* - [Email](mailto:mail@jakebrehm.com) | [Github](http://github.com/jakebrehm) | [LinkedIn](http://linkedin.com/in/jacobbrehm)
<div align="center">

  <img src="https://github.com/jakebrehm/multitooner/blob/master/img/logo.png" alt=" MultiTooner Logo"/>

  <br>
  <br>

  <h1>A Toontown Rewritten multi-launcher for MacOS.</h1>

  <br>

  <img src="https://img.shields.io/github/last-commit/jakebrehm/multitooner?style=for-the-badge&color=yellow" alt="Last Commit"></img>
  <img src="https://img.shields.io/github/commit-activity/w/jakebrehm/multitooner?style=for-the-badge&color=yellow" alt="Commit Activity"></img>
  <img src="https://img.shields.io/github/license/jakebrehm/multitooner?style=for-the-badge&color=yellow" alt="MIT License"></img>
  <br>
  <img src="https://img.shields.io/badge/Made%20With-Python%203.7-violet.svg?style=for-the-badge&logo=Python" alt="Made with Python 3.7"></img>

  <!-- <img src="https://github.com/jakebrehm/multitooner/blob/master/img/demo.gif" alt="MultiTooner Demo"></img> -->

</div>

## What does it do?

A companion to *[Toontown Rewritten](https://www.toontownrewritten.com)*, **MultiTooner** allows you to store login information for an unlimited amount of accounts and start playing them from the menu bar.

You are also able to add or remove stored accounts from the menu bar alone.

## Requirements

Firstly, this application **only works on MacOS**, and it uses the following packages:
- **[rumps]()** to actually build the menu bar app
- **[pyobjc-framework-LaunchServices]()** to help with login on startup functionality
- **[tooner](http://github.com/jakebrehm/tooner)**, my own package, to launch a Toontown Rewritten session

## How can I get this set up?

Very soon, I'll release a frozen build of the project, but for now, clone this repository via the command

```
git clone https://github.com/jakebrehm/multitooner.git
```

and then navigate to the directory in a terminal. Make sure you are in the outer **multitooner** folder, and not the nested folder with the same name, and then you can build the application using [py2app](https://github.com/ronaldoussoren/py2app). Run the command

```
python script/setup.py py2app
```

and the application will then appear in the **dist** folder.

## Authors
- **Jake Brehm** - *Initial Work* - [Email](mailto:mail@jakebrehm.com) | [Github](http://github.com/jakebrehm) | [LinkedIn](http://linkedin.com/in/jacobbrehm)
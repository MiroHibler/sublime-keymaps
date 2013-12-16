# Sublime Text Keymap Helper

Plugin for Sublime Text 2/3 editor that enables searching for keymaps by function as well as showing all enabled keymaps in a searchable color-coded list - Cheat Sheet.

## Features

* **NEW!** Search for keymaps by function
* Shows searchable color-coded Cheat Sheet (overview) of keymaps
* Open the keymap file to edit chosen keymap

## Usage

### Find a keymap for...

* Invoke via <kbd>⌃</kbd><kbd>⌥</kbd><kbd>?</kbd> / <kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>?</kbd> (menu: `Tools` -> `Keymaps` -> `Find a keymap for...`)
* Start typing the function you need keymap for and - voilà!
* Additionaly, hit <kbd>⏎</kbd> to execute it!

![Find a keymap for...](https://raw.github.com/MiroHibler/sublime-keymaps/master/images/quick_panel.gif)

### Cheat Sheet

* Invoke via <kbd>⌃</kbd><kbd>⌥</kbd><kbd>\_</kbd> / <kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>\_</kbd> (menu: `Tools` -> `Keymaps` -> `Cheat Sheet`)
* Use these commands to browse the Cheat Sheet and select an entry to open corresponding `.sublime-keymap` file and edit the keymap

<kbd>⌃</kbd><kbd>⌥</kbd><kbd>⇧</kbd><kbd>↓</kbd> / <kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>⇧</kbd><kbd>↓</kbd>: **Navigate Forward**

<kbd>⌃</kbd><kbd>⌥</kbd><kbd>⇧</kbd><kbd>↑</kbd> / <kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>⇧</kbd><kbd>↑</kbd>: **Navigate Backward**

<kbd>⌃</kbd><kbd>⌥</kbd><kbd>⇧</kbd><kbd>C</kbd> / <kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>⇧</kbd><kbd>C</kbd>: **Clear Selection**

<kbd>⌃</kbd><kbd>⌥</kbd><kbd>⇧</kbd><kbd>⏎</kbd> / <kbd>Ctrl</kbd><kbd>Alt</kbd><kbd>⇧</kbd><kbd>⏎</kbd>: **Open .sublime-keymap File For Editing**

or double-click _previously selected_ line while holding <kbd>⌃</kbd><kbd>⌥</kbd> / <kbd>Ctrl</kbd><kbd>Alt</kbd>

Here's an example of possible output (OS X, truncated):

![Cheat Sheet](https://raw.github.com/MiroHibler/sublime-keymaps/master/images/cheat_sheet.png)


## How to install

*Warning:* If you experience problems or editor crashes please [file an issue](https://github.com/MiroHibler/sublime-keymaps/issues).

With [Package Control](http://wbond.net/sublime_packages/package_control):

1. Run “Package Control: Install Package” command, find and install `Keymaps` plugin.
2. Restart ST editor (if required)

## Options

~~Mac~~ ALL users can now opt for pretty simbols instead of text for keys.

Go to `Preferences` -> `Settings - User` and add this to the file:

~~`"keymaps": { "show_osx_keys": true }`~~

`"keymaps": { "show_pretty_keys": true }`


## Changelog

### v1.3.1

* Bug fix for issue #9: parse Default.sublime-keymap file in packages

### v1.3.0

* Search for keymaps by function
* Simplified keymaps for Keymaps itself
* Moved to Tools menu
* Bug fixes (yes, I know - again :P )

### v1.2.3

* Bumped internal version number

### v1.2.2

* Fixed bug in Keymaps.py in v1.2.1 (and v1.2.0) preventing plugin running

### v1.2.1

* Fixed bug in messages.json preventing plugin upgrade

### v1.2.0

* Additional Sublime Text 3 compatibility
* More Cross-platform pretty simbols instead of text for keys (optional)
* Bug fixes

### v1.1.0

* Sublime Text 3 compatibility
* Cleaned up and center-aligned listing
* Cross-platform pretty simbols instead of text for keys (optional)
* Bug fixes

### v1.0.0

* Initial release

## Acknowledgments

Inspired by [KeymapViewer](https://github.com/wwwjfy/KeymapViewer)

## Copyright and license

Copyright © 2013 @[MiroHibler](http://twitter.com/MiroHibler)

Licensed under the [**MIT**](http://miro.mit-license.org) license.

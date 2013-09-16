# Sublime Text Keymaps Cheat Sheet

## ST3 compatible!

Inspired by [KeymapViewer](https://github.com/wwwjfy/KeymapViewer), this plugin for Sublime Text editor shows all enabled keymaps in a searchable color-coded list.

User can select an entry which will open corresponding `.sublime-keymap` file and select the keymap for editing.

Here's an example of possible output (OS X, truncated):
```
                             Clipboard History (6)                              

                                  [ ⌘ C ]: Clipboard Copy
                                  [ ⌘ X ]: Clipboard Copy
                             [ ⌃ ⌥ ⌘ V ]: Clipboard History
                             [ ⌃ ⌥ ⌘ D ]: Clipboard Clear History
                               [ ⇧ ⌘ V ]: Clipboard Paste Previous
                             [ ⇧ ⌥ ⌘ V ]: Clipboard Paste Next
```

## Features

- Shows Cheat Sheet (overview) of keymaps
- Helps search for keymaps
- Open the keymap file to edit chosen keymap

## Usage

- View -> Keymaps Cheat Sheet, or <kbd>⌃</kbd> <kbd>⌥</kbd> <kbd>?</kbd> / <kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>?</kbd>

Use these commands to browse the Cheat Sheet:

<kbd>⌃</kbd> <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>N</kbd> / <kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>⇧</kbd> <kbd>N</kbd>: **Navigate Forward**

<kbd>⌃</kbd> <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>↓</kbd> / <kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>⇧</kbd> <kbd>↓</kbd>: **Navigate Forward**

<kbd>⌃</kbd> <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>J</kbd> / <kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>⇧</kbd> <kbd>J</kbd>: **Navigate Forward**

<kbd>⌃</kbd> <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>P</kbd> / <kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>⇧</kbd> <kbd>P</kbd>: **Navigate Backward**

<kbd>⌃</kbd> <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>↑</kbd> / <kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>⇧</kbd> <kbd>↑</kbd>: **Navigate Backward**

<kbd>⌃</kbd> <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>K</kbd> / <kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>⇧</kbd> <kbd>K</kbd>: **Navigate Backward**

<kbd>⌃</kbd> <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>C</kbd> / <kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>⇧</kbd> <kbd>C</kbd>: **Clear Selection**

<kbd>⌃</kbd> <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>⏎</kbd> / <kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>⇧</kbd> <kbd>⏎</kbd>: **Open Keymap File For Edit**

- or double-click _previously selected_ line while holding <kbd>⌃</kbd> <kbd>⌥</kbd> <kbd>⇧</kbd> / <kbd>Ctrl</kbd> <kbd>Alt</kbd> <kbd>⇧</kbd>

## How to install

*Warning:* If you experience problems or editor crashes please [file an issue](https://github.com/MiroHibler/sublime-keymaps/issues).

With [Package Control](http://wbond.net/sublime_packages/package_control):

1. Run “Package Control: Install Package” command, find and install `Keymaps` plugin.
2. Restart ST editor (if required)

## Options

~~Mac~~ ALL users can now opt for pretty simbols instead of text for keys.

Go to `Preferences` > `Settings - User` and add this to the file:

~~`"keymaps": { "show_osx_keys": true }`~~

`"keymaps": { "show_pretty_keys": true }`


## Changelog

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

## Copyright and license

Copyright © 2013 @[MiroHibler](http://twitter.com/MiroHibler) 

Licensed under the [**MIT**](./LICENSE.txt) license.
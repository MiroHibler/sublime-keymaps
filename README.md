# Sublime Text 2/3 Keymaps Cheat Sheet

## Now ST3 compatible!

Inspired by [KeymapViewer](https://github.com/wwwjfy/KeymapViewer), this plugin for Sublime Text editor shows all enabled keymaps in a searchable color-coded list.

User can select an entry which will open corresponding `.sublime-keymap` file and select the keymap for editing.

Here's an example of possible output (OS X, truncated):
```
                             Clipboard History (6)                              

                                 [ ⌘ C ]: clipboard_copy
                                 [ ⌘ X ]: clipboard_copy
                            [ ⌘ ⌃ ⌥ V ]: Clipboard History
                            [ ⌘ ⌃ ⌥ D ]: clipboard_clear_history
                              [ ⌘ ⇧ V ]: clipboard_paste_previous
                            [ ⌘ ⇧ ⌥ V ]: clipboard_paste_next
```

## Features

- Shows Cheat Sheet (overview) of keymaps
- Helps search for keymaps
- Open the keymap file for the chosen keymap

## Usage

- View -> Keymaps Cheat Sheet, or <kbd>⌃</kbd>+<kbd>⌥</kbd>+<kbd>?</kbd> / <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>?</kbd>

Use these commands to browse the Cheat Sheet:

<kbd>⌃</kbd>+<kbd>⌥</kbd>+<kbd>⇧</kbd>+<kbd>N</kbd> / <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>SHIFT</kbd>+<kbd>N</kbd>: **Navigate Forward**

<kbd>⌃</kbd>+<kbd>⌥</kbd>+<kbd>⇧</kbd>+<kbd>DOWN</kbd> / <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>SHIFT</kbd>+<kbd>DOWN</kbd>: **Navigate Forward**

<kbd>⌃</kbd>+<kbd>⌥</kbd>+<kbd>⇧</kbd>+<kbd>J</kbd> / <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>SHIFT</kbd>+<kbd>J</kbd>: **Navigate Forward**

<kbd>⌃</kbd>+<kbd>⌥</kbd>+<kbd>⇧</kbd>+<kbd>P</kbd> / <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>SHIFT</kbd>+<kbd>P</kbd>: **Navigate Backward**

<kbd>⌃</kbd>+<kbd>⌥</kbd>+<kbd>⇧</kbd>+<kbd>UP</kbd> / <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>SHIFT</kbd>+<kbd>UP</kbd>: **Navigate Backward**

<kbd>⌃</kbd>+<kbd>⌥</kbd>+<kbd>⇧</kbd>+<kbd>K</kbd> / <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>SHIFT</kbd>+<kbd>K</kbd>: **Navigate Backward**

<kbd>⌃</kbd>+<kbd>⌥</kbd>+<kbd>⇧</kbd>+<kbd>C</kbd> / <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>SHIFT</kbd>+<kbd>C</kbd>: **Clear Selection**

<kbd>⌃</kbd>+<kbd>⌥</kbd>+<kbd>⇧</kbd>+<kbd>ENTER</kbd> / <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>SHIFT</kbd>+<kbd>ENTER</kbd>: **Open Keymap File For Edit**

- or double-click _previously selected_ line while holding <kbd>⌃</kbd>+<kbd>⌥</kbd>+<kbd>⇧</kbd> / <kbd>CTRL</kbd>+<kbd>ALT</kbd>+<kbd>SHIFT</kbd>

## How to install

*Warning:* If you experience problems or editor crashes please [file an issue](https://github.com/MiroHibler/sublime-keymaps/issues).

With [Package Control](http://wbond.net/sublime_packages/package_control):

1. Run “Package Control: Install Package” command, find and install `Keymaps` plugin.
2. Restart ST editor (if required)

Manually:

1. Clone or [download](https://github.com/MiroHibler/sublime-keymaps/archive/master.zip) git repo into your packages folder (in ST, find Browse Packages... menu item to open this folder)
2. Restart ST editor (if required)

## Options

~~Mac~~ ALL users can now opt for pretty simbols instead of text for keys.

Go to `Preferences` > `Settings - User` and add this to the file:

~~`"keymaps": { "show_osx_keys": true }`~~

`"keymaps": { "show_pretty_keys": true }`


## Changelog

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
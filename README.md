# Sublime Text Keymaps Cheat Sheet

Inspired by [KeymapViewer](https://github.com/wwwjfy/KeymapViewer), this plugin for Sublime Text editor shows all enabled keymaps in a searchable color-coded list.

User can select an entry which will open corresponding `.sublime-keymap` file and select the keymap for eventual editing.

Here's an example of possible output (OS X, truncated):

     Case Conversion (7)
        [ ⌃ ⌥ C ], [ ⌃ ⌥ S ]: Convert Case: snake_case
        [ ⌃ ⌥ C ], [ ⌃ ⌥ C ]: Convert Case: camelCase
        [ ⌃ ⌥ C ], [ ⌃ ⌥ P ]: Convert Case: PascalCase
        [ ⌃ ⌥ C ], [ ⌃ ⌥ D ]: Convert Case: dot.case
        [ ⌃ ⌥ C ], [ ⌃ ⌥ H ]: Convert Case: dash-case
        [ ⌃ ⌥ C ], [ ⌃ ⌥ W ]: Convert Case: separate␣words
        [ ⌃ ⌥ C ], [ ⌃ ⌥ / ]: Convert Case: separate/with/slash


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

## How to install

*Warning:* If you experience problems or editor crashes please [file an issue](https://github.com/MiroHibler/sublime-keymaps/issues).

With [Package Control](http://wbond.net/sublime_packages/package_control):

1. Run “Package Control: Install Package” command, find and install `Keymaps` plugin.
2. Restart ST editor (if required)

Manually:

1. Clone or [download](https://github.com/MiroHibler/sublime-keymaps/archive/master.zip) git repo into your packages folder (in ST, find Browse Packages... menu item to open this folder)
2. Restart ST editor (if required)

## Options

Mac users can opt for a nice simbols instead of text for keys.

Go to `Sublime Text 2` > `Preferences` > `Settings - User` and add this to the file:

`"keymaps": { "show_osx_keys": true }`


## Changelog

### v1.0.0

* Initial release

## Copyright and license

Copyright © 2013 [Miroslav Hibler](http://miro.hibler.me) 

Licensed under the [**MIT**](./LICENSE.txt) license.
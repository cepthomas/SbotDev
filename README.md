# Sublime Text Plugin Incubator and Playground

Just a big messy area. These are not the codes you are looking for.

![owk](owk.jpg)

Built for ST4 on Windows and Linux (lightly tested).


# Commands

`sbot.py` is a sandard ST plugin with a variety of commands that process text, simplify ST internals,
interact with the OS, etc. Displays absolute text position in status bar next to row/col.

Supported menu type is <b>C</b>ontext, <b>S</b>idebar, <b>T</b>ab.

| Command                 | Menu | Description                                                    | Args                       |
| :--------               | :--- | :------------                                                  | :-------                   |
| sbot_split_view         | C S  | Toggle simple split view like VS, Word etc.                    |                            |
| sbot_copy_name          | S T  | Copy file/dir name to clipboard.                               | S: `"args": {"paths": []}` |
| sbot_copy_path          | S T  | Copy full file/dir path to clipboard.                          | S: `"args": {"paths": []}` |
| sbot_copy_file          | S T  | Copy selected file to a new file in the same directory.        | S: `"args": {"paths": []}` |
| sbot_delete_file        | C T  | Moves the file in current view to recycle/trash bin.           |                            |
| sbot_run                | C S  | Run a script file (py, lua, cmd, bat, sh) and show the output. |                            |
| sbot_click              | C S  | Open file (html, py, etc) as if you double clicked it.         | S: `"args": {"paths": []}` |
| sbot_terminal           | C S  | Open a terminal here.                                          | S: `"args": {"paths": []}` |
| sbot_tree               | C S  | Run tree cmd to new view.                                      | S: `"args": {"paths": []}` |
| sbot_open_context_path  | C    | Open path under cursor like `[tag](C:\my\file.txt)`            |                            |
| sbot_trim               | C    | Remove ws from Line ends.  | how: leading or trailing or both                               |
| sbot_remove_empty_lines | C    | Like it says.              | how: remove_all or normalize ( to one)                         |
| sbot_remove_ws          | C    | Like it says.              | how: remove_all or keep_eol or normalize (to one)              |
| sbot_insert_line_indexes| C    | not in clean?              |                                                                |


There are no default `Context/Tab/Side Bar.sublime-menu` files in this plugin.
Add the ones you like to your own `Context/Tab/Side Bar.sublime-menu` files. Typical entries are:
``` json
{ "caption": "Copy Name", "command": "sbot_copy_name"},
{ "caption": "Copy Path", "command": "sbot_copy_path"},
{ "caption": "Copy File", "command": "sbot_copy_file"},
{ "caption": "Delete File", "command": "sbot_delete_file" },
{ "caption": "Click File", "command": "sbot_click"},
{ "caption": "Split View 2 Pane", "command": "sbot_split_view" },
{ "caption": "Run", "command": "sbot_run" },
{ "caption": "Terminal Here", "command": "sbot_terminal" },
{ "caption": "Tree", "command": "sbot_tree" },
{ "caption": "Trim Leading WS", "command": "sbot_trim", "args" : {"how" : "leading"}  },
{ "caption": "Trim Trailing WS", "command": "sbot_trim", "args" : {"how" : "trailing"}  },
{ "caption": "Trim WS", "command": "sbot_trim", "args" : {"how" : "both"}  },
{ "caption": "Remove Empty Lines", "command": "sbot_remove_empty_lines", "args" : { "how" : "remove_all" } },
{ "caption": "Collapse Empty Lines", "command": "sbot_remove_empty_lines", "args" : { "how" : "normalize" } },
{ "caption": "Remove WS", "command": "sbot_remove_ws", "args" : { "how" : "remove_all" } },
{ "caption": "Remove WS Except EOL", "command": "sbot_remove_ws", "args" : { "how" : "keep_eol" } },
{ "caption": "Collapse WS", "command": "sbot_remove_ws", "args" : { "how" : "normalize" } },
{ "caption": "Insert Line Indexes", "command": "sbot_insert_line_indexes" },
```


# Utilities

`sbot_common.py` contain miscellaneous common components primarily for internal use by the sbot family.

This includes a very simple logger primarily for user-facing information, syntax errors and the
like. For debugging, `tracer.py` is more useful. It's also handy to add a command somewhere:

``` json
{ "caption": "Open Log", "command": "sbot_click", "args": { "paths": ["$APPDATA\\Sublime Text\\Packages\\User\\.SbotStore\\sbot.log"]} },
```

Note that the file in this repo is the master and is copied to other repos that use it upon update.
Submodules were considered but seemed more complex than a simple copy-op. Fight me.

# Settings

None.

Right click stuff works best with this global setting:
```
"preview_on_click": "only_left",
```

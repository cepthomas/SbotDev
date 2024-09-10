# Sublime Text Plugin Incubator and Playground

Just a big messy area. These are not the codes you are looking for.

![owk](owk.jpg)

Built for ST4 on Windows and Linux (lightly tested).


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

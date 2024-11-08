# Sublime Text Plugin Incubator and Playground

Just a big messy area. These are not the codes you are looking for.

![owk](owk.jpg)

Built for ST4 on Windows. Linux and OSX should be ok but are minimally tested.


- `sbot_common.py` contain miscellaneous common components primarily for internal use by the sbot family.
  This includes a very simple logger primarily for user-facing information, syntax errors and the
  like. For debugging, `tracer.py` is more useful. It's also handy to add a command somewhere:
``` json
{ "caption": "Open Log", "command": "sbot_click", "args": { "paths": ["$APPDATA\\Sublime Text\\Packages\\User\\.Dev\\Dev.log"]} },
```

- The `sbot_common.py` in this repo is the master and is copied to other repos that use it upon update.
  Submodules were considered but seemed more complex than a simple copy-op. Fight me.

- Right click stuff works best with this global setting:
```
"preview_on_click": "only_left",
```

- There is sparse but functional unit test code. Run from the cmd like with `go.cmd` or inside a
  Visual Studio project `VsTester.sln`.
  
- Really, python is a horrible mess. https://xkcd.com/1987.

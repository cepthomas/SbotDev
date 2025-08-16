# Sublime Text Plugin Incubator and Playground

Just a big messy area. These are not the codes you are looking for. ST4 on Windows.

![owk](owk.jpg)


- `sbot_common.py` contain miscellaneous common components primarily for internal use by the sbot family.
  This includes a very simple logger primarily for user-facing information, syntax errors and the like.
  The `sbot_common.py` and `emu_sublime_api.py` files in this repo are the masters which are copied to other repos as pertinent.
  Submodules were considered but seemed more complex than a simple copy-op. Fight me.

- Right click stuff works best with this global setting:
```
"preview_on_click": "only_left",
```
- [Really, python is a mess.](https://xkcd.com/1987)


# Using pbot_pdb to debug ST plugins

Most instructions in [PyBagOfTricks](https://github.com/cepthomas/PyBagOfTricks/blob/main/README.md).
apply here. The code under test is of course the plugin.

See 'sbot_dev.py' as example.

It's usually handy to add a command like this in one of the menus:
```json
{ "caption": "Run pdb", "command": "run_pdb" },
```

Note that ST is blocked while running the debugger so you can't edit files using it.
You may have to resort to *another editor!*.

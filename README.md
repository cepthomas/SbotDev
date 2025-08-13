# Sublime Text Plugin Incubator and Playground

Just a big messy area. These are not the codes you are looking for. ST4 on Windows.

![owk](owk.jpg)


- `sbot_common.py` contain miscellaneous common components primarily for internal use by the sbot family.
  This includes a very simple logger primarily for user-facing information, syntax errors and the like.
  The `sbot_common.py` in this repo is the master and is copied to other repos that use it upon update.
  Submodules were considered but seemed more complex than a simple copy-op. Fight me.

- Right click stuff works best with this global setting:
```
"preview_on_click": "only_left",
```

[Really, python is a mess.](https://xkcd.com/1987)


# Using pbot_pdb.py to debug ST plugins

Most instructions in [PyBagOfTricks](https://github.com/cepthomas/PyBagOfTricks/blob/main/README.md).
apply here. The code under test is of course the plugin.

It's usually handy to add a command like this in one of the menus:
```json
{ "caption": "Run pdb example", "command": "run_pdb" },
```
and a corresponding handler:
```python
class RunPdbCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        from . import pbot_pdb; pbot_pdb.breakpoint()
        my_plugin_code()
```

Note that ST is blocked while running the debugger so you can't edit files using it.
  You may have to resort to *another editor!*.

# Sublime Text plugin development playground. Nothing to see here, move along.

## General Notes

- In the code, `line` refers to editor lines and is 1-based. `row` refers to buffer contents as an array and is 0-based.
- Project collections, variables, functions, etc use:
    - `persisted` is the json compatible file format.
    - `visual` is the way ST API handles elements.
    - `internal` is the plugin format.
- Commands can't end with `<underscore numeral>` e.g. `my_cmd_1` should be `stpt_cmd1`.
- If you pass a dict as value in View.settings().set(name, value), it seems that the dict key must be a string.


## Event Handling
There are some idiosyncrasies with ST event generation.

- https://stackoverflow.com/questions/43125002/on-load-method-doesnt-work-as-expected
- https://github.com/sublimehq/sublime_text/issues/5

### ViewEventListener
Is instantiated once per view and:

- `on_load()` doesn't seem to work. Use EventListener instead.
- `on_load_project()` doesn't work on first start.
- `on_activated()` is normally called when the view gets focus but not when initially opened from single click.
- `on_close()` is normally called when a view is closed but it does not appear to be consistent. Perhaps if ST is closed
  without closing the views first?
- `on_deactivated()` is used in place of `on_close()` to save the persistence file every time the view loses focus. Good enough.

Why does it matter? Highlighting and signets persist their state per file and the application needs to hook the open/close
events in order to do so. Because the two obvious events don't work as expected (by me at least), some
less-than-beautiful hacks happen.


From the webs:
In views, find results fail until the focus is lost and regained. This is a bug in Sublime, so work around it by changing the focus.
```
window.focus_view(prev_view)
window.focus_view(view)
```

### EventListener
Is instantiated once per window (ST instance):

- `on_load()` is called when the file is loaded. Seems to work.
- `on_load_project()` doesn't fire on startup (last) project load.
- `on_exit()` called once after the API has shut down, immediately before the plugin_host process exits.
- `on_pre_close_window()` seems to work.

### Global
ST says `plugin_loaded()` fires only once for all instances of sublime. However you can add this to 
each module and they all get called. Safest is to only use it once.

## Module Loading
ST doesn't load modules like plain python and can cause some surprises. The problem is that sbot_common
gets reloaded but it appears to be a different module from the one linked to by the other modules.
This makes handling globals difficult. Modules that are common cannot store meaningful state.

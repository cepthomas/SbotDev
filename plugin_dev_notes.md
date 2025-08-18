# Tech Notes

Gleanings while building ST plugins.

https://github.com/cepthomas/example_plugin.git contains a lot of structural information.

## Error Handling

Because ST takes ownership of the python module loading and execution, it just dumps any load/parse and runtime exceptions
to the console. This can be annoying because it means you have to have the console open pretty much all the time.
First attempt was to hook the console stdout but it was not very cooperative. So now there are try/except around all the
ST callback functions and this works to catch runtime errors and pop up a message box. Import/parse errors still go to the
console so you have to keep an eye open there while developing but they should resolve quickly.

## Exceptions

These are the categories of exceptions in the Sublime python implementation:
- User-handled with the standard `try/except` mechanism.
- Plugin command syntax and functional errors are intercepted and logged by a custom `sys.excepthook` in `sbot_logger.py`.
- Errors in scripts that are executed by sublime internals e.g. `load_module()` are not caught by the above hook but go straight
  to stdout. It *works* but is not as tightly integrated as preferred.

## General Notes

- In the code, `line` refers to editor lines and is 1-based. `row` refers to buffer contents as an array and is 0-based.
- Project collections, variables, functions, etc use:
    - `persisted` is the json compatible file format.
    - `visual` is the way ST API handles elements.
    - `internal` is the plugin format.
- If you pass a dict as value in View.settings().set(name, value), it seems that the dict key must be a string.
- In views, find results fail until the focus is lost and regained. This is a bug in Sublime, so work around it by changing the focus.
'''
window.focus_view(prev_view)
window.focus_view(view)
'''

## Commands
If you are going to interact with the current view, use TextCommand, otherwise use WindowCommand.
Unknown usage for ApplicationCommand.
WindowCommand is instantiated once per window (all views). Use for commands sited in main and sidebar menus.
TextCommand is instantiated once per view. Use for commands sited in context (view) menus.
- Commands can't end with `<underscore numeral>` e.g. `my_cmd_1` should be `stpt_cmd1`.


## Events
There are some idiosyncrasies with ST event generation.

- https://stackoverflow.com/questions/43125002/on-load-method-doesnt-work-as-expected
- https://github.com/sublimehq/sublime_text/issues/5

ST says `plugin_loaded()` fires only once for all instances of sublime. However you can add this to 
each module and they all get called. Safest is to only use it once.


### ViewEventListener
A class that provides similar event handling to EventListener, but bound
to a specific view. Provides class method-based filtering to control what views objects are created for.

Is instantiated once per view and:
- `on_load()` is normally called when the file is loaded. However it is not called if ST startup shows previously opened files,
  or if it is shown as a (single-click) preview.
- `on_close()` is normally called when a view is closed but it does not appear to be consistent. Perhaps if ST is closed
  without closing the views first?

Why does it matter? Highlighting and signets persist their state per file and the application needs to hook the open/close
events in order to do so. Because the two obvious events don't work as expected (by me at least), some
less-than-beautiful hacks happen:
- `on_activated()` is normally called when the view gets focus. This is reliable so is used instead of on_load(), along with
  some stuff to track if it's been initialized.
- `on_deactivated()` is used in place of `on_close()` to save the persistence file every time the view loses focus. Good enough.

So, in general use EventListener instead. https://stackoverflow.com/a/50226141.

### EventListener
Is instantiated once per window (ST instance):
- `on_load_project()` doesn't fire on startup (last) project load.
- `on_exit()` called once after the API has shut down, immediately before the plugin_host process exits.
- `on_pre_close_window()` seems to work.

Note that many of these events are triggered by the buffer underlying the view,
and thus the method is only called once, with the first view as the parameter.

## Module Loading
ST doesn't load modules like plain python and can cause some surprises. One problem is that sbot_common
gets reloaded per module but it is a different object from the ones imported by the other modules.
This makes handling globals difficult - modules that are common cannot store meaningful state.


Actual complete sequence:
```text
# UI: Open default/empty file.
EventListener.on_init ([View(12)],)
# UI: Open real file with sigs.
  # First close current or default.
EventListener.on_pre_close (View(12),) # Window is valid!
EventListener.on_close (View(12),)
  # Then open new.
EventListener.on_load (View(15),)
# UI: Close real file.
EventListener.on_pre_close (View(15),)
EventListener.on_close (View(15),)
# UI: Shutdown.
EventListener.on_pre_close_project (Window(2),)
EventListener.on_pre_close_project (Window(2),)
EventListener.on_pre_close (View(16),) # Window is not valid!
EventListener.on_close (View(16),)
```

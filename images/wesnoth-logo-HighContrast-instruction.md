At least KDE does not support the draft-oder option in svgs. As a result the stroke is applied to the filled part as well, which looks very bad.
To create a usable file:
- select the outer objects (both swords and outer shield) and unite them into a single object.
- use a stroke-width >=6, adjust other stroke settings freely. The objects can also have different stroke settings if they are united after being transfomed to a path rather than before.
- transform them to a path [e.g. in inkscape's menubar: path -> stroke to path. Note: not object to path]

This new object can then be used as background/frame in the final file instead of a stroke. Thatfor, copy it to the final file and make sure that it's before the other objects listed in the (xml) file.
Final file can be found at wesnoth/packaging/icons/HighContrast/scalable/apps/wesnoth-icon.svg

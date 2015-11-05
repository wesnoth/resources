This is a "source package" for the Wesnoth logo and contains the files needed for rendering the logo (image and text together or separately) in different resolutions.

The package contains the following files:

Weslogo.svg
	The SVG file for the logo image (shield and swords).
Weslogo-text.svg
	The SVG file for the text, containing the different language versions.
render.py
	A Python script for rendering the images. A selection of language versions can be rendered with one command. 
LiberationSerif-Regular.ttf
	A font file containing the Devanagari font (Liberation Serif) used for the Marathi language version.
KeterYG-Medium.ttf
	A font file for the Hebrew font (Keter YG) used for the Hebrew language version.
OldaniaADFStd-Regular.otf
        A font file for the latin font (Oldania).
README.TXT
	This file.


Rendering
---------

Rendering can be done directly from Inkscape or by the render.py script. The script works with both Python versions 2.7 and 3.x. Inkscape must be installed on the system as the script uses it for backend. Both Inkscape versions .48 and .91 should work, but the latter is faster. The font files don't need to be installed for rendering.

Run::

	python render.py --help

for the usage.


Adding new translations
-----------------------

New languages versions can be added to ``Weslogo-text.svg``. Open it in Inkscape. Copy the layer ``Template`` and rename it so that the first part of the name is the language code of the new translation. After a space you should put the name of the language in english (for example, the name for the English version layer is ``en english``). If the same translation is usable for more than one language, the language code used should be the one first alphabetically. Include the other languages codes and names in the layer name in parenthesis. The rendering script will depend on this naming convention for finding the different versions.

If the new translation uses latin alphabet, you should have the font file ``OldaniaADFStd-Regular.otf`` installed on your system. Font files for Devanagari and Hebrew fonts are also included, install these if your translation uses these alphabets. With other alphabets you should decide the font yourself, but it should be released under a license which permits commercial use and redistribution of the font files (such as GPL or Open Font License). 

Your new layer will contain the text ``The Text Here``. Replace it with your own text. The text should be centered and visually balanced and usually some tweaking with kerning and possibly some scaling is needed. There is a layer ``Shield`` which contains a bitmap of the logo image, making this visible may help with designing the layout. The upper line should only contain a preceding article (or other similar construct) and the main part of the text should go to the lower line. The article may also be placed on the same line with the rest of the text if this works better with the layout. See the existing versions to get a feel for the design principles.

When the layout is ready, you should change the text into a sigle path, with no outline and solid black fill.


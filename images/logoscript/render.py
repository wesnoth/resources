import subprocess, tempfile, argparse, shutil, sys
from PIL import Image
import xml.etree.ElementTree as ET
from os import path

parser = argparse.ArgumentParser(
description = """'render.py' is a convenience script for rendering the Wesnoth logo indesired resolution and language versions.""")

parser.add_argument('-i', '--icon', action="store_true", help='Render the shield and swords icon.')
parser.add_argument('-t', '--text', action="store_true", help='Render the text.')
parser.add_argument('-H', '--height', type=int, default=200,
                    help='Image height in pixels. The width will be the same for the icon '
                         'and 3 x height for the text vesrions. The largest practica value '
                         'is 960, if you want bigger resolution, you shoud render directly '
                         'from Inkscape. Default is 200.')
parser.add_argument('-l', '--language-list', 
                    help='List the language codes in comma-separated list (no spaces). If '
                         'omitted, all language versions will be rendered.')
parser.add_argument('-o', '--output-dir', 
                    help='Directory, where the output will be saved. It must already exist. '
                         'Default is the current working directory.')
parser.add_argument('--list-languages', action="store_true",
                    help='Output a list of language versions available (language code: '
                         'language name). When this option is used, nothing else will be done.')
parser.add_argument('-v', '--verbose', action="store_true",
                    help='Include Inkscape messages in the output. This may be useful if something '
                         'goes wrong.')

args = parser.parse_args()

outdir = path.abspath('')
if args.output_dir:
    if not path.isdir(args.output_dir):
        sys.exit("Error: '" + path.abspath(args.output_dir) + "' is not a valid directory.")
    else:
        outdir = path.abspath(args.output_dir)

with open('Weslogo-text.svg') as source:
    tempsource = source.read().replace('display:none;','')
root = ET.fromstring(tempsource)
langlist, listlang = {}, {}

for i in root.iter('{http://www.w3.org/2000/svg}g'):
    try:
        content = i.attrib['{http://www.inkscape.org/namespaces/inkscape}label'].split(' ')
        langlist[content[0]] = i.attrib['id']
        listlang[content[0]] = ' '.join(content[1:])
    except:
        pass

del(langlist['Template'], langlist['Shield'], listlang['Template'], listlang['Shield'])

if args.list_languages:
    sys.exit('\n'.join([': '.join([i, listlang[i]]) for i in sorted(listlang.keys())]))

if args.language_list:
    llist = {}
    for i in args.language_list.split(','):
        try:
            llist[i] = langlist[i]
        except(KeyError):
            sys.exit("Error: Unknown language code: " + i)
    langlist = llist

if args.verbose:
    inkout = None
    enl = '\n---\n'
else:
    inkout = subprocess.PIPE
    enl = ''

try:
    tempdir = tempfile.mkdtemp()
    with open(path.join(tempdir, 'logotemp.svg'),'w') as temp:
        temp.write(tempsource)
    if args.icon:
        print('Rendering: Icon' + enl)
        subprocess.Popen(['inkscape', '--shell'], stdin=subprocess.PIPE, stdout=inkout, stderr=inkout, universal_newlines=True)\
        .communicate('-f Weslogo.svg -a -1920:0:3840:1920 -e ' + path.join(tempdir, 'weslogo-temp.png') + '\n')
        image_icon = Image.open(path.join(tempdir, 'weslogo-temp.png'))
        print(enl + 'Resizing: Icon')
        image_icon.crop((1920, 0, 3840, 1920))\
        .resize((args.height, args.height), Image.ANTIALIAS)\
        .save(path.join(outdir, 'weslogo-icon.png'))
        print('Saved: ' + path.join(outdir, 'weslogo-icon.png'))
    if args.text:
        for c in sorted(langlist.keys()):
            i = langlist[c]
            print('Rendering: ' + c + enl)
            subprocess.Popen(['inkscape', '--shell'],
                             stdin=subprocess.PIPE, stdout=inkout, stderr=inkout, universal_newlines=True)\
            .communicate('-f ' + path.join(tempdir,'logotemp.svg') + ' -C -j -i ' + i + ' -l ' + 
                         path.join(tempdir, 'weslogo-temp.svg') + '\n')
            subprocess.Popen(['inkscape', '--shell'],
                             stdin=subprocess.PIPE, stdout=inkout, stderr=inkout, universal_newlines=True)\
            .communicate('-f ' + path.join(tempdir,'weslogo-temp.svg') + ' -C -e ' + 
                         path.join(tempdir, 'weslogo-temp.png') + '\n')
            print(enl + 'Resizing: ' + c)
            image = Image.open(path.join(tempdir, 'weslogo-temp.png')).crop((576,192,6336,2112))
            if args.icon:
                mask = image.copy()
                image.putalpha(255)
                image = Image.composite(image, image_icon, mask)
            image.resize((3 * args.height, args.height), Image.ANTIALIAS)\
            .save(path.join(outdir, ('weslogo-' + c + '.png')))
            print('Saved: ' + path.join(outdir, ('weslogo-' + c + '.png')))
except:
    sys.excepthook(*sys.exc_info())
finally:
    shutil.rmtree(tempdir)


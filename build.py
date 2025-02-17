# GyverHub Web Builder
# pip install rcssmin
# pip install rjsmin

version = '0.51.4b'
notes = 'New version!'
# remove_non_gz = False
remove_non_gz = True

js_hub = [
    "src/inc/lib/hub/mqtt.min.js",
    "src/inc/lib/hub/bt.js",
    "src/inc/lib/hub/serial.js",
    "src/inc/lib/hub/utils.js",
    "src/inc/lib/hub/buffer.js",
    "src/inc/lib/hub/discover.js",
    "src/inc/lib/hub/conn_bt.js",
    "src/inc/lib/hub/conn_http.js",
    "src/inc/lib/hub/conn_mqtt.js",
    "src/inc/lib/hub/conn_serial.js",
    "src/inc/lib/hub/conn_ws.js",
    "src/inc/lib/hub/device.js",
    "src/inc/lib/hub/GyverHub.js",
]

js_files = [
    "src/inc/lib/qrcode.min.js",
    "src/inc/lib/sort-paths.min.js",
    "src/inc/lib/pickr.min.js",
    "src/inc/lib/joy.js",
    "src/inc/data.js",
    "src/inc/widgets.js",
    "src/inc/controls.js",
    "src/inc/render.js",
    "src/inc/config.js",
    "src/inc/projects.js",
    "src/inc/ui.js",
    "src/inc/fs.js",
    "src/inc/index.js",
    "src/inc/updates.js",
    "src/inc/events.js",
    "src/inc/test.js",
]

css_files = [
    'src/inc/lib/nano.min.css',
    'src/inc/style/main.css',
    'src/inc/style/ui.css',
    'src/inc/style/widgets.css',
]

sw_cache = '''
  '/',
  '/fa-solid-900.woff2',
  '/PTSans-Narrow.woff2',
  '/favicon.svg',
  '/index.html',
  '/script.js',
  '/style.css',
'''

copy_web = [
    'favicon.svg',
    'index.html',
    'manifest.json',
    'sw.js',
    'icons/icon-192x192.png',
    'icons/icon-256x256.png',
    'icons/icon-384x384.png',
    'icons/icon-512x512.png',
]

inc_min = '''
  <script src="script.js?__VER__="></script>
  <link href="style.css?__VER__=" rel="stylesheet">
'''

##############################################################

from rcssmin import cssmin
from rjsmin import jsmin
import gzip
import shutil
import os
import re
import base64

##############################################################

if os.path.exists('app'): shutil.rmtree('app')
if os.path.exists('esp'): shutil.rmtree('esp')
if os.path.exists('esp_h'): shutil.rmtree('esp_h')
if os.path.exists('host'): shutil.rmtree('host')
if os.path.exists('local'): shutil.rmtree('local')
if os.path.exists('lib'): shutil.rmtree('lib')

os.mkdir('app')
os.mkdir('esp')
os.mkdir('esp_h')
os.mkdir('host')
os.mkdir('host/icons')
os.mkdir('host/fonts')
os.mkdir('local')
os.mkdir('lib')

with open('version.txt', "w") as f:
    f.write(version)

###############################################################
###                          HUBJS                          ###
###############################################################
js_min = ''
for file in js_hub:
    with open(file, 'r') as f:
        read = f.read()
        if ('.min.' not in file): read = jsmin(read)
        js_min += read + '\n'

js_min = re.sub(r'(^\s+)', '' , js_min, flags=re.MULTILINE)

with open('lib/GyverHub.min.js', 'w') as f:
    f.write(js_min)

###############################################################
###                           HOST                          ###
###############################################################

metrika = '''
  <script type="text/javascript">
    (function (m, e, t, r, i, k, a) {
        m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments) };
        m[i].l = 1 * new Date();
        for (var j = 0; j < document.scripts.length; j++) { if (document.scripts[j].src === r) { return; } }
        k = e.createElement(t), a = e.getElementsByTagName(t)[0], k.async = 1, k.src = r, a.parentNode.insertBefore(k, a)
    })
        (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
    ym(93507215, "init", {clickmap: true, trackLinks: true, accurateTrackBounce: true});
  </script>
  <noscript>
    <div><img src="https://mc.yandex.ru/watch/93507215" style="position:absolute; left:-9999px;" alt="" /></div>
  </noscript>
'''

shutil.copyfile('src/inc/style/fonts/fa-solid-900.woff2', 'host/fonts/fa-solid-900.woff2')
shutil.copyfile('src/inc/style/fonts/PTSans-Narrow.woff2', 'host/fonts/PTSans-Narrow.woff2')

for file in copy_web:
    shutil.copyfile('src/' + file, 'host/' + file)

with open('host/index.html', "r+") as f:
    data = f.read()
    data = re.sub(r'<!--INC-->([\s\S]*?)<!--\/INC-->', inc_min, data)
    data = re.sub(r'<!--METRIKA-->', metrika, data)
    data = re.sub(r'__VER__', version, data)
    data = re.sub(r'<!--([\s\S]*?)-->', '', data)
    data = re.sub(r'<!--\/([\s\S]*?)-->', '', data)
    data = "".join([s for s in data.strip().splitlines(True) if s.strip()])
    f.seek(0)
    f.write(data)
    f.truncate()

with open('host/sw.js', "r+") as f:
    data = f.read()
    data = re.sub(r'__VER__', version, data)
    data = re.sub(r'\'__CACHE__\'', sw_cache, data)
    f.seek(0)
    f.write(data)
    f.truncate()

# JS
js_min = ''
with open('lib/GyverHub.min.js', 'r') as f:
    js_min = f.read()

for file in js_files:
    with open(file, 'r') as f:
        read = f.read()
        if ('.min.' not in file): read = jsmin(read)
        js_min += read + '\n'

js_min = js_min.replace('__VER__', version)
js_min = js_min.replace('__NOTES__', notes)
js_min = re.sub(r'(^\s+)', '' , js_min, flags=re.MULTILINE)

with open('host/script.js', 'w') as f:
    f.write(js_min)

# CSS
css_min = ''
for file in css_files:
    with open(file, 'r') as f:
        read = f.read()
        if ('.min.' not in file): read = cssmin(read)
        css_min += read + '\n'

with open('host/style.css', 'w') as f:
    f.write(css_min)

#################################################################
###                           LOCAL                           ###
#################################################################
fa_b64 = 'data:font/woff2;charset=utf-8;base64,'
with open("src/inc/style/fonts/fa-solid-900.woff2", "rb") as f:
    fa_b64 += (base64.b64encode(f.read())).decode('ascii')

pt_b64 = 'data:font/woff2;charset=utf-8;base64,'
with open("src/inc/style/fonts/PTSans-Narrow.woff2", "rb") as f:
    pt_b64 += (base64.b64encode(f.read())).decode('ascii')

css_min_l = css_min
css_min_l = css_min_l.replace('url(fonts/fa-solid-900.woff2)', 'url(' + fa_b64 + ')')
css_min_l = css_min_l.replace('url(fonts/PTSans-Narrow.woff2)', 'url(' + pt_b64 + ')')

icon_b64 = "<link rel='icon' href='data:image/svg+xml;base64,"
with open("src/favicon.svg", "rb") as f:
    icon_b64 += (base64.b64encode(f.read())).decode('ascii') + "'>"

shutil.copyfile('src/index.html', 'local/GyverHub.html')

inc_local = '<style>\n' + css_min_l + '\n</style>\n'
inc_local += '<script>\n' + js_min + '\n</script>\n'

with open('local/GyverHub.html', "r+") as f:
    data = f.read()
    data = re.sub(r'<!--INC-->([\s\S]*?)<!--\/INC-->', '__INC__', data)
    data = data.replace('__INC__', inc_local)
    data = re.sub(r'<!--ICON-->([\s\S]*?)<!--\/ICON-->', icon_b64, data)
    data = re.sub(r'<!--PWA-->([\s\S]*?)<!--\/PWA-->', '', data)
    data = re.sub(r'<!--METRIKA-->', '', data)
    data = re.sub(r'__VER__', version, data)
    data = re.sub(r'<!--([\s\S]*?)-->', '', data)
    data = re.sub(r'<!--\/([\s\S]*?)-->', '', data)
    data = "".join([s for s in data.strip().splitlines(True) if s.strip()])
    f.seek(0)
    f.write(data)
    f.truncate()

###############################################################
###                           APP                           ###
###############################################################
shutil.copyfile('src/index.html', 'app/index.html')
inc_app = inc_local.replace('__APP__', '')

with open('app/index.html', "r+") as f:
    data = f.read()
    data = re.sub(r'<!--INC-->([\s\S]*?)<!--\/INC-->', '__INC__', data)
    data = data.replace('__INC__', inc_app)
    data = re.sub(r'<!--ICON-->([\s\S]*?)<!--\/ICON-->', '', data)
    data = re.sub(r'<!--PWA-->([\s\S]*?)<!--\/PWA-->', '', data)
    data = re.sub(r'<!--APP-->([\s\S]*?)<!--\/APP-->', '', data)
    data = re.sub(r'<!--METRIKA-->', '', data)
    data = re.sub(r'__VER__', version, data)
    data = re.sub(r'<!--([\s\S]*?)-->', '', data)
    data = re.sub(r'<!--\/([\s\S]*?)-->', '', data)
    data = "".join([s for s in data.strip().splitlines(True) if s.strip()])
    f.seek(0)
    f.write(data)
    f.truncate()

# with open('app/index.html', 'rb') as f_in, gzip.open('app/index.html.gz', 'wb') as f_out: f_out.writelines(f_in)
# if (remove_non_gz): os.remove("app/index.html")

###############################################################
###                           ESP                           ###
###############################################################
# JS
js_min = ''
for file in js_hub:
    with open(file, 'r') as f:
        read = f.read()
        read = re.sub(r'\/\*NON-ESP\*\/([\s\S]*?)\/\*\/NON-ESP\*\/', '', read)
        read = jsmin(read)
        js_min += read + '\n'

js_min = re.sub(r'(^\s+)', '' , js_min, flags=re.MULTILINE) # hub min js

for file in js_files:
    with open(file, 'r') as f:
        read = f.read()
        read = re.sub(r'\/\*NON-ESP\*\/([\s\S]*?)\/\*\/NON-ESP\*\/', '', read)
        read = re.sub(r'<!--NON-ESP-->([\s\S]*?)<!--\/NON-ESP-->', '', read)
        if ('.min.' not in file): read = jsmin(read)
        js_min += read + '\n'

js_min = js_min.replace('__VER__', version)
js_min = js_min.replace('__NOTES__', notes)
js_min = js_min.replace('__ESP__', '')
js_min = re.sub(r'(^\s+)', '' , js_min, flags=re.MULTILINE)

with open('esp/script.js', 'w') as f: f.write(js_min)
with open('esp/script.js', 'rb') as f_in, gzip.open('esp/script.js.gz', 'wb') as f_out: f_out.writelines(f_in)

# CSS
fa_min_b64 = 'data:font/woff2;charset=utf-8;base64,'
with open("src/inc/style/fonts/fa-solid-900.min.woff2", "rb") as f:
    fa_min_b64 += (base64.b64encode(f.read())).decode('ascii')

css_min = ''
for file in css_files:
    with open(file, 'r') as f:
        read = f.read()
        read = re.sub(r'\/\*NON-ESP\*\/([\s\S]*?)\/\*\/NON-ESP\*\/', '', read)
        read = read.replace('url(fonts/fa-solid-900.woff2)', 'url(' + fa_min_b64 + ')')
        if ('.min.' not in file): read = cssmin(read)
        css_min += read + '\n'

with open('esp/style.css', 'w') as f: f.write(css_min)
with open('esp/style.css', 'rb') as f_in, gzip.open('esp/style.css.gz', 'wb') as f_out: f_out.writelines(f_in)

# INDEX
shutil.copyfile('src/index.html', 'esp/index.html')
with open('esp/index.html', "r+") as f:
    data = f.read()
    data = re.sub(r'<!--ICON-->([\s\S]*?)<!--\/ICON-->', '', data)
    data = re.sub(r'<!--INC-->([\s\S]*?)<!--\/INC-->', inc_min, data)
    data = re.sub(r'<!--PWA-->([\s\S]*?)<!--\/PWA-->', '', data)
    data = re.sub(r'<!--METRIKA-->', '', data)
    data = re.sub(r'__VER__', version, data)
    data = re.sub(r'<!--([\s\S]*?)-->', '', data)
    data = re.sub(r'<!--\/([\s\S]*?)-->', '', data)
    data = "".join([s for s in data.strip().splitlines(True) if s.strip()])
    f.seek(0)
    f.write(data)
    f.truncate()

with open('esp/index.html', 'rb') as f_in, gzip.open('esp/index.html.gz', 'wb') as f_out: f_out.writelines(f_in)

if (remove_non_gz): os.remove("esp/script.js")
if (remove_non_gz): os.remove("esp/style.css")
if (remove_non_gz): os.remove("esp/index.html")

###############################################################
###                         ESP INC                         ###
###############################################################

def file_to_h(src, dest, name):
    with open(src, "rb") as f:
        bytes = bytearray(f.read())
        data = '#pragma once\n'
        data += '#define ' + name + '_len ' + str(len(bytes)) + '\n\n'
        data += 'const uint8_t ' + name + '[] PROGMEM = {\n\t'
        count = 0
        for b in bytes:
            data += "0x{:02x}".format(b) + ', '
            count += 1
            if (count % 16 == 0): data += '\n\t'

        data += '\n};'
        with open(dest, "w") as f: f.write(data)

file_to_h('esp/index.html.gz', 'esp_h/index.h', 'hub_index_h')
file_to_h('esp/style.css.gz', 'esp_h/style.h', 'hub_style_h')
file_to_h('esp/script.js.gz', 'esp_h/script.h', 'hub_script_h')
import mechanize
import http.cookiejar as cookielib
import re
import sys

# Fungsi untuk mencetak teks berwarna di terminal
def cetak(x, e=0):
    w = 'mhkbpcP'
    for i in w:
        j = w.index(i)
        x = x.replace('!%s' % i, '\033[%s;1m' % str(31 + j))
    x += '\033[0m'
    x = x.replace('!0', '\033[0m')
    if e != 0:
        sys.stdout.write(x)
    else:
        sys.stdout.write(x + '\n')

# Setup mechanize browser
def install_browser():
    global br
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_handle_equiv(True)
    br.set_handle_referer(True)
    br.set_cookiejar(cookielib.LWPCookieJar())
    br.set_handle_redirect(True)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')]

# Fungsi untuk membuka URL
def buka(d):
    try:
        x = br.open(d)
        br._factory.is_html = True
        x = x.read()
    except:
        cetak('\r!m[!] Gagal membuka !p' + str(d))
        sys.exit()
    if '<link rel="redirect" href="' in x.decode('utf-8'):
        return buka(br.find_link().url)
    else:
        return x.decode('utf-8')

# Fungsi untuk login ke Facebook
def login():
    global log
    us = input('Email/HP: ')
    pa = input('Kata Sandi: ')
    cetak('!h[*] Sedang Login....')
    buka('https://m.facebook.com')
    
    # Pilih form yang benar
    br.select_form(nr=0)
    
    # Debugging: Cetak semua kontrol form
    hidden_controls = {}
    for control in br.form.controls:
        print(f"Control name: {control.name}")
        if control.type == "hidden":
            hidden_controls[control.name] = control.value
    
    # Isi kontrol form
    try:
        br.form['email'] = us  # Nama kontrol untuk email
    except mechanize._form_controls.ControlNotFoundError:
        cetak("Kontrol 'email' tidak ditemukan. Silakan periksa struktur form.")
        sys.exit()
    
    try:
        br.form['pass'] = pa  # Nama kontrol untuk password
    except mechanize._form_controls.ControlNotFoundError:
        cetak("Kontrol 'pass' tidak ditemukan. Silakan periksa struktur form.")
        sys.exit()
    
    # Tambahkan nilai kontrol tersembunyi ke dalam form
    for name, value in hidden_controls.items():
        try:
            br.form[name] = value
        except AttributeError:
            print(f"Skipping read-only control '{name}'")

    # Debugging: Cetak semua kontrol dan nilainya setelah pengisian
    for control in br.form.controls:
        print(f"Control name: {control.name}, value: {control.value}")
    
    # Submit form dan cek URL
    response = br.submit()
    url = br.geturl()
    if 'save-device' in url or 'm_sess' in url:
        buka('https://mobile.facebook.com/home.php')
        nama = br.find_link(url_regex='logout.php').text
        nama = re.findall(r'\((.*a?)\)', nama)[0]
        cetak('!h[*] Selamat datang !k%s' % nama)
        cetak('!h[*] Semoga ini adalah hari keberuntungan mu...')
        log = 1
    elif 'checkpoint' in url:
        cetak('!m[!] Akun kena checkpoint\n!k[!]Coba Login dengan opera mini')
        sys.exit()
    else:
        cetak('!m[!] Login Gagal')

# Jalankan fungsi-fungsi
install_browser()
login()

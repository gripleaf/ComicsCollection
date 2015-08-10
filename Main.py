__author__ = 'glcsnz123'
# _*_ coding: utf-8 _*_
import re
import urllib, urllib2
import os
from Globals import Settings, MyDeamon
import logging

import sys

_patten = re.compile("""<img id="main-comic" src=['"].+['"]""")


def img_download(url, path):
    urllib.urlretrieve(url, path)


def get_url_from_key(key):
    return key.split(" ")[-1][5:-1]


def _read_count_no():
    cnt_no = open("cnt").readline()
    return int(cnt_no)


def _write_count_no(cnt_no):
    f = open("cnt", 'w')
    f.write(str(cnt_no))
    f.close()


def get_url(url="http://explosm.net/comics/1001/"):
    try:
        req = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        logging.warning("".join(["\t[HTTP ERROR] ", e.msg]))
        return ""
    logging.info("\treading web page...")
    while True:
        html = req.readline()
        ant = _patten.findall(html)
        if len(ant) > 0:
            return "http:" + get_url_from_key(ant[0])
    return ""


def main_task():
    comics_path = "comics"
    start_no = _read_count_no()
    for i in range(start_no, 10000):
        try:
            logging.info("downloading comics [%d]" % i)
            _write_count_no(i)
            img_url = get_url("http://explosm.net/comics/%d/" % i)
            if img_url == '':
                logging.info("\tpage [%d] is not exits\n" % i)
                continue
            file_path = os.path.join(comics_path, ".".join([str(i), img_url.split('.')[-1]]))
            logging.info("".join(["\t downloading ", img_url.split('/')[-1], " --> ", file_path]))
            img_download(img_url, file_path)
        except Exception, e:
            logging.warning("".join(["[PRCS ERROR]", e.message]))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.info("***********FRONT***********")
        main_task()
    else:
        logging.info("***********BACK***********")
        if sys.argv[1].upper() == "START":
            MyDeamon.daemonize("", main_task)

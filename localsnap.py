#!python3
# localsnap.py - Offline Snap! runner and manager
# Written by Matthew and released under the MIT license (see LICENSE.txt)
from __future__ import print_function

import requests
import argparse, os, zipfile, pickle
import io, shutil, webbrowser
try:
    # Python3
    from http.server import *
except ImportError:
    # Python2
    from SocketServer import TCPServer as HTTPServer
    from SimpleHTTPServer import *


version, __version__ = ("1.0.0",) * 2

def script_dir():
    "Returns the directory of the script's home dir"
    return os.path.dirname(os.path.realpath(__file__))

DOWNLOAD_FOLDER = os.path.join(script_dir(), "snapdownload")
FOLDER_PATT = "Snap--Build-Your-Own-Blocks-%s"

def get_latest_url():
    r = requests.get("https://github.com/jmoenig/Snap--Build-Your-Own-Blocks/releases/latest")
    r.raise_for_status()
    return r.url

def get_version_from_url(url):
    return url.split("/")[-1]

def get_snap_zip(version):
    url = "https://github.com/jmoenig/Snap--Build-Your-Own-Blocks/archive/%s.zip" % version
    r = requests.get(url)
    r.raise_for_status()
    z = io.BytesIO(r.content)
    return zipfile.ZipFile(z)

def clear_download_folder():
    if os.path.exists(DOWNLOAD_FOLDER):
        shutil.rmtree(DOWNLOAD_FOLDER)
    os.mkdir(DOWNLOAD_FOLDER)

def load_meta():
    return pickle.load(open(os.path.join(DOWNLOAD_FOLDER, "meta.pickle"), "rb"))

def dump_meta(meta):
    pickle.dump(meta, open(os.path.join(DOWNLOAD_FOLDER, "meta.pickle"), "wb"), 2)

def download_snap():
    url = get_latest_url()
    version = get_version_from_url(url)
    clear_download_folder()
    dump_meta({"version": version})
    snapzip = get_snap_zip(version)
    snapzip.extractall(DOWNLOAD_FOLDER)

def create_argparser():
    parser = argparse.ArgumentParser(prog="localsnap",
                                     description='Offline Snap! runner and manager')
    parser.add_argument("-w", "--web",
                action="store_true",
                help="Open up the online version of Snap! in a web browser.")
    parser.add_argument("-u", "--update",
                action="store_true",
                help="Update to the latest Snap! release.")
    parser.add_argument("-f", "--force",
                action="store_true",
                help="Force --update to redownload Snap!, even if you already have the latest version.")
    parser.add_argument("-p", "--port",
                default=8000,
                type=int,
                help="Specifies the port the webserver uses to serve the local Snap! copy (default is 8000)")
    parser.add_argument("-V", "--version",
                action="version",
                version="localsnap %s, Snap! %s" % (version, load_meta()["version"]),
                help="Display the version of localsnap and the downloaded Snap!")
    return parser

def serve_snap(port):
    os.chdir(os.path.join(DOWNLOAD_FOLDER, FOLDER_PATT % load_meta()["version"]))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

def main():
    if not os.path.exists(DOWNLOAD_FOLDER):
        print("Downloading Snap!...")
        download_snap()
    meta = load_meta()
    parser = create_argparser()
    args = parser.parse_args()
    if args.web:
        print("Opening http://snap.berkeley.edu/")
        webbrowser.open("http://snap.berkeley.edu/")
    elif args.update:
        print("Checking for update...")
        new_version = get_version_from_url(get_latest_url())
        print("Latest version is", new_version)
        if args.force or new_version > meta["version"]:
            print("Updating from %s to %s" % (meta["version"], new_version))
            download_snap()
        else:
            print("You already have the latest version!")
    else:
        print("Serving local Snap! on port %s" % args.port)
        webbrowser.open("http://localhost:%s" % args.port)
        serve_snap(args.port)

if __name__ == '__main__':
    main()

#!/usr/bin/python3
import os
from datetime import datetime
from fabric.api import *


env.hosts = ["100.25.146.136", "54.237.38.206"]
env.user = "ubuntu"


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    try:
        if not os.path.exists("versions"):
            local("mkdir versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        path = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(path))
        return path
    except Exception:
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        file = archive_path.split("/")[-1]
        folder = "/data/web_static/releases/" + file.split(".")[0]
        run("mkdir {}".format(folder))
        run("tar -xzf /tmp/{} -C {}".format(file, folder))
        run("rm /tmp/{}".format(file))
        run("mv {}/web_static/* {}/".format(folder, folder))
        run("rm -rf {}/web_static".format(folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder))
        return True
    except Exception:
        return False

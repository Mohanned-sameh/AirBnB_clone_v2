#!/usr/bin/python3
from fabric.api import env, put, run, local
from datetime import datetime
import os

env.hosts = ["100.25.146.136", "54.237.38.206"]
env.user = "ubuntu"


def do_pack():
    """Function to compress files"""
    try:
        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file))
        return file
    except BaseException:
        return None


def do_deploy(archive_path):
    """Function to deploy"""
    if not os.path.exists(archive_path):
        return False
    try:
        file = archive_path.split("/")[-1]
        new_folder = "/data/web_static/releases/" + file.split(".")[0]
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(new_folder))
        run("tar -xzf /tmp/{} -C {}".format(file, new_folder))
        run("rm /tmp/{}".format(file))
        run("mv {}/web_static/* {}/".format(new_folder, new_folder))
        run("rm -rf {}/web_static".format(new_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(new_folder))
        return True
    except BaseException:
        return False

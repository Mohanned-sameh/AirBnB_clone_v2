#!/usr/bin/python3
from fabric.api import env, put, run, local
from datetime import datetime
import os

env.hosts = ["100.25.146.136", "54.237.38.206"]


def do_pack():
    """Function to compress files"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static".format(date))
        return "versions/web_static_{}.tgz".format(date)
    except BaseException:
        return None


def do_deploy(archive_path):
    """Function to deploy"""
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        name = archive_path.split("/")[1].split(".")[0]
        run("mkdir -p /data/web_static/releases/{}/".format(name))
        run(
            "tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/".format(
                name,
                name,
            )
        )
        run("rm /tmp/{}.tgz".format(name))
        run(
            "mv /data/web_static/releases/{}/web_static/*\
            /data/web_static/releases/{}/".format(
                name, name
            )
        )
        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        run("rm -rf /data/web_static/current")
        run(
            "ln -s /data/web_static/releases/{}/ \
                /data/web_static/current".format(
                name,
            )
        )
        return True
    except BaseException:
        return False

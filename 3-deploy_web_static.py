#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack."""
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists


env.hosts = ["100.25.146.136", "54.237.38.206"]


def do_pack():
    """generates a .tgz archive from the contents of the web_static"""
    try:
        local("mkdir -p versions")
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if exists(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        path = "/data/web_static/releases/{}/".format(no_ext)
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(path))
        run("sudo tar -xzf /tmp/{} -C {}".format(filename, path))
        run("sudo rm /tmp/{}".format(filename))
        run("sudo mv {}web_static/* {}".format(path, path))
        run("sudo rm -rf {}web_static".format(path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(path))
        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

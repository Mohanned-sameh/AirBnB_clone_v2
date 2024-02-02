#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ["100.24.74.133", "100.26.162.171"]
env.user = "ubuntu"


def do_pack():
    """creates an archive from the web_static folder"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_n = "versions/web_static_{}.tgz".format(date)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(file_n))
        return file_n
    except Exception as e:
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        file_n = archive_path.split("/")[1].split(".")[0]
        run("mkdir -p /data/web_static/releases/{}/".format(file_n))
        run(
            "tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/".format(
                file_n, file_n
            )
        )
        run("rm /tmp/{}.tgz".format(file_n))
        run(
            "mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(
                file_n, file_n
            )
        )
        run("rm -rf /data/web_static/releases/{}/web_static".format(file_n))
        run("rm -rf /data/web_static/current")
        run(
            "ln -s /data/web_static/releases/{}/\
                  /data/web_static/current".format(
                file_n
            )
        )
        return True
    except Exception as e:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

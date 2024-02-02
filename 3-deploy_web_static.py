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
    """generates a .tgz archive from the contents of the web_static folder"""
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(current_time)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception as e:
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        file_name = archive_path.split("/")[1][:-4]
        run("mkdir -p /data/web_static/releases/{}/".format(file_name))
        run(
            "tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/".format(
                file_name, file_name
            )
        )
        run("rm /tmp/{}.tgz".format(file_name))
        run(
            "mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(
                file_name, file_name
            )
        )
        run("rm -rf /data/web_static/releases/{}/web_static".format(file_name))
        run("rm -rf /data/web_static/current")
        run(
            "ln -s /data/web_static/releases/{}\
                  /data/web_static/current".format(
                file_name
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

#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack."""
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists


env.hosts = ["54.237.38.206", "100.25.146.136"]


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(filename))
    if result.succeeded:
        return filename
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to my web servers"""
    if exists(archive_path) is False:
        return False  # Returns False if the file at archive_path doesnt exist
    filename = archive_path.split("/")[-1]
    # so now filename is <web_static_2021041409349.tgz>
    no_tgz = "/data/web_static/releases/" + "{}".format(filename.split(".")[0])
    # curr = '/data/web_static/current'
    tmp = "/tmp/" + filename

    try:
        put(archive_path, "/tmp/")
        # ^ Upload the archive to the /tmp/ directory of the web server
        run("mkdir -p {}/".format(no_tgz))
        # Uncompress the archive to the folder /data/web_static/releases/
        # <archive filename without extension> on the web server
        run("tar -xzf {} -C {}/".format(tmp, no_tgz))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(no_tgz, no_tgz))
        run("rm -rf {}/web_static".format(no_tgz))
        # ^ Delete the archive from the web server
        run("rm -rf /data/web_static/current")
        # Delete the symbolic link /data/web_static/current from the web server
        run("ln -s {}/ /data/web_static/current".format(no_tgz))
        # Create a new the symbolic link /data/web_static/current on the
        # web server, linked to the new version of your code
        # (/data/web_static/releases/<archive filename without extension>)
        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    new_archive_path = do_pack()
    if exists(new_archive_path) is False:
        return False
    result = do_deploy(new_archive_path)
    return result

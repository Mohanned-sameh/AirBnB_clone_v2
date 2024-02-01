#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["100.25.146.136", "54.237.38.206"]


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        If the archive is successfully created - path of the archive.
        Otherwise - None.
    """
    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(date)
    try:
        local("tar -cvzf {} web_static".format(file))
        return file
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): Path of the archive to distribute.

    Returns:
        True if the archive has been successfully deployed.
        Otherwise, return False.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server.
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder
        # /data/web_static/releases/<archive filename without extension>
        filename = archive_path.split("/")[-1]
        folder_path = "/data/web_static/releases/{}".format(
            filename.replace(".tgz", "")
        )
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Move the content of the folder
        run("mv {}/web_static/* {}/".format(folder_path, folder_path))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf {}/web_static".format(folder_path))

        # Delete the old folder /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        run("ln -s {} /data/web_static/current".format(folder_path))

        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to a web server."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """Deletes out-of-date archives.

    Args:
        number (int): Number of archives to keep.
    """
    number = int(number)
    if number < 0:
        return
    elif number == 0 or number == 1:
        number = 2
    else:
        number += 1

    local("cd versions; ls -t | tail -n +{} | xargs rm -rf --".format(number))
    run(
        "cd /data/web_static/releases; ls -t \
            | tail -n +{} | xargs rm -rf --".format(
            number
        )
    )

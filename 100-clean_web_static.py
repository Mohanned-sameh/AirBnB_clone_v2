#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ["100.24.74.133", "100.26.162.171"]


@runs_once
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
    """Deletes out-of-date archives of the static files.
    Args:
        number (Any): The number of archives to keep.
    """
    archives = os.listdir("versions/")
    archives.sort(reverse=True)
    start = int(number)
    if not start:
        start += 1
    if start < len(archives):
        archives = archives[start:]
    else:
        archives = []
    for archive in archives:
        os.unlink("versions/{}".format(archive))
    cmd_parts = [
        "rm -rf $(",
        "find /data/web_static/releases/ -maxdepth 1 -type d -iregex",
        " '/data/web_static/releases/web_static_.*'",
        " | sort -r | tr '\\n' ' ' | cut -d ' ' -f{}-)".format(start + 1),
    ]
    run("".join(cmd_parts))

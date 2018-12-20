#!/usr/bin/python3
import os
import json

import subprocess
import argparse

from libtools import *

SCRIPT_FOLDER = 'git-tools'
CONFIG_FILENAME = 'purge-exclusion.txt'

parser = argparse.ArgumentParser(
    description="Clear repository from unnecessary branches.",
    epilog="Find more information at https://digitalduke.github.io/git-tools/"
)

parser.add_argument(
    "--version",
    action="version",
    version="purge branches version 1.0"
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    dest="dry_run",
    help="only report, doesn't do any real changes"
)

def run():
    args = parser.parse_args()

    command = ["git", "branch", "--merged"]
    git_process = subprocess.run(
        args=command,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    if git_process.returncode != 0:
        print("something wrong: %s" % git_process.stderr)
    else:

        # Get repos that is excluded from the purge
        with open(get_config_file_full_path(SCRIPT_FOLDER, CONFIG_FILENAME),
            'a+') as config_file:
                exclusion_repos = config_file.read()

        
        all_repositories = [
            repo.lstrip().rstrip()
            for repo in git_process.stdout.split("\n")
        ]

        # filter repos to those that can be purged
        repositories = [repo for repo in all_repositories 
            if repo != "" and repo != "master" and not repo.startswith("* ")
                and repo not in exclusion_repos
        ]

        repo_count = len(repositories)
        if repo_count == 0:
            print("nothing for purge")
        else:
            if args.dry_run:
                print("can purge this branches:")
                for repo in repositories:
                    print(" %s" % repo)
            else:
                command = ["git", "branch", "-d"]
                for repo in repositories:
                    command.append(repo)
                git_process = subprocess.run(
                    args=command,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    universal_newlines=True
                )
                if git_process.returncode != 0:
                    print("something wrong: %s" % git_process.stderr)
                else:
                    print("all done, purged %d branch(es)" % repo_count)


if __name__ == "__main__":
    run()

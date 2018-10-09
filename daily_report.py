from datetime import date, datetime
from github import Github, BadCredentialsException

ACCESS_TOKEN = ""
REPO_NAME = "a-iv/100maketov"

today = datetime.combine(date.today(), datetime.min.time())

github = Github(ACCESS_TOKEN)
user = github.get_user()


try:
    repo = github.get_repo(REPO_NAME)
except (Exception, BadCredentialsException) as error:
    print("Can't get repo %s" % REPO_NAME)


try:
    closed_issues = user.get_issues(state="closed", since=today)
    print("List of daily closed issues")
    for issue in closed_issues:
        print(issue.number, issue.html_url, issue.title)
    print()
except (Exception, BadCredentialsException) as error:
    print("Can't get list of closed issues.")


try:
    commits = repo.get_commits(since=today, author=user)
    print("List of daily commits in repo \"%s\" in PR which already closed" % REPO_NAME)
    for commit in commits:
        if not commit.commit.message.startswith("Merge"):
            print(commit.sha[:7], commit.html_url, commit.commit.message)
    print()
except (Exception, BadCredentialsException) as error:
    print("Can't get list of commits in PR which already closed.")


try:
    pulls = repo.get_pulls(state="open", base="master")
    if pulls:
        print("List of daily commits in repo \"%s\" in PR which don't closed" % REPO_NAME)

    for pr in pulls:
        commits = pr.get_commits()
        print_pr_number = True

        for commit in commits:

            if not commit.commit.author.name == user.name:
                continue

            if commit.commit.author.date.year == today.year and \
                    commit.commit.author.date.month == today.month and \
                    commit.commit.author.date.day == today.day:
                if print_pr_number:
                    print("PR#%s %s %s" % (pr.number, pr.html_url, pr.title))
                    print_pr_number = False

                print(commit.sha[:7], commit.html_url, commit.commit.message)

except (Exception, BadCredentialsException) as error:
    print("Can't get list of commits in opened PR.")


print("\r\nDone.")

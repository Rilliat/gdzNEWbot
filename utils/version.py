__version__ = (4, 0, 0)

import os
import git


try:
    branch = git.Repo(
        path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    ).active_branch.name
except Exception:
    branch = 'master'


def get_git_hash() -> str | bool:
    """
    Get current git hash
    :return: Git commit hash
    """
    try:
        return git.Repo().head.commit.hexsha
    except Exception:
        return False


def get_update_status():
    repo = git.Repo(search_parent_directories=True)
    diff = repo.git.log([f"HEAD..origin/{branch}", "--oneline"])
    upd = (
        'Скоро обновление!' if diff else 'Актуальная версия.'
    )
    return upd


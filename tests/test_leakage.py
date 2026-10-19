import os, subprocess, tempfile
import pytest
from timemachine.ingest_git import ingest_git
from timemachine.view import TimeView, LeakageError


@pytest.fixture
def repo():
    d = tempfile.mkdtemp()
    def run(*a, date):
        env = {**os.environ, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
        subprocess.run(["git", "-C", d, *a], check=True, env=env, capture_output=True)
    run("init", "-q", date="2020-01-01T00:00:00Z")
    run("config", "user.email", "a@b.c", date="2020-01-01T00:00:00Z"); run("config", "user.name", "a", date="2020-01-01T00:00:00Z")
    for n, date in enumerate(["2020-01-01T00:00:00Z", "2020-06-01T00:00:00Z"]):
        open(f"{d}/f.py", "w").write(f"x={n}\n"); run("add", ".", date=date); run("commit", "-qm", f"c{n}", date=date)
    return d


def test_future_commits_invisible(repo):
    db = os.path.join(repo, "..", "t.db"); ingest_git(repo, db)
    shas = subprocess.run(["git", "-C", repo, "log", "--format=%H"], capture_output=True, text=True).stdout.split()
    v = TimeView(db, repo, 1580000000)  # ~2020-01-26
    assert len(v.commits()) == 1
    with pytest.raises(LeakageError):
        v.diff(shas[0])  # newest commit, after T
    assert v.diff(shas[1])

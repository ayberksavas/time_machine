"""SQLite store. Every row carries the timestamp at which it became *visible* in reality."""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS commits(
  sha TEXT PRIMARY KEY, ts INTEGER NOT NULL, author_ts INTEGER, author TEXT,
  message TEXT, parents TEXT);                     -- ts = committer time (visibility)
CREATE TABLE IF NOT EXISTS commit_files(
  sha TEXT, path TEXT, added INTEGER, deleted INTEGER, is_test INTEGER, is_doc INTEGER);
CREATE INDEX IF NOT EXISTS cf_sha ON commit_files(sha);
CREATE INDEX IF NOT EXISTS cf_path ON commit_files(path);
CREATE TABLE IF NOT EXISTS issues(
  number INTEGER PRIMARY KEY, is_pr INTEGER, ts INTEGER NOT NULL, author TEXT,
  title TEXT, body TEXT);                          -- ts = created_at; body = latest (see README caveat)
CREATE TABLE IF NOT EXISTS issue_events(
  number INTEGER, ts INTEGER NOT NULL, type TEXT, actor TEXT, data TEXT);
CREATE INDEX IF NOT EXISTS ie_num ON issue_events(number);
CREATE TABLE IF NOT EXISTS comments(
  id INTEGER PRIMARY KEY, number INTEGER, ts INTEGER NOT NULL, author TEXT,
  body TEXT, kind TEXT);                           -- kind: issue | review
CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
"""


def connect(path: str) -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.executescript(SCHEMA)
    return db

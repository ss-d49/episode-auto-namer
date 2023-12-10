#!/usr/bin/env python3
"""This script renames all files in the current directory to match the data in a database created from TVDB data."""

import argparse
import re
from pathlib import Path
from pytvdbapi import api
from episode_auto_namer_scraper.common.Database import Database
from episode_auto_namer_scraper.common.schema import Title, Episode
from typing import Callable
from contextlib import contextmanager, AbstractContextManager
from sqlalchemy.orm import Session


def containsTitle(title, filename):
    words = title.split(' ')
    count = 0
    regex = r".*"
    for word in words:
        regex += word.strip(':|-|_| ') + '.*'
    regex += '$'
    matches = re.search(regex, filename)
    if matches:
        return True
    else:
        return False


def rename_episode(file, series, session_factory: Callable[..., AbstractContextManager[Session]]):
    with session_factory() as session:
        eps = session.query(Title).filter(
            Title.title.ilike(f"%{series}%")).first().episodes

    for e in eps:
        if e.seasonNumber != None:
            if f"S{e.seasonNumber:02}E{e.episodeNumber:02}" in file.name:
                newname = f"{series} - S{e.seasonNumber:02}E{e.episodeNumber:02} - {e.episodeTitle.replace('?','').replace('/','-').replace(':',' -')}{file.suffix}"
                print(newname)
                file.rename(newname)
            elif containsTitle(e.episodeTitle, file.name):
                newname = f"{series} - S{e.seasonNumber:02}E{e.episodeNumber:02} - {e.episodeTitle.replace('?','').replace('/','-').replace(':',' -')}{file.suffix}"
                print(newname)
                file.rename(newname)


def main():
    db_uri = "mariadb+pymysql://root:root@localhost:3306/media2"
    session_factory = Database(db_uri).session

    parser = argparse.ArgumentParser("Usage: epNamer.py ")
    parser.add_argument("series", help="name of the series")
    args = parser.parse_args()

    for file in Path('.').glob('*.*'):
        rename_episode(file, args.series, session_factory)


if __name__ == '__main__':
    main()

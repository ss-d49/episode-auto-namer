#!/usr/bin/env python3
"""This script imports data into a database from tvdb."""

import argparse

from pytvdbapi import api
from episode_auto_namer_scraper.common.Database import Database
from episode_auto_namer_scraper.common.schema import Title, Episode
from typing import Callable
from contextlib import contextmanager, AbstractContextManager
from sqlalchemy.orm import Session


def retrieveToDb(series, language, session_factory: Callable[..., AbstractContextManager[Session]]):
    db = api.TVDB("B43FF87DE395DF56")
    result = db.search(f"{series}", language)
    show = result[0]
    show.update()
    print(show.lang)
    with session_factory() as session:
        if language == "en":
            session.merge(Title(
                titleId=show.id,
                titleIMDBId=show.IMDB_ID[2:] or None,
                title=show.SeriesName,
                titleSynopsis=show.Overview,
                network=show.Network)
            )
        else:
            session.merge(Title(
                titleId=show.id,
                originalTitle=show.SeriesName,
                titleOriginalSynopsis=show.Overview)
            )

        for season in show:
            for episode in season:
                if episode.EpisodeName != "":
                    if language == "en":
                        session.merge(Episode(
                            titleId=show.id,
                            episodeId=episode.id,
                            episodeIMDBId=episode.IMDB_ID[2:] or None,
                            seasonNumber=season.season_number,
                            episodeNumber=episode.EpisodeNumber,
                            episodeTitle=episode.EpisodeName,
                            episodeAired=episode.FirstAired or None,
                            episodeSynopsis=episode.Overview)
                        )
                    else:
                        session.merge(Episode(
                            episodeId=episode.id,
                            episodeOriginalTitle=episode.EpisodeName,
                            episodeOriginalSynopsis=episode.Overview)
                        )

        session.commit()


def main():
    db_uri = "mariadb+pymysql://root:root@localhost:3306/media2"
    session_factory = Database(db_uri).session

    parser = argparse.ArgumentParser(
        description="Usage: get.py \"name of series\"")
    parser.add_argument("series", help="name of the series")
    parser.add_argument("language")
    args = parser.parse_args()
    retrieveToDb(args.series, args.language, session_factory)


if __name__ == '__main__':
    main()

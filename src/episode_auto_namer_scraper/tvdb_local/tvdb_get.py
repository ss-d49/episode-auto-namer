#!/usr/bin/env python3
"""This script imports data into a database from tvdb."""

import argparse

from pytvdbapi import api
from episode_auto_namer_scraper.common.database import create_connection
from episode_auto_namer_scraper.common.schema import Title, Episode


def retrieveToDb(series, table, language, session):
    db = api.TVDB("B43FF87DE395DF56")
    result = db.search(f"{series}", language)
    show = result[0]
    show.update()
    print(show.lang)

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
    session = create_connection()

    parser = argparse.ArgumentParser(
        description="Usage: get.py \"name of series\"")
    parser.add_argument("series", help="name of the series")
    parser.add_argument("table", help="name of table in database for the series")
    parser.add_argument("language")
    args = parser.parse_args()
    retrieveToDb(args.series, args.table, args.language, session)


if __name__ == '__main__':
    main()

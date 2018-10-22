#!/usr/bin/python -tt
# -*- encoding: UTF-8 -*-
"""
'I Refuse' web application
Copyright (C) 2017  Jacob Delgado

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import json
import logging
import logging.config

import irefuse.irefuse


def setup_logging(logging_config: str) -> logging.Logger:
    with open(logging_config, 'rt') as f:
        config = json.load(f)
    logging.config.dictConfig(config)

    return logging.getLogger()


def main():
    """
    Main function
    """
    logger = setup_logging('logging.json')
    logger.info("Starting I Refuse")

    game_play = irefuse.irefuse.IRefuse()
    try:
        game_play.setup(input)
        winners = game_play.play(input)
    except Exception:
        logger.exception("Unhandled exception. Exiting.")
        raise

    for winner in winners:
        logger.info("Winner: {}".format(winner))
    logger.info("Shutting down I Refuse")


if __name__ == "__main__":
    main()

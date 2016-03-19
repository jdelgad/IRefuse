[![Build Status](https://travis-ci.org/jdelgad/IRefuse.svg?branch=master)](https://travis-ci.org/jdelgad/IRefuse)
[![codecov.io](https://codecov.io/github/jdelgad/IRefuse/coverage.svg?branch=master)](https://codecov.io/github/jdelgad/IRefuse?branch=master)
[![Code Climate](https://codeclimate.com/github/jdelgad/IRefuse/badges/gpa.svg)](https://codeclimate.com/github/jdelgad/IRefuse)

# I Refuse

Simple card game where the objective is to have the least amount of points at the end of the game.

## Setup and Rules
- There are 33 cards in the deck, ranging from \[3-35\].
- The deck is shuffled at the begging and 11 cards are discarded. The remaining cards are in play.
  - No player knows what card values have been discarded.
- Players start out with 11 tokens.
  - These tokens are used to pass on a card if the player chooses.
  - Tokens are accumulated per pass, until a card and its tokens are taken.
  - Tokens have a negative point value of -1.
  - Tokens are subtracted from your card total (by value) when all cards are accounted for.
- When all cards have been taken, the player with the fewest points summed over their hand wins.
- Caveat
  - If a player has a run (e.g. they have 7-8-9 in their hand), then only the lowest valued card is counted.
  - A run can be as few as 2 cards.

## Plan
- v1.0: Support 3-5 players at the command prompt only.
- v1.1: Minor refactor. No rules change. Got rid of code smells.

Software is licensed under the GPL

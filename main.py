#!/usr/bin/env python -tt


def setup_players(input_func):
    print("Number of players: ")
    num = input_func()
    if num < 3 or num > 5:
        raise AssertionError("invalid number of players")
    return num

def main():
    setup_players(input)

if __name__ == "__main__":
    main()
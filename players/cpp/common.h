#ifndef COMMON_H
#define COMMON_H

#include <iostream>
#include <string>
#include <vector>

struct Player {
    int x, y, dx, dy, speed, speed_reset_time, powerup;
    bool alive;
    Player () {}
    Player (std::istream& is) {
        is >> x >> y >> dx >> dy >> speed >> speed_reset_time >> alive >> powerup;
    }
};

struct PowerUp {
    int x, y;
};

struct Map {
    int width, height;
    std::vector<std::vector<bool>> contents;
    std::vector<PowerUp> powerups;
};

enum Direction: char {
    LEFT = 'L',
    RIGHT = 'R',
    NONE = 'x'
};

struct Command {
    Direction direction;
    bool use_powerup;
};

Player player_from_input();

void read_state();

void greet_server(const char *name, const char *color);

void send_command(const Command cmd);

#endif

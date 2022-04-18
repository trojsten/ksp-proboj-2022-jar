#include <iostream>
#include <string>
#include <vector>

struct Player {
    int x, y, dx, dy, speed, speed_reset_time, powerup;
    bool alive;
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
}

Player player_from_input() {
    Player p;
    std::cin >> p.x >> p.y >> p.dx >> p.dy >> p.speed >> p.speed_reset_time >> p.alive >> p.powerup;
    return p;
}

Player MYSELF;
Map MAP;
std::vector<Player> PLAYERS;
std::string NAME, COLOR;

void read_state() {
    std::cin >> MAP.width >> MAP.height;
    if (MAP.contents.empty()) {
        for (int x = 0; x < MAP.width; ++x) {
            std::vector<bool> row;
            for (int y = 0; y < MAP.height; ++y) {
                row.push_back(false);
            }
            MAP.contents.push_back(row);
        }
    }

    for (int y = 0; y < MAP.height; ++y) {
        for (int x = 0; x < MAP.width; ++x) {
            bool a;
            std::cin >> a;
            MAP.contents[x][y] = a;
        }
    }

    MYSELF = player_from_input();
    int players;
    std::cin >> players;
    PLAYERS.clear();
    for (int i = 0; i < players; ++i) {
        PLAYERS.push_back(player_from_input());
    }

    int powerups;
    std::cin >> powerups;
    MAP.powerups.clear();
    for (int i = 0; i < powerups; ++i) {
        PowerUp p;
        std::cin >> p.x >> p.y;
        MAP.powerups.push_back(p);
    }

    char dot;
    std::cin >> dot;
}

void greet_server() {
    std::string hello;
    std::cin >> hello;
    char dot;
    std::cin >> dot;
    std::cout << NAME << COLOR << std::endl << "." << std::endl;
}

Command do_turn() {
    int x = rand() % 3;
    Command cmd;
    if (x == 0) {
        cmd.direction = LEFT;
    } else if (x == 1) {
        cmd.direction = RIGHT;
    } else {
        cmd.direction = NONE;
    }
    return cmd;
}

int main() {
    srand(time(0));

    NAME = "Cpp";
    COLOR = "#00ff00";

    greet_server();

    MYSELF.alive = true;
    while (MYSELF.alive) {
        read_state();
        Command cmd = do_turn();
        if (cmd.use_powerup) {
            std::cout << cmd.direction << "+" << std::endl;
        } else {
            std::cout << cmd.direction << std::endl;
        }
        std::cout << "." << std::endl;
    }
}

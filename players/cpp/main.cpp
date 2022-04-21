#include "common.h"

#define NAME "cpp"
#define COLOR "#00ff00"


Player MYSELF;
Map MAP;
std::vector<Player> PLAYERS;

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

    greet_server(NAME, COLOR);

    MYSELF.alive = true;
    while (MYSELF.alive) {
        read_state();
        Command cmd = do_turn();
        send_command(cmd);
    }
    std::cout << "Bye\n";
}

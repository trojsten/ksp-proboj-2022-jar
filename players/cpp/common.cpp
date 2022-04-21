#include "common.h"

Player player_from_input() {
    return Player(std::cin);
}

void greet_server(const char *name, const char *color) {
    std::string hello;
    char dot;
    std::cin >> hello >> dot;
    std::cout << name << ' ' << color << "\n." << std::endl;
}

void send_command(const Command cmd) {
    std::cout << cmd.direction << ((cmd.use_powerup) ? "+" : "") << "\n." << std::endl;
}

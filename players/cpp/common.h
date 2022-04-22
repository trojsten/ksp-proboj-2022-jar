#ifndef COMMON_H
#define COMMON_H

#include <iostream>
#include <string>
#include <vector>

struct Player {
	int x, y, dx, dy, speed, speed_reset_time, powerup;
	bool alive;

	void update ();
};

struct PowerUp {
	int x, y;

	void update ();
};

struct Command {
	char direction;
	bool use_powerup;
};

//dalej citat pravdepodobne naozaj nemusis

void read_state ();

void greet_server (const char *name, const char *color);

void send_command (const Command& cmd);

void end_communication ();

template<class T>
void update (std::vector<T>& vec) {
	int n;
	std::cin >> n;
	if (vec.empty()) vec.assign(n, T());
	for (int i = 0; i < n; ++i) vec[i].update();
}

template<class T>
void update (std::vector<std::vector<T>>& vec) {
	int w, h;
	std::cin >> w >> h;
	if (vec.empty()) vec.assign(w, std::vector<T>(h, T()));
	for (int y = 0; y < h; ++y) for (int x = 0; x < w; ++x) std::cin >> vec[x][y];
}

template<class T>
void update (T& p) {
	p.update();
}

#endif

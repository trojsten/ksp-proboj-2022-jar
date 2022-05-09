#ifndef COMMON_H
#define COMMON_H

#include <bits/stdc++.h>

using namespace std;

#define FOR(i, n) for(int i = 0; i < n; i++)

template<typename T>
ostream& operator<<(ostream &out, vector<T> cont)
{
    for(auto it = cont.begin(); it != cont.end(); it++)
        out << *it << (it != cont.end()-1 ? ' ' : '\n');
    return out;
}

template<typename T>
ostream& operator<<(ostream &out, vector<vector<T>> cont)
{
    for(auto it = cont.begin(); it != cont.end(); it++)
        out << *it;
    return out;
}

// pohyb
#define LEFT   -1
#define RIGHT   1
#define FORWARD 0

// powerupy Player.powerup
#define NO_POWERUP   0
#define SPEED_ME     1
#define SPEED_OTHERS 2
#define STOP_ME      3
#define STOP_OTHERS  4
#define CLEAN        5

const int  DX[] = { 0, 1, 0, -1};
const int  DY[] = {-1, 0, 1,  0};
const char DS[] = {FORWARD, RIGHT, LEFT};

struct Player {
	int x, y, dx, dy, speed, speed_reset_time, powerup, d;
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
void update (vector<T>& vec) {
	int n;
	cin >> n;
	vec.resize(n+1);
	for (int i = 0; i < n; ++i) vec[i].update();
}

template<class T>
void update (vector<vector<T>>& vec) {
	int w, h;
	cin >> w >> h;
	if (vec.empty()) vec.assign(w, vector<T>(h, T()));
	for (int y = 0; y < h; ++y) for (int x = 0; x < w; ++x) cin >> vec[x][y];
}

template<class T>
void update (T& p) {
	p.update();
}

#endif

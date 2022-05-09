#include "common.h"
//uplne nezaujimave nemusis citat
//definuje iba format komunikacie so serverom

void Player::update () {
	cin >> alive >> x >> y >> dx >> dy >> speed >> speed_reset_time >> powerup;
	for (int i = 0; i < 4; ++i)
		if(dx == DX[i] && dy == DY[i])
			d = i;
}

void PowerUp::update () {
	cin >> x >> y;
}

void greet_server (const char *name, const char *color) {
	string hello;
	char dot;
	cin >> hello >> dot;
	cout << name << ' ' << color << "\n." << endl;
}

void send_command (const Command& cmd) {
	char DS[] = {'L', 'x', 'R'};
	cout << DS[cmd.direction+1] << ((cmd.use_powerup) ? "+" : "") << "\n." << endl;
}

void end_communication () {
	char dot;
	cin >> dot;
}

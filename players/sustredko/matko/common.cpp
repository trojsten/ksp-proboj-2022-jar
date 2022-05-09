#include "common.h"

// uplne nezaujimave nemusis citat
// definuje iba format komunikacie so serverom

void Player::update()
{
	std::cin >> alive >> x >> y >> dx >> dy >> speed >> speed_reset_time >> powerup;
}

void PowerUp::update()
{
	std::cin >> x >> y;
}

void greet_server(const char *name, const char *color)
{
	std::string hello;
	char dot;
	std::cin >> hello >> dot;
	std::cout << name << ' ' << color << "\n." << std::endl;
}

void send_command(const Command &cmd)
{
	char DS[] = {'L', 'x', 'R'};
	std::cout << DS[cmd.direction + 1] << ((cmd.use_powerup) ? "+" : "") << "\n." << std::endl;
}

void end_communication()
{
	char dot;
	std::cin >> dot;
}

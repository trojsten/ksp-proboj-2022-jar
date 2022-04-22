#include "common.h"

// pohyb
#define LEFT    -1
#define RIGHT   1
#define FORWARD 0

// powerupy Player.powerup
#define NO_POWERUP   0
#define SPEED_ME     1
#define SPEED_OTHERS 2
#define STOP_ME      3
#define STOP_OTHERS  4
#define CLEAN        5

#define NAME "cpp"
#define COLOR "#00ff00"

int  DX[] = { 0, 1, 0, -1};
int  DY[] = {-1, 0, 1,  0};
char DS[] = {LEFT, FORWARD, RIGHT};

int width, height; 
Player myself;
std::vector<std::vector<int>> walls;
std::vector<PowerUp> powerups;
std::vector<Player> players;

// vrati smer ktorym sme prave otoceny
int get_my_direction() {
	for (int i = 0; i < 4; ++i)
		if(myself.dx == DX[i] && myself.dy == DY[i])
			return i;
	return -1;
}

// skontrolujem ci sa pozeram do pola a ci je v nom 0
bool is_free(int x, int y) {
	return x >= 0 && x < width && y >= 0 && y < height && !walls[x][y];
}

void read_state() {
	update(walls);
	update(myself);
	update(players);
	update(powerups);

	end_communication();
	width = walls.size();
	height = walls[0].size();
}


// sem pis svoj kod
Command do_turn() {
	int x, y;
	Command cmd;
	// ak mam powerup pouzijem ho
	if (myself.powerup != NO_POWERUP) cmd.use_powerup = true;
	
	int direction = get_my_direction();
	// vyskusam pohyb vsetkymi moznymi smermi
	for (int i = 0; i < 3; ++i) {
		// zratam potencionalnu polohu
		x = myself.x + DX[(direction+DS[i]+4)%4];
		y = myself.y + DY[(direction+DS[i]+4)%4];
		// skontrolujem ci je volne
		if (is_free(x,y)) {
			cmd.direction = DS[i];
		}
	}
	// vypisem si kam sa chcem hybat lebo mozem
	std::cerr << x << ' ' << y << '\n'; 
	return cmd;
}

int main() {
	// aby sme mali nahodu
	srand(time(0));
	// povieme serveru ako sa chceme volat a farbu
	greet_server(NAME, COLOR);
	// robime tahy kym sme zivy
	myself.alive = true;
	while (myself.alive) {
		read_state();
		send_command(do_turn());
	}
	std::cout << "Bye\n";
}

#include "common.h"
#include <bits/stdc++.h>
using namespace std;

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

#define NAME "DuPi(dup)"
#define COLOR "#5e1c73"

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



	/*void Update_okolia(int y, int x){
		for (int i = 0; i < 4; i++){
			if (mapa_[y][x] + 1 < mapa_[y + DY[i]][x + DX[i]]) {
				mapa_[y + DY[i]][x + DX[i]] == mapa_[y][x] + 1;
				Pridaj_do_queue(y + DY[i], x + DX[i]);
			}
		}
	}*/

int BFS(int x, int y)
{
	if (!is_free(x, y)) return 0;
	queue<pair<int, int>> q;
	vector<vector<bool>> visited;
	for (int i = 0; i < walls.size(); i++)
	{
		vector<bool> temp;
		for (int j = 0; j < walls[0].size(); j++)
		{
			temp.push_back(walls[i][j]);
		}
		visited.push_back(temp);
	}

	q.push(pair<int, int>(x, y));
	int cnt = 0;
	while (!q.empty())
	{
		pair<int, int> cur = q.front();
		q.pop();
		if (!visited[cur.first][cur.second])
		{
			cnt++;
			visited[cur.first][cur.second] = true;
			for (int i = 0; i < 4; i++)
				if (is_free(cur.first + DX[i], cur.second + DY[i]))
					q.push(pair<int, int>(cur.first + DX[i], cur.second + DY[i]));
		}
		
	}
	return cnt;
}

// sem pis svoj kod
/*Command do_turn() {
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
}*/
Command do_turn(){
	if (get_my_direction() == -1)
		{
			Command cmd;
			cmd.direction = DS[1];
			cmd.use_powerup = false;
			return cmd;
		}
	pair<int, int> najlepsie(-1, 0);
	int x, y;
	for (int i = 0; i < 3; i++)
	{
		y = myself.y + (DY[(get_my_direction()+DS[i]+4)%4]) * myself.speed;
		x = myself.x + (DX[(get_my_direction()+DS[i]+4)%4]) * myself.speed;
		bool mozem = true;
		for (int j = 1; j<=myself.speed; j++)
		{
				x = myself.x + (DX[(get_my_direction() + DS[i] +4) %4] *j);
				y = myself.y + (DY[(get_my_direction() + DS[i] +4) %4] *j);
				if (!is_free(x,y) || !mozem){
					mozem = false;
				}
				else {
					mozem = true;
				}
			}
		if (mozem)
		{
			int bfs = BFS(x, y);
			//cerr << get_my_direction() << " " << myself.x << " " << myself.y << " " << i << " " << x << " " << y << endl;
			if (bfs > najlepsie.second)
			{
				najlepsie.first = i;
				najlepsie.second = bfs;
			}
		}
	}
	while (najlepsie.first == -1) {}
	Command cmd;
	cmd.direction = DS[najlepsie.first];
	cmd.use_powerup = false;
	if (myself.powerup == 5 || myself.powerup == 3)
	{
		if (najlepsie.second <= 3 * myself.speed)
		{
			cmd.use_powerup = true;
			return cmd;
		}
		bool isPowerup = false;
		for (int j = 0; j < powerups.size(); j++)
			if (powerups[j].x == x + DX[(DS[get_my_direction()]+4)%4] && powerups[j].y == y + DY[(+DS[get_my_direction()]+4)%4])
			{
				isPowerup = true;
			}
		if (isPowerup)
			cmd.use_powerup = true;
	}

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

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

#define NAME "0bodovgang"
#define COLOR "#b00b69"

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
vector<vector<int>> first(50, vector<int>(50, 150)); // za kollko sa dostane na miesto
vector<vector<int>> predosla;
vector<pair<int, int>> en_play;
unordered_set<int> seen;
void bfs(int x, int y, int smer) // hrac - nepriatel alebo ja, krok - predpocitanie
{
	int md = smer;
	first[x][y] = 0;
	queue<vector<int>> mozne; // kam sa vieme dostat z pozicie x y
	vector<vector<int>> vis(50, vector<int>(50, 0)); // navstivene
	mozne.push({x, y, md});
	//cerr << mozne.size() << endl;
	while (mozne.size() != 0)
	{
		int xn = mozne.front()[0];
		int yn = mozne.front()[1];
		int md = mozne.front()[2];
		//cerr << xn << " " << yn << " " << md << endl;
		vis[xn][yn] = 1;
		//cerr << vis[xn][yn] << endl;
		for(int a = 0; a < 3; a++)
		{
			int xh = xn + DX[(md+DS[a]+4)%4];
			int yh = xn + DY[(md+DS[a]+4)%4];
			if (is_free(xh, yh))
			{
				if (first[xh][yh] > first[xn][yn] + 1 && vis[xh][yh] == 0)
				{
					first[xh][yh] = first[xn][yn]+1;
					mozne.push({xh, yh, DS[a]});
					vis[xh][yh] = 1;
				}
			}
		}
		mozne.pop();
		//cerr << mozne.size() << endl;
	}
}

pair<int,int> minmax(int x, int y, int deep, int smer){ // 0 - vpravo, 1 - vlavo, 2 - dole, 3 - hore
	//cerr << "GOT MINMAX" << '\n';
	if(seen.find(x*100+y) != seen.end())
		return {smer, -90};
	else if(is_free(x, y) == false && deep != 0)
		return {smer, -80};
	else if(first[x][y]<= deep && deep != 0)
		return {smer, -70};
	else if(deep == 11)
		return {smer, 100};

	seen.insert(x*100+y);
	vector<pair<int, int>> smery(4);
	if(smer != 1){
		smery[3]= minmax(x-1, y, deep+1, 3);
		smery[3].first = 3;
	}
	if(smer != 3){
		smery[1] = minmax(x+1, y, deep+1, 1);
		smery[1].first = 1;
	}
	if(smer != 2){
		smery[0] = minmax(x, y-1, deep+1, 0);
		smery[0].first = 0;
	}
	if(smer != 0){
		smery[2] = minmax(x, y+1, deep+1, 2);
		smery[2].first = 2;
	}
	seen.erase(x*100+y);
	
	int pocMoznosti = 0;
	pair<int, int> best = smery[0];
	for(auto i:smery){
		if(i.second > best.second && i.second != 0)
			best = i;
		pocMoznosti += i.second;
	}
	return {best.first, pocMoznosti+1};

}

Command do_turn() {
	Command cmd;
	// ak mam powerup pouzijem ho
	//if (myself.powerup != NO_POWERUP) cmd.use_powerup = true;
	
	int direction = get_my_direction(); // 
	// skontrolujem ci je volne
	/*if (is_free(x,y)) {
		cmd.direction = DS[i];
	}*/


	int x = myself.x, y = myself.y;

	en_play.clear();
	if (!predosla.empty()){
		for(int i=0;i<height;i++){ // predtym tu bolo 50
			for(int ii=0;ii<width;ii++){ // predtym tu
				if(walls[ii][i]==1 && predosla[ii][i]==0){
					en_play.push_back({ii,i});
				}
			}
		}
		int sizeOfEnPlay = en_play.size();
		for(int i = 0; i < sizeOfEnPlay; i++){
			for (int j = 0; j < 2; j++){
				bfs(en_play[i].first, en_play[i].second, j);
			}
		}
	}
	pair <int, int> kam = minmax(x, y, 0, direction);
	
	for(int i=0; i<3; i++){

		
		if(kam.first == 0 && is_free(x, y-1) == false)
			kam.first++;
		if(kam.first == 1 && is_free(x+1, y) == false)
			kam.first++;
		if(kam.first == 2 && is_free(x, y+1) == false)
			kam.first++;
		if(kam.first == 3 && is_free(x-1, y) == false)
			kam.first=0;
		if(abs(kam.first-direction) == 2)
			kam.first = (kam.first+1)%4;
	}	
	if (kam.first == direction){
		cmd.direction = 0;
	}
	else if (kam.first - direction == 1 || kam.first - direction == -3){
		cmd.direction = 1;
	}
	else{
		cmd.direction = -1;
	}

	predosla = walls;
	
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

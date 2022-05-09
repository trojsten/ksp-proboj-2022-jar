#include "common.h"

#define NAME "Veduci_cpp"
#define COLOR "#818F3D"


int width, height; 
Player myself;
vector<vector<int>> walls;
vector<vector<int>> supermapa;
vector<PowerUp> powerups;
vector<Player> players;
vector<Player> old_players;


void update_super_map(const vector<vector<int>>& mapa, vector<vector<int>>& supermapa) {
	if (supermapa.empty()) {
		supermapa.assign(width, vector<int>(height, -1));
		for (int y = 0; y < height; ++y) for (int x = 0; x < width; ++x)
			if (mapa[x][y] == 1) supermapa[x][y] = -2;
	}

	for (int y = 0; y < height; ++y) for (int x = 0; x < width; ++x)
			if (mapa[x][y] == 0) supermapa[x][y] = -1;

	for(int i = 0; i < players.size(); i++) {
		while (old_players[i].x != players[i].x || old_players[i].y != players[i].y) {
			old_players[i].x += players[i].dx;
			old_players[i].y += players[i].dy;
			if (mapa[old_players[i].x][old_players[i].y] == 1){
				supermapa[old_players[i].x][old_players[i].y] = -i-3;
			} 
			else cerr << "nesedia data x y: " << old_players[i].x << " " << old_players[i].y << endl;
		}
	}
    // cerr << supermapa;

}



// skontrolujem ci sa pozeram do pola a ci je v nom 0
bool is_free(const vector<vector<int>>& A, int x, int y) {
	return x >= 0 && x < width && y >= 0 && y < height && A[x][y] >= -1;
}

// pole je mapa, -2 je stena, -3 a dalej su steny hracov, -1 je volne,
// zapise na volne vzdialensot od najblizsieho startu
// vracia sucet velkosti komponentov
int bfs(vector<vector<int>>& pole, vector <vector<int>> starts) {
    int res = 0;
    queue<vector<int>> Q;
    for(auto v : starts)
    {
        v.push_back(0);
        Q.push(v);
        res++;
        pole[v[0]][v[1]] = 0;
    }


    while (Q.size())
    {
        auto cur = Q.front();
        Q.pop();
        int d = cur[2]+1;
        FOR(i, 4)
        {
            int x = cur[0]+DX[i], y = cur[1]+DY[i];
            if(is_free(pole, x, y) && pole[x][y] == -1)
            {
                pole[x][y] = d;
                Q.push({x, y, d});
                res++;
            }
        }
    }
    return res;
}

void read_state() {
	old_players = players;
	update(walls);
	update(myself);
	update(players);
	update(powerups);

	end_communication();
	width = walls.size();
	height = walls[0].size();
	players[players.size()-1] = myself;
	if(old_players.empty()) old_players = players;
	update_super_map(walls, supermapa);
}




Command hlupy_turn(Player& me = myself) {
	int x, y;
	Command cmd;
	if (me.powerup != NO_POWERUP) cmd.use_powerup = true;

    vector<int> komponenty;
	
	for (int i = 0; i < 3; ++i) {
	    bool ok = true;
		for (int j = 1; j <= myself.speed; ++j) {
			x = me.x + j*DX[(me.d+DS[i]+4)%4];
			y = me.y + j*DY[(me.d+DS[i]+4)%4];

			if (!is_free(supermapa, x, y)) {
				ok = false;
			}
		}
		if (ok) {
			auto m = supermapa;
            int dx = DX[(me.d+DS[i]+4)%4], dy = DY[(me.d+DS[i]+4)%4];
            for(int s = 1; s <= me.speed; s++)
            {
                m[me.x+dx*s][me.y+dy*s] = m[me.x][me.y];
            }
            komponenty.push_back(bfs(m, {{me.x+dx*me.speed, me.y+dy*me.speed}}));
		}
        else komponenty.push_back(0);
	}

	

    int best = 0;
    FOR(i, 3)
    {
        if(komponenty[best] < komponenty[i]) best = i;
    }

	if(komponenty[best] == 0) cout << "penis123\n" << flush;

    cmd.direction = DS[best];

	return cmd;
}

	



Command do_turn() {
	return hlupy_turn();
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
	cout << "Bye\n";
}

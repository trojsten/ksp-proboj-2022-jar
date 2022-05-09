#include "common.h"
#include<bits/stdc++.h>
using namespace std;

#define For(i, a, n) for(int i = a;i< n;i++)
typedef long long ll;
typedef pair<ll, ll> pii;
typedef pair<ll, float> pif;
#define vec vector
#define mp make_pair
#define sus for (int i = 0; i < 4; ++i) //iteruje susedov
#define inf 1234567890
#define f first
#define s second
#define pi pair<int,int>

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
#define DURATION     10

#define NAME "Found_the_bitches!!"
#define COLOR "#7393B3"

vec<pi> SMER = {{-1,0},{1,0},{0,1},{-1,0}};
int  DX[] = { 0, 1, 0, -1};
int  DY[] = {-1, 0, 1,  0};
char DS[] = {FORWARD,LEFT, RIGHT};

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
bool je_volne(pi pos,vec<vec<int>> &kde = walls) {
	return pos.f >= 0 && pos.f < width && pos.s >= 0 && pos.s < height && !kde[pos.f][pos.s];
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

void print(vec<vec<int>>mapa){
    for(int y = height-1;y>=0;y--){for(int x = width-1;x>=0;x--){
            if(myself.x == x && myself.y == y)cerr<<"X";
            else{
                for(auto p:players)if(p.x == x && p.y ==y ) mapa[x][y] = 9;
                cerr<<mapa[x][y];
            }
        }
        cerr<<endl;
    }
    cerr<<endl;
}

int move_x(int i){
    int direction = get_my_direction();
    return myself.x + myself.speed*DX[(direction+DS[i]+4)%4];
}

int move_y(int i){
    int direction = get_my_direction();
    return myself.y + myself.speed*DY[(direction+DS[i]+4)%4];
}

pi move(pi pos,int i){
    int direction = get_my_direction();
    return {pos.f + DX[(direction+DS[i]+4)%4],pos.s + DY[(direction+DS[i]+4)%4]};
}
/// powerup begin
pii pohyb(pii pos, int i) {// pohyb na zaklade suradnice
	return { pos.first + DX[i],pos.second + DY[i] };
}

int choose_random(vec<pi> results){
    vec<int>mozem;
    for(int i = 0;i<results.size();i++){
        pi kam = move({myself.x,myself.y},results[i].s);
        if(je_volne(kam) && results[i].f >= 300) mozem.push_back(DS[results[i].s]);
    }
    return mozem[rand()%(mozem.size())];
}

int DFS(pi cur, vec<vec<int>>& mozem,int speed_left = myself.speed_reset_time){
    if(mozem[cur.f][cur.s]) return 0;
    int ret = 0;
    mozem[cur.f][cur.s] = 1;
    sus{
        pi pozicia = pohyb(cur,i);
        if(speed_left){
            bool fl = 1;
            for(int j = 0;j<myself.speed-1;j++){
                pozicia = pohyb(pozicia,i);
                if(!je_volne(pozicia, mozem)){fl = 0;break;}
            }
            if(!fl) continue;
            pozicia = pohyb(cur,i);
            for(int j = 0;j<myself.speed-1;j++){
                mozem[pozicia.f][pozicia.s] = 2;
                pozicia = pohyb(pozicia,i);
            }
            ret = max(ret,DFS(pozicia,mozem,max(0,speed_left-1)));
        }else{
            if(je_volne(pozicia)){
                ret = max(ret,DFS(pozicia,mozem,max(0,speed_left-1)));
            }
        }
    }
    return ret+1;
}
int smart_DFS(pi cur, vec<vec<int>>& mozem,int h = 0){
    if(h >= 15) return 1;
    if(mozem[cur.f][cur.s]) return 0;
    int ret = 0;
    mozem[cur.f][cur.s] = 1;
    sus{
        pi pozicia = pohyb(cur,i);
        if(je_volne(pozicia,mozem)){
            ret = max(ret,DFS(pozicia,mozem, h+1) + 1);
        }
    }
    mozem[cur.f][cur.s] = 0;
    return ret;
}

int size_of_component(pi cur, vec<vec<int>> mozem){ //faking nefung
    int ans = 0;
    queue<pi> q;
    q.push(cur);
    while(!q.empty()){
        pi nv = q.front();q.pop();
        if(!je_volne(nv,mozem)) continue;
        mozem[nv.f][nv.s] = 1;
        ans++;
        for(auto smer : SMER){
            pi kam = {nv.f + smer.f,nv.s+smer.s};
            if(!je_volne(kam,mozem)) q.push(kam);
        } 
    }
    return ans;
}
void zapis_suseda(pii pos, int h, vec<vec<int>>& new_walls,int speed) {
    if (h == 0)return;
    if (!je_volne(pos, new_walls)) {
        return;
    }
    new_walls[pos.f][pos.s] = 1;
    //print(new_walls);
    sus{
        pi kam = pos;
        kam = pohyb(kam, i);
        For(j, 0, speed - 1) {
            if (je_volne(kam)) new_walls[kam.f][kam.s] = 2;
            kam = pohyb(kam, i);
        }
        zapis_suseda(kam, h - 1, new_walls,speed);
    }
    return;
}
int dfs_na_komponenty(pii pos, vec<vec<int>> &new_walls) {
    if (new_walls[pos.f][pos.s]) return 0;
    new_walls[pos.f][pos.s] = 1;
    int vys = 1;
    sus{
        pii kam = pohyb(pos, i);
        if(je_volne(kam, new_walls))
            vys+= dfs_na_komponenty(kam, new_walls);
    }
    return vys;
}

int velkost_komponentu(pii pos) {
    vec<vec<int>> new_walls;
    for(auto i: walls) new_walls.push_back(i);
    new_walls[pos.f][pos.s] = 0;
    int vys = dfs_na_komponenty(pos, new_walls);
    new_walls[pos.f][pos.s] = 1;
    return vys;
}


int max_velkosti_ostatnych() {
    int vys = 0;
    for (auto player : players)if(player.alive){
        vys = max(vys, velkost_komponentu(mp(player.x, player.y)));
    }
    return vys;
}
bool powerup_blyzko(pii pos) {
    for (auto i : powerups) {
        if (abs(i.x - pos.first) + abs(i.y - pos.s) == 1)
            return true;
    }
    return false;
}
// sem pis svoj kod
Command do_turn(){
    //myself.speed_reset_time = 10;
    //myself.speed = 2;
	pi pos = {myself.x,myself.y};
	Command cmd;
    cmd.direction = DS[0];
    cmd.use_powerup = 0;
	// ak mam powerup pouzijem ho
	if (myself.powerup == SPEED_OTHERS) cmd.use_powerup = true;
	// vyskusam pohyb vsetkymi moznymi smermi
    if(myself.speed == 0){
        cmd.direction = FORWARD;
        return cmd;
    }
    int most_free;
        for(int hlbka_buducnosti = 8; hlbka_buducnosti >= 0; hlbka_buducnosti--){
        most_free = 0;
        vec<pi> results;
        for (int i = 0; i < 3; ++i) {
            vec<vec<int>> new_walls;
            for (auto i : walls) {
                new_walls.push_back(i);
            }
            for (auto player : players) {
                sus{
                    pi kam = pohyb({player.x,player.y},i);
                    zapis_suseda(kam, hlbka_buducnosti, new_walls,player.speed);
                }
            }
            pi nv_pos = pos;
            // zratam potencionalnu polohu
            bool fl = 0;
            for (int j = 0; j < myself.speed; j++) {
                new_walls[nv_pos.f][nv_pos.s] = 2;
                nv_pos = move(nv_pos, i);
                if (!je_volne(nv_pos, new_walls)) { fl = 1; break; }
            }
            if (fl) continue;
            //print(new_walls);
            // skontrolujem ci je volne
            if (je_volne(nv_pos, new_walls)) {
                //cerr<<"bfs "<<size_of_component(nv_pos,new_walls)<<endl;
                int nv = DFS(nv_pos, new_walls);
                //print(new_walls);
                results.push_back({ nv,i });
                //cerr << "dfs " << nv << " " << i << endl;
                if (nv > most_free) {
                    cmd.direction = DS[i];
                    most_free = nv;
                }
            }
        }
        if (most_free > width*height/(4+hlbka_buducnosti)) {
            break;
        }
    }
    if(most_free == 0) cmd.direction = inf;
    bool chcem = (1.3*velkost_komponentu(mp(myself.x, myself.y)) < max_velkosti_ostatnych());
    if(myself.powerup == STOP_ME && velkost_komponentu({myself.x,myself.y}) <= 100){cmd.use_powerup = 1;}
    if(most_free <= 1 && myself.powerup == CLEAN)cmd.use_powerup = 1;
    if(myself.powerup == CLEAN && chcem && powerup_blyzko(mp(myself.x, myself.y)))cmd.use_powerup = 1;
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
}
//ked som v malom komponente, tak po sebe mozem mazat mozem[][]
//nezrazat sa s ostatnymi, nechces mat artikulacie pri ostatnych
//predpovedanie buducnosti nakonstantit
//zlepsit clear
//DFS double speed robi hovadiny

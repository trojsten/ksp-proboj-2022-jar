#include "common.h"
#include "queue"
#include <chrono>
#include <thread>


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

#define log std::cerr <<
#define nl  << std::endl;

#define NAME "Pterodactyl"
#define COLOR "#0061ED"

int DX[] = {0, 1, 0, -1};
int DY[] = {-1, 0, 1, 0};
char DS[] = {LEFT, FORWARD, RIGHT};

int width, height;
Player myself;
std::vector<std::vector<int>> walls;
std::vector<PowerUp> powerups;
std::vector<Player> players;

// vrati smer ktorym sme prave otoceny
int get_my_direction() {
    for (int i = 0; i < 4; ++i)
        if (myself.dx == DX[i] && myself.dy == DY[i])
            return i;
    return -1;
}


// skontrolujem ci sa pozeram do pola a ci je v nom 0
bool is_free(int x, int y) {
    if (x >= 0 && x < width && y >= 0 && y < height && !walls[x][y]) {
        return true;
    } else { return false; }
}

bool is_free_no_walls(int x, int y) {
    if (x >= 0 && x < width && y >= 0 && y < height) {
        return true;
    } else { return false; }
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
    Command cmd{};
    // ak mam powerup pouzijem ho
    if (myself.powerup != SPEED_ME && myself.powerup != NO_POWERUP) cmd.use_powerup = true;

    // vyskusam pohyb vsetkymi moznymi smermi

    int grid[8][2];
    grid[0][0] = -1; grid[0][1] = 0;
    grid[3][0] = 0; grid[3][1] = -1;
    grid[4][0] = 0; grid[4][1] = 1;
    grid[5][0] = 1; grid[5][1] = 0;

    log "entering algorithm" nl;
    int glob_max = -2;
    std::pair<int, int> glob_max_loc = {-1, -1};
    std::queue<std::vector<int>> queue;
    std::vector<int> loc{myself.x, myself.y, get_my_direction(), 0};
    queue.push(loc);
    std::vector<std::vector<int>> visited(walls.size(), std::vector<int>(walls[0].size(), -1));
    visited[myself.x][myself.y] = 0;
    while (!queue.empty()) {
        log "skusam smery" nl;
        for (char j: DS) {
            log "jeden smer" nl;
            int current_dir = (queue.front()[2] + j + 4) % 4;
            x = queue.front()[0] + DX[current_dir];
            y = queue.front()[1] + DY[current_dir];
            if (is_free(x, y) && visited[x][y] == -1) {
                loc[0] = x;
                loc[1] = y;
                loc[2] = current_dir;
                loc[3] = queue.front()[3] + 1;
                queue.push(loc);
                visited[x][y] = queue.front()[3] + 1;
                if (glob_max < loc[3]) {
                    glob_max = loc[3];
                    glob_max_loc = { loc[0], loc[1] };
                }
            }
        }
        queue.pop();
    }

    log "idem do gridu" nl;
    while (glob_max != 1) {
        for (auto block : grid) {
            if (is_free(glob_max_loc.first + block[0], glob_max_loc.second + block[1]) && visited[glob_max_loc.first + block[0]][glob_max_loc.second + block[1]] == glob_max - 1) {
                glob_max--;
                glob_max_loc = { glob_max_loc.first + block[0],  glob_max_loc.second + block[1]};
            }
        }
    }

    log "idem dir" nl;
    char final_dir = FORWARD;
    if (myself.x + myself.dx == glob_max_loc.first && myself.y + myself.dy == glob_max_loc.second) {
        final_dir = FORWARD;
    } else if (myself.x - myself.dy == glob_max_loc.first && myself.y + myself.dx == glob_max_loc.second) {
        final_dir = RIGHT;
    } else if (myself.x + myself.dy == glob_max_loc.first && myself.y - myself.dx == glob_max_loc.second) {
        final_dir = LEFT;
    }

    log "Idem " << (int) final_dir << "lebo mozem a je to vyhodne: " << glob_max nl;
    cmd.direction = final_dir;
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
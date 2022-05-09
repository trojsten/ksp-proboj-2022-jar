#include "common.h"

#include <queue>
#include <math.h>

template <class T>
std::ostream &operator<<(std::ostream &out, std::vector<T> &v)
{
	for (auto it = v.begin(); it != v.end(); ++it)
	{
		if (it == v.begin())
			out << *it;
		else
			out << " " << *it;
	}
	out << "\n";
	return out;
}

// pohyb
#define LEFT -1
#define RIGHT 1
#define FORWARD 0

// powerupy Player.powerup
#define NO_POWERUP 0
#define SPEED_ME 1
#define SPEED_OTHERS 2
#define STOP_ME 3
#define STOP_OTHERS 4
#define CLEAN 5

#define NAME "bulsit"
#define COLOR "#ad01ff"

int DX[] = {0, 1, 0, -1};
int DY[] = {-1, 0, 1, 0};
char DS[] = {LEFT, FORWARD, RIGHT};

int width, height;
Player myself;
std::vector<std::vector<int>> walls;
std::vector<PowerUp> powerups;
std::vector<Player> players;

int get_direction(Player p)
{
	for (int i = 0; i < 4; ++i)
		if (p.dx == DX[i] && p.dy == DY[i])
			return i;
	return 0;
}

// vrati smer ktorym sme prave otoceny
int get_my_direction()
{
	return get_direction(myself);
}

struct Point
{
	int x, y;

	Point move(int direction, int distance)
	{
		int nx = x + DX[direction] * distance;
		int ny = y + DY[direction] * distance;
		return {nx, ny};
	}
};

// skontrolujem ci sa pozeram do pola a ci je v nom 0
bool is_free(Point p)
{
	return p.x >= 0 && p.x < width && p.y >= 0 && p.y < height && !walls[p.x][p.y];
}

void read_state()
{
	update(walls);
	update(myself);
	update(players);
	update(powerups);

	end_communication();
	width = walls.size();
	height = walls[0].size();
}

typedef std::vector<std::vector<std::vector<int>>> vec3d;

int turn(int direction, int diff)
{
	return (direction + diff + 4) % 4;
}

void bfs(Point p, int direction, int step, vec3d &dist)
{
	std::queue<std::pair<Point, int>> Q;
	dist[p.x][p.y][direction] = 0;
	Q.push({p, direction});
	while (Q.size())
	{
		auto next = Q.front();
		Q.pop();
		Point cur_p = next.first;
		int cur_dir = next.second;
		for (int i = -1; i <= 1; i++)
		{
			int new_dir = turn(cur_dir, i);
			bool can_move = true;
			for (int s = 1; s <= step; s++)
			{
				if (!is_free(cur_p.move(new_dir, s)))
				{
					can_move = false;
					break;
				}
			}
			if (!can_move)
				continue;

			Point new_p = cur_p.move(new_dir, step);
			if (dist[new_p.x][new_p.y][new_dir] == INT32_MAX)
			{
				dist[new_p.x][new_p.y][new_dir] = dist[cur_p.x][cur_p.y][cur_dir] + 1;
				Q.push({new_p, new_dir});
			}
		}
	}
}

int pathfind(Point to, int direction, vec3d &dist, int step)
{
	int move_to;
	while (dist[to.x][to.y][direction] > 0)
	{
		if (dist[to.x][to.y][direction] == 1)
			move_to = direction;

		Point new_to = to.move((direction + 2) % 4, step);
		for (int i = -1; i <= 1; i++)
		{
			if (dist[new_to.x][new_to.y][(direction + 4 + i) % 4] < dist[to.x][to.y][direction])
			{
				direction = (direction + 4 + i) % 4;
				to = new_to;
				break;
			}
		}
	}
	std::cerr << move_to << std::endl;

	return (move_to - direction + 5) % 4 - 1;
}

std::pair<Point, int> closest_powerup(vec3d &dists, int speed)
{
	int best_dist = INT32_MAX;
	std::pair<Point, int> best = {{-1, -1}, -1};
	for (auto pu : powerups)
	{
		Point pu_pos = {pu.x, pu.y};
		for (int i = 0; i < 4; i++)
		{
			for (int over = 0; over < speed; over++)
			{
				Point turn_end = pu_pos.move(i, over);
				if (!is_free(turn_end))
					continue;
				if (dists[turn_end.x][turn_end.y][i] < best_dist)
				{
					best_dist = dists[turn_end.x][turn_end.y][i];
					best.first = turn_end;
					best.second = i;
				}
			}
		}
	}
	return best;
}

int closest_powerup_distance(vec3d &dists, int speed)
{
	auto closest = closest_powerup(dists, speed);
	if (closest.second == -1)
		return INT32_MAX;
	return dists[closest.first.x][closest.first.y][closest.second];
}

int pathfind_to_powerup(vec3d &dists, int speed)
{
	auto closest = closest_powerup(dists, speed);
	if (closest.second == -1)
		return -1;
	return pathfind(closest.first, closest.second, dists, speed);
}

struct ComponentStats
{
	int cells;
	int players;
	int powerups;

	int quality()
	{
		return (cells + 2 * powerups) / (1 + 3 * players);
	}
};

ComponentStats get_component_stats(Point p)
{
	std::vector<std::vector<int>> visited(width, std::vector<int>(height));
	std::queue<Point> Q;
	Q.push(p);
	visited[p.x][p.y] = 1;
	ComponentStats result = {0, 0, 0};
	std::cerr << p.x << " " << p.y << std::endl;
	while (Q.size())
	{
		Point cp = Q.front();
		Q.pop();
		for (int i = 0; i < 4; i++)
		{
			Point np = cp.move(i, 1);
			if (is_free(np) && !visited[np.x][np.y])
			{
				visited[np.x][np.y] = 1;
				Q.push(np);
				result.cells++;
			}
		}
	}
	std::cerr << powerups.size() << std::endl;
	for (PowerUp pu : powerups)
	{
		std::cerr << pu.x << " " << pu.y << std::endl;
		if (visited[pu.x][pu.y])
			result.powerups++;
	}
	for (Player pl : players)
	{
		if (!pl.alive)
			continue;
		Point pl_pos = {pl.x, pl.y};
		for (int i = -1; i <= 1; i++)
		{
			int d = turn(get_direction(pl), i);
			Point potential_move = pl_pos.move(d, pl.speed);
			std::cerr << potential_move.x << " " << potential_move.y << std::endl;
			bool can_move = true;
			for (int s = 1; s <= pl.speed; s++)
			{
				if (!is_free(pl_pos.move(d, s)))
					can_move = false;
			}
			std::cerr << can_move << std::endl;
			if (can_move && visited[potential_move.x][potential_move.y])
				result.players++;
		}
	}
	return result;
}

bool should_use_powerup(int powerup)
{
	return powerup == STOP_ME || powerup == STOP_OTHERS || powerup == SPEED_OTHERS;
}

bool is_alone(Player &p)
{
	ComponentStats cs = get_component_stats({p.x, p.y});
	return cs.players == 0;
}

bool should_use_powerup(std::vector<int> &dir_score, vec3d &dists, vec3d &dists_speed)
{
	if (myself.powerup == NO_POWERUP)
		return false;
	if (myself.powerup == SPEED_ME)
	{
		if (get_component_stats({myself.x, myself.y}).players == 0)
			return false;
		auto closest_pu = closest_powerup_distance(dists, myself.speed);
		auto closest_pu_speed = closest_powerup_distance(dists_speed, myself.speed * 2);
		return closest_pu_speed < std::min(10, closest_pu);
	}
	if (myself.powerup == SPEED_OTHERS || myself.powerup == STOP_ME)
		return get_component_stats({myself.x, myself.y}).players == 0;
	if (myself.powerup == STOP_OTHERS)
		return get_component_stats({myself.x, myself.y}).players > 0;
	if (myself.powerup == CLEAN)
	{
		for (int i = 0; i < 3; i++)
			if (dir_score[i])
				return false;
		return true;
	}
	return false;
}

bool should_keep_powerup(std::vector<int> &dir_score, vec3d &dists, vec3d &dists_speed)
{
	return !should_use_powerup(dir_score, dists, dists_speed) && myself.powerup == CLEAN;
}

// sem pis svoj kod
Command do_turn()
{
	Command cmd;
	int direction = get_my_direction();
	Point pos = {myself.x, myself.y};

	vec3d dists(width, std::vector<std::vector<int>>(height, std::vector<int>(4, INT32_MAX)));
	vec3d dists_speed(width, std::vector<std::vector<int>>(height, std::vector<int>(4, INT32_MAX)));

	bfs(pos, direction, myself.speed, dists);
	bfs(pos, direction, myself.speed * 2, dists_speed);

	std::vector<int> dir_score(3);
	for (int i = -1; i <= 1; i++)
	{
		Point potential_move = pos.move(turn(direction, i), myself.speed);
		if (is_free(potential_move))
			dir_score[i + 1] += get_component_stats(potential_move).quality();
	}

	if (should_use_powerup(dir_score, dists, dists_speed))
		cmd.use_powerup = true;

	// apply to powerup bonuses
	int to_powerup = -1;
	if (!should_keep_powerup(dir_score, dists, dists_speed))
	{
		if (cmd.use_powerup && myself.powerup == SPEED_ME)
			to_powerup = pathfind_to_powerup(dists_speed, myself.speed * 2);
		else
			to_powerup = pathfind_to_powerup(dists, myself.speed);
		dir_score[to_powerup + 1] += 10;
	}

	int best_score = 0;
	for (int i = -1; i <= 1; i++)
	{
		if (dir_score[i + 1] >= best_score)
		{
			cmd.direction = i;
			best_score = dir_score[i + 1];
		}
	}

	// std::vector<int> wtf(1000);
	// for (int i = -1; i <= 1; i++)
	// {
	// 	int d = (direction + i + 4) % 4;
	// 	if (is_free(pos.move(d, 1)))
	// 	{
	// 		cmd.direction = i;
	// 	}
	// }
	return cmd;
}

int main()
{
	// aby sme mali nahodu
	srand(time(0));
	// povieme serveru ako sa chceme volat a farbu
	greet_server(NAME, COLOR);
	// robime tahy kym sme zivy
	myself.alive = true;
	while (myself.alive)
	{
		read_state();
		send_command(do_turn());
	}
	std::cout << "Bye\n";
}

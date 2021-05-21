#include <bits/stdc++.h>
using namespace std;

#define MAXTIME 1000

vector<flow> elephants;

int bigrand()
{
	return rand() * 32768 + rand();
}

int randint(int l, int r)
{
	return l + bigrand() % (r - l + 1);
}

int getflowlen()
{
	int t = bigrand() / 1073741824.0;
	if (t < 0.15)
		return randint(1, 10000) / 1460 + 1;
	if (t < 0.2)
		return randint(10000, 20000) / 1460 + 1;
	if (t < 0.3)
		return randint(20000, 30000) / 1460 + 1;
	if (t < 0.4)
		return randint(30000, 50000) / 1460 + 1;
	if (t < 0.53)
		return randint(50000, 80000) / 1460 + 1;
	if (t < 0.6)
		return randint(80000, 200000) / 1460 + 1;
	if (t < 0.7)
		return randint(200000, 1000000) / 1460 + 1;
	if (t < 0.8)
		return randint(100000, 2000000) / 1460 + 1;
	if (t < 0.9)
		return randint(200000, 5000000) / 1460 + 1;
	if (t < 0.97)
		return randint(500000, 10000000) / 1460 + 1;
	return randint(1000000, 30000000) / 1460 + 1;
}

int getflowport()
{
	map<long long, bool> mp;
	
}

void send_request(int client)
{
	for (int i = 1; i <= 200 - bigrand() % 50 + bigrand() % 150; ++i)
	{
		// send a request to a server randomly
		int server = client;
		while (server == client)
			server = randint(1, 8);
		flows[server].push(new flow(client, getflowport(), getflowlen(), 0));
	}
}

void send_msg(int server)
{

}

int main()
{
	for (int time = 1; time <= MAXTIME; ++time) // time
	{
		for (int client = 1; client <= 8; client++)
		{
			send_request(client);
		}
		for (int server = 1; server <= 8; server++)
		{
			send_msg(server);
		}
	}
}

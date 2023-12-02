#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

class Trial {
  public:
    Trial(string s);
   
    int red;
    int green;
    int blue;
  private:
    void parse(string s);
};

class Game {
  public:
    Game(string s);
    bool isValid(); // <=12 red, 13 green, 14 blue
    int power();    // product of minimum red, green, and blue required
    
    int id;
    vector<Trial> t;

};

Game::Game(string s) {
    int pos = s.find(": ");
    id = stoi(s.substr(0, pos).substr(5,3));
    s.erase(0, pos+2);

    while((pos = s.find("; ")) != string::npos) {
        t.push_back(Trial(s.substr(0, pos)));
        s.erase(0, pos+2);
    }
    t.push_back(s);
}

bool Game::isValid() {
    for(Trial &tt : t) {
        if(tt.red > 12 || tt.green > 13 || tt.blue > 14)
            return false;
    }
    return true;
}

int Game::power() {
    int red = 0, green = 0, blue = 0;

    for(Trial &tt : t) {
        if(tt.red > red)
            red = tt.red;
        if(tt.green > green)
            green = tt.green;
        if(tt.blue > blue)
            blue = tt.blue;
    }
    return(red * green * blue);
}

Trial::Trial(string s) {
    red = green = blue = 0;
    int pos;
    while((pos = s.find(", ")) != string::npos) {
        parse(s.substr(0, pos));
        s.erase(0, pos+2);
    }
    parse(s);
}

void Trial::parse(string s) {
    int pos = s.find(" ");
    int val = stoi(s.substr(0, pos));
    if(s.find("red") != string::npos) {
        red = val;
    } else if(s.find("green") != string::npos) {
        green = val;
    } else if(s.find("blue") != string::npos) {
        blue = val;
    }
}

int main() {
    ifstream input;
    string line;
    input.open("inputs/2");
    int part1 = 0, part2 = 0;
    while(getline(input, line)) {
        Game g = Game(line);
        if(g.isValid()) 
            part1 += g.id;
        part2 += g.power();
    }
    cout << "Part1: " << part1 << "\n" << "Part2: " << part2 << endl;
    input.close();
    return 0;
}

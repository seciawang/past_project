#include<iostream>
#include<vector>
#include<string>
#include<windows.h>
#include<ctime>
#include<sstream>
#include<cstdlib>
#include<conio.h>
#pragma comment(lib, "winmm.lib")
#define skip << endl
#define skipm << "@"
#define atkstat 0
#define hpstat 1
#define mpstat 2
#define critstat 3
#define defstat 4
#define cls << "   "
#define range(n1,n2) n1 + rand()%(n2-n1+1)
#define iflvl(n,k) if(lvl==n){sp+=k;}
#define iflvlbelow(n,k) if(lvl<=n) {sp+=k;}
#define LVL_REQUIRED(n) lvl_requirementSkill.push_back(n);
#define ADD_FORBIDDEN(n1,n2) x_forbidden.push_back(n1); y_forbidden.push_back(n2);
#define COORDINATE_MAP 4, 25
#define PLAYER_COORDINATE(xx1, yy1) (getpx()==xx1 && getpy()==yy1)
#define DIALOGUE_MAP(astring, decision, thedelay) advancedMsg(astring, COORDINATE_MAP , '|', decision, thedelay);
#define PLAYER_NAMETAG "["+player->getName()+"]@"
#define BATTLE_DIALOGUE(astring, decision, thedelay )advancedMsg(astring, 4, 27, '+', decision, thedelay);
#define CHECK_GAMEOVER  if(player->getHp()<=0){clearMsg();printEntity();printStatus(player);BATTLE_DIALOGUE("[@   GAME OVER!!!   ",true, 20);exit(0);}
#define SHOW_FULL_UI clearMsg(); printEntity(); printStatus(player);
#define EXPERIENCE(val1, val2, val3, val4) val1 + val2 * (lvlT - val3 + val4)
#define RED 0x0C
#define PURPLE 0x0D

#define WINVER 0x0500
#include <windows.h>

 

//#define TEXT_COLOR(color) setColor(color)

//#define YELLOW
//#define TEXT(a) 
//#define DIALOGUE_MAP(speaker, astring) advancedMsg("[" + speaker + "]" + "@" + astring, COORDINATE_MAP , '|', true, 40);
int floor_progress=1;
/*
//Archieve--------
musicLoop
musicLoop2
atkNormal
atkCritical
atkPlayerNormal
atkPlayerCritical
getItem
sfxwalk
//Archive---------
*/

/*
What we need:
Sound for every skill
startBattle
startBossBattle
navigate (picking up and down)
runSfx



*/

using namespace std;

int BoundaryOfRealityX = 4;
int BoundaryOfDreamY = 2;

void gotoxy(int x, int y){
 COORD k = {x*BoundaryOfRealityX,y*BoundaryOfDreamY};
 SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), k);
}

void gotoxyreal(int x, int y){
COORD k = {x,y};
SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), k);
}

void setColor(WORD w){
	SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), w);
}

void showPixelArt(string pixel[15], int coord_x, int coord_y, int delay=200){
	
	for(int ix=0; ix<15; ix++){
		gotoxyreal(coord_x, coord_y);
		cout << pixel[ix];
		coord_y++;
	}
	
	Sleep(delay);
}

char capital(char letter){
	if(letter>='a' && letter<='z')
		letter = 'A' + (letter-'a');
}

void createWall(int x1, int x2, int y1, int y2, int mode, char wall='#'){
	
	if(mode==1){
		x1*=BoundaryOfRealityX;
		x2*=BoundaryOfRealityX;
		y1*=BoundaryOfDreamY;
		y2*=BoundaryOfDreamY;
	}
	
	for(int j=y1; j<=y2; j++){
		for(int i=x1; i<=x2; i++){
			if(j==y1 || j==y2 || i==x1 || i==x2){
				gotoxyreal(i,j);
				cout << wall;
			}
		}
	}
}

void clearArea(int x1, int x2, int y1, int y2, int mode){
	
	if(mode==1){
		x1*=BoundaryOfRealityX;
		x2*=BoundaryOfRealityX;
		y1*=BoundaryOfDreamY;
		y2*=BoundaryOfDreamY;
	}
	
	for(int j=y1; j<=y2; j++){
		for(int i=x1; i<=x2; i++){
				gotoxyreal(i,j);
				cout << ' ';
		}
	}
}

void hold(){
	char exit_button='x';
	do{
		exit_button=getch();
	}while(exit_button!=13);
}

void msg(string sentence, int iid){
	
	int line=1;
	int xline=0;
	
	if(iid==1){
		xline=18;
		line=2;
	}
	else
		xline=12;
	
	gotoxy(xline,line);
	
	if(sentence=="clear"){
		for(int i=0; i<5; i++){
			gotoxy(12,i);
			cout << "                                           ";
		}
		return;
	}
	
	int sentence_length = sentence.length();
	
	for(int i=0; i<sentence_length; i++){
	if(sentence[i]=='@'){
		line++;
		gotoxy(xline,line);
	}
	else
		cout << sentence[i];
	}
}

void clearMsg(){
	system("cls");
}

void advancedMsg(string sentence, int xstart, int ystart, char wall, bool dialogue=false, int delay=50){
	
	int xend=xstart;
	int yend=ystart;
	int xtemp=xstart;
	int ynow=ystart;
	
	int sentence_length = sentence.length();
	
	for(int i=0; i<sentence_length; i++){
		if(sentence[i]=='@' || i==sentence.length()-1){
			yend++;
			if(xtemp>xend)
				xend = xtemp;
			xtemp=xstart;
		}else{
			xtemp++;
		}
	}
	
	ystart = ystart - 2;
	yend = yend + 2;
	xstart = xstart - 2;
	xend = xend + 2;
	
	for(int j=ystart; j<=yend; j++){
		for(int i=xstart; i<=xend; i++){
			if(i==xstart || i==xend || j==ystart || j==yend){
				gotoxyreal(i,j);
				cout << wall;
			}
		}
	}
	
	for(int j=ystart+1; j<=yend-1; j++){
		for(int i=xstart+1; i<=xend-1; i++){
				gotoxyreal(i,j);
				cout << ' ';
		}
	}
	
	ystart = ystart + 2;
	yend = yend - 2;
	xstart = xstart + 2;
	xend = xend - 2;
	gotoxyreal(xstart, ynow);
	
	for(int i=0; i<sentence_length; i++){
		if(sentence[i]=='@'){
			ynow++;
			gotoxyreal(xstart, ynow);
		}else{
			cout << sentence[i];
			if(dialogue)
				Sleep(delay);
		}
	}
	
	ynow = ystart;
	
	if(dialogue){
		
		hold();
		mciSendString("play progress_dialogue.wav", NULL, 0, NULL);

		
		for(int j=ystart-2; j<=yend+2; j++){
		for(int i=xstart-2; i<=xend+2; i++){
				gotoxyreal(i,j);
				cout << ' ';
		}
		}
	}
		
}


void damagedScreen(bool critical){
	
	int x;
	int y;
	//setColor(0x4F);
	setColor(0x0C);
	
	if(!critical){
		setColor(0x0C);
		for(int i=0; i<150; i++){
			x=rand()%35;
			y=rand()%50;
			gotoxyreal(x,y);
			Sleep(1);	
		}
	}
	else{
		setColor(0x4F);
		for(int i=0; i<150; i++){
			x=rand()%100;
			y=rand()%100;
			gotoxyreal(x,y);
			Sleep(1);	
		}
	}
	setColor(RED);
}

class Skill{
private:
	string name;
	int dmg;
	int status;
	int chance;
	int mp;
	int turn;
	float min_multiplier;
	float max_multiplier;
	string sound_file;
	
	
public:
	
	Skill(string name, int dmg, int status, int chance, int mp, float min_multiplier, float max_multiplier, string sound_file,int turn){
		this->name = name;
		this->dmg = dmg;
		this->status = status;
		this->chance = chance;
		this->mp = mp;
		this->min_multiplier = min_multiplier;
		this->max_multiplier = max_multiplier;
		this->sound_file = sound_file;
		this->turn = turn;
		//sound+=".wav";
		//cout << sounds skip;
		/*string lol=sounds;
		LPCSTR a=lol.c_str();
		PlaySound(a, GetModuleHandle(NULL), SND_FILENAME | SND_ASYNC);
		this->sound_file = a;
		cout << a << " &&& " << sound_file skip;*/
	}
	
	string getName(){
		return name;
	}
	
	int getStatus(){
		return this->status;
	}
	
	int getChance(){
		return this->chance;
	}
	
	int getTurn(){
		return this->turn;
	}
	
	int getMp(){
		return mp;
	}
	
	template<class T>
	void cast(T *target, int atk, int mp_caster){
		int product=range((int)(min_multiplier*10), (int)(max_multiplier*10));
		float dmgMultiplier = (float)product / 10;
		int statusChance=rand()%100 + 1;
		if(status!=0 && statusChance<=chance){
			target->addStat(status);
			target->addTurn(turn);
		}
		int dmgDealt = (float)dmg + ((float)atk*dmgMultiplier*(float)(100-target->getDef())/100.0) + ((float)dmg*(float)mp_caster*0.8/100.0);
		
		if(min_multiplier==0 && max_multiplier==0)
			dmgDealt=0;
		
		target->setHp(target->getHp()-dmgDealt);
		if(target->getHp()<0){
			target->setHp(0);
		}
		
		stringstream ss;
		ss << dmgDealt;
		string str = ss.str();
		
		string sentence;
		if(target->getId()!=0){
			sentence="Player ";
			sentence+="USED ";
		}
		else{
			sentence="Enemy ";
			sentence+="CASTED ";
		}
		
		//+getName()+"@Dealt "+dmgDealt+" damage!";
		//sentence+=getName() + "@Dealt" + dmgDealt + "damage!";
		sentence+=getName();
		sentence+="!!@Dealt ";
		sentence+=str;
		sentence+=" damage!";
		
		string sound_file_real;
		sound_file_real = "play " + sound_file + ".wav";
		
		LPCSTR file = sound_file_real.c_str();
		mciSendString(file, NULL, 0, NULL);
		//PlaySound(file, GetModuleHandle(NULL), SND_FILENAME | SND_ASYNC);
		BATTLE_DIALOGUE(sentence, false, 0);
		//msg(sentence, 1);
	}
	 
	
};

class Monster{
protected:
	int atk;
	int maxHp;
	int hp;
	int def;
	int lvl;
	vector<int> stat;
	vector<int> turn;
	int gold;
	int critical_chance;
	int expGet;
	bool para;
	int id; //0 = player
			//1 = monster
			//2 = boss
			//3 = vampire passive:-> lifesteal (hp+ ketika atk)
			//4 = berserker -> hp- dmg+ fixed every turn tergantung floor @ battleSequence
			//5 = zombie -> poison% @
			//6 = dragon -> burn
			//7 = sandman -> crit and acc player -%
			//8 = axeman -> stat: hi dmg low hp
			//9 = pikachu -> paralyzed chance%
			//10 = rabbit chest -> hold chest, do nothing, has huge gold
public:
	
	int getExpGet(){
		return this->expGet;
	}
	
	void addTurn(int turn){
		this->turn.push_back(turn);
	}
	
	void setAtk(int atk){
		this->atk=atk;
	}
	int getAtk(){
		return this->atk;
	}
	
	void setHp(int hp){
		this->hp=hp;
	}
	int getHp(){
		return this->hp;
	}
	
	void setMaxHp(int maxHp){
		this->maxHp = maxHp;
	}
	
	int getMaxHp(){
		return this->maxHp;
	}

	void setDef(int def){
		this->def=def;
	}
	int getDef(){
		return this->def;
	}

	void addStat(int status){
		stat.push_back(status);
	}
	void delStat(int status){
		stat.erase(stat.begin()+status);
	}
	
	bool getPara(){
		return this->para;
	}
	
	void clearStatus(){
		stat.clear();
		turn.clear();
	}
	
	void checkStatus(){
		int size;
		size = stat.size();
		//1 : Burn
		//2 : Poison
		//3 : para
		para = false;
		stringstream sentence;
		int dmgDealt;
		
		for(int i=0;i<size;i++){
			if(stat[i]==1){
				dmgDealt = ((float)hp*20/100);
				if(id==0){		
					sentence << "You smelled something burning *sniff *sniff   " skipm;
					sentence << "your health burned by " << dmgDealt;
				}else{
					sentence << "That monster IS ON FIRE!!!       " skipm;
					sentence << "monster takes " << dmgDealt << " damages!";
				}
				hp -= dmgDealt;
				BATTLE_DIALOGUE(sentence.str(),true, 10);
			}
			else if(stat[i]==2){
				dmgDealt = ((float)hp*15/100);
				if(id==0){		
					sentence << "You have been poisoned           " skipm;
					sentence << "your took " << dmgDealt;
				}else{
					sentence << "That monster have been poisoned!!" skipm;
					sentence << "monster takes " << dmgDealt << " damages!";
				}
				hp -= dmgDealt;
				BATTLE_DIALOGUE(sentence.str(),true, 10);
			}
			else if(stat[i]==3)
			{
				para = true;
				if(id==0){		
					sentence << "bzzzzzzzzzztt..... " skipm;
					sentence << "your unable to move" << dmgDealt;
				}else{
					sentence << "BZZZZzzt.....               " skipm;
					sentence << "The monster stop moving     ";
				}
				BATTLE_DIALOGUE(sentence.str(),true, 10);
				
			}
			turn[i]-=1;
			if(turn[i]==0){
				delStat(i);
				turn.erase(turn.begin()+i);
				size--;
				i--;
			}
			
		}	
	}
	
	void setGold(int gold){
		this->gold=gold;
	}
	int getGold(){
		return this->gold;
	}
	
	void setLvl(int lvl){
		this->lvl = lvl;
	}
	int getLvl(){
		return this->lvl;
	}
	
	int getId(){
		return this->id;
	}
	
	int getCritical_chance(){
		return this->critical_chance;
	}
	
	void setCritical_chance(int critical_chance){
		this->critical_chance = critical_chance;
	}
	
	template<class T>
	void attack(T *target){
		
		string sentence;
		int chance=rand()%100+1;
		int bonus_damage=rand()%(lvl*2);
		int damage=this->atk;
		
		if(chance<=critical_chance){
			damage=(int)((float)damage*1.42);
			if(this->id==0)		
				sentence="CRITICAL HIT!!                 ";
			else if(this->id==1)
				sentence="Monster did a CRITICAL!!       ";
			else if(this->id==3)
				sentence="VAMPRICAL ATTACK!              ";
			else if(this->id==4)
				sentence="HEAVY CRITICAL FIST!           ";
		}else{
			if(this->id==0)
				sentence="You hit the monster!           ";			
			else if(this->id==1)
				sentence="Monster severly hurt you!      ";	
			else if(this->id==3)
				sentence="Vampire attacks you!           ";
			else if(this->id==4)
				sentence="Berserker attack with his fury!";	
		}
			
		damage+=bonus_damage;
		damage-=target->getDef();
		if(damage<=0)
			damage=1;
			
		target->setHp(target->getHp()-damage);
		if(target->getHp()<0)
			target->setHp(0);
		
		stringstream ss;
		ss << damage;
		string str = ss.str();
		
		//+getName()+"@Dealt "+dmgDealt+" damage!";
		//sentence+=getName() + "@Dealt" + dmgDealt + "damage!";
		sentence+="@Dealt ";
		sentence+=str;
		sentence+=" damage!";
		advancedMsg(sentence, 4, 27, '+', false, 35);
		//msg(sentence, 1);
		if(this->id!=0){
		if(chance<=critical_chance){
			PlaySound(TEXT("atkCritical.wav"), NULL, SND_FILENAME | SND_ASYNC);
			//damagedScreen(true);
		}
		else{
			PlaySound(TEXT("atkNormal.wav"), NULL, SND_FILENAME | SND_ASYNC);
			//damagedScreen(false);	
		}
		}else{
			if(chance<=critical_chance){
			PlaySound(TEXT("atkPlayerCritical.wav"), NULL, SND_FILENAME | SND_ASYNC);
			}
			else{
			PlaySound(TEXT("atkPlayerNormal.wav"), NULL, SND_FILENAME | SND_ASYNC);
			}
		}
		
		
	} 
	
	Monster(int atk, int hp, int def, int lvl, int floor, int critical_chance=10, int gold=100, int expGet=0){
		this->atk=atk;
		this->hp=hp;
		this->maxHp = hp;
		this->def=def;
		this->id = 1;
		
		//int randomlevel=rand()%5;
		//lvl = lvl + 2 - randomlevel;
		
		/*if(lvl<=0)
			this->lvl=1;
		else
			this->lvl = lvl;*/
		
		this->lvl = lvl;	
		this->gold=gold;
		this->critical_chance = critical_chance;
		this->expGet = expGet;
	}
};

class Vampire :public Monster{
protected:
	int lifesteal;
public:
	
	
	int getLifesteal(){
		return this->lifesteal;
	}
	
	template<class T>
	void attack(T *target){
		
		string sentence;
		int chance=rand()%100+1;
		int bonus_damage=rand()%(lvl*2);
		int damage=this->atk;
		
		if(chance<=critical_chance){
			damage=(int)((float)damage*1.42);
			if(this->id==0)		
				sentence="CRITICAL HIT!!                 ";
			else if(this->id==1)
				sentence="Monster did a CRITICAL!!       ";
			else if(this->id==3)
				sentence="VAMPRICAL ATTACK!              ";
			else if(this->id==4)
				sentence="HEAVY CRITICAL FIST!           ";
		}else{
			if(this->id==0)
				sentence="You hit the monster!           ";			
			else if(this->id==1)
				sentence="Monster severly hurt you!      ";	
			else if(this->id==3)
				sentence="Vampire attacks you!           ";
			else if(this->id==4)
				sentence="Berserker attack with his fury!";	
		}
			
		damage+=bonus_damage;
		damage-=target->getDef();
		if(damage<=0)
			damage=1;
			
		target->setHp(target->getHp()-damage);
		if(target->getHp()<0)
			target->setHp(0);
		
		stringstream ss;
		ss << damage;
		string str = ss.str();
		
		int total_lifesteal;
		total_lifesteal = int((float)damage * (float)lifesteal / 100.0); 
		//cout << "THE LIFESTEAL IS: " << damage << " " << damage*lifesteal/100 << " " << lifesteal;
		//hold();
		
		this->hp += total_lifesteal;
		
		if(this->hp > this->maxHp)
			this->hp = this->maxHp;
		
		//+getName()+"@Dealt "+dmgDealt+" damage!";
		//sentence+=getName() + "@Dealt" + dmgDealt + "damage!";
		sentence+="@Dealt ";
		sentence+=str;
		sentence+=" damage!";
		advancedMsg(sentence, 4, 27, '+', false, 35);
		//msg(sentence, 1);
		if(this->id!=0){
		if(chance<=critical_chance){
			PlaySound(TEXT("atkCritical.wav"), NULL, SND_FILENAME | SND_ASYNC);
			//damagedScreen(true);
		}
		else{
			PlaySound(TEXT("atkNormal.wav"), NULL, SND_FILENAME | SND_ASYNC);
			//damagedScreen(false);	
		}
		}else{
			if(chance<=critical_chance){
			PlaySound(TEXT("atkPlayerCritical.wav"), NULL, SND_FILENAME | SND_ASYNC);
			}
			else{
			PlaySound(TEXT("atkPlayerNormal.wav"), NULL, SND_FILENAME | SND_ASYNC);
			}
		}
		
		
	} 
	
	/*template<class T>
	void attack(T *target){
		
		string sentence;
		int chance=rand()%100+1;
		int bonus_damage=rand()%(lvl*2);
		int damage=this->atk;
		
		if(chance<=critical_chance){
			damage=(int)((float)damage*1.38);
			sentence="VAMPRICAL ATTACK! SUPER EFFECTIVE!";
		}else
			sentence="The vampire attacked you!";
			
		damage+=bonus_damage;
		damage-=target->getDef();
		if(damage<=0)
			damage=1;
			
		target->setHp(target->getHp()-damage);
		if(target->getHp()<0)
			target->setHp(0);
		
		stringstream ss;
		ss << damage;
		string str = ss.str();
		
		int total_lifesteal;
		total_lifesteal = int((float)damage * (float)lifesteal / 100.0); 
		//cout << "THE LIFESTEAL IS: " << damage << " " << damage*lifesteal/100 << " " << lifesteal;
		//hold();
		
		this->hp += total_lifesteal;
		
		if(this->hp > this->maxHp)
			this->hp = this->maxHp;
		
		//+getName()+"@Dealt "+dmgDealt+" damage!";
		//sentence+=getName() + "@Dealt" + dmgDealt + "damage!";
		sentence+="@Dealt ";
		sentence+=str;
		sentence+=" damage!";
		msg(sentence, 1);
		
		if(chance<=critical_chance)
			damagedScreen(true);
		else
			damagedScreen(false);
	}
	*/
	
	Vampire(int atk, int hp, int def, int lvl, int floor, int lifesteal, int expGet=0, int critical_chance=13):Monster(atk, hp, def, lvl, floor){
		this->id = 3;
		this->lifesteal = lifesteal;
		this->critical_chance = critical_chance;
		this->expGet = expGet;
	}
};

class Berserker:public Monster{
	
	int atkup;
	int hpup;
	
public:
	
	Berserker(int atk, int hp, int def, int lvl, int floor, int critical_chance=10, int gold=100, int atkup=10, int hpup=-10, int expGet=0):Monster(atk, hp, def, lvl, floor, critical_chance, gold){
		this->id = 4;
		this->atkup = atkup;
		this->hpup = hpup;
		this->expGet = expGet;
	}
	
	void passive(){
		atk += atkup;
		hp += hpup;
	}
	
	template<class T>
	void attack(T *target){
	this->Monster::attack(target); 
	passive();
	}
};

class Zombie:public Monster{
	
	int chance;
	int turn;
	
public:
	
	Zombie(int atk, int hp, int def, int lvl, int floor, int critical_chance=10, int gold=100, int chance=50, int turn=2, int expGet=0):Monster(atk, hp, def, lvl, floor, critical_chance, gold){
		this->id = 5;
		this->chance = chance;
		this->turn = turn;
		this->expGet = expGet;
	}
	
	template<class T>
	void attack(T *target){
	this->Monster::attack(target); 
	
	int apply=rand()%100 + 1;
	if(apply<=chance)
		target->addStat(2);
		target->addTurn(turn);
	}
};

class Dragon:public Monster{
	
	int chance;
	int turn;
	
public:
	
	Dragon(int atk, int hp, int def, int lvl, int floor, int critical_chance=10, int gold=100, int chance=50, int turn=2, int expGet=0):Monster(atk, hp, def, lvl, floor, critical_chance, gold){
		this->id = 6;
		this->chance = chance;
		this->turn = turn;
		this->expGet = expGet;
	}
	
	template<class T>
	void attack(T *target){
	this->Monster::attack(target); 
	
	int apply=rand()%100 + 1;
	if(apply<=chance)
		target->addStat(1);
		target->addTurn(turn);
	}
};

class Player:public Monster{
	private:
		string name;
		int mp;
		int maxMp;
		int exp;
		int expNeeded;
		int sp;
		vector<Skill> skill;
		vector<int> item;
		bool run;
		
	public:
		
		Player(int atk, int hp, int def, int lvl, int floor, int mp, int gold, string name="Player"):Monster(atk, hp, def, lvl, floor){
			setGold(gold);
			this->mp = mp;
			this->lvl=lvl;
			this->critical_chance = 10;
			this->maxMp = mp;
			this->exp=0;
			this->expNeeded=48;
			this->sp = 0;
			this->id = 0;
			this->name = name;
			this->run = false;
		}
		
		int itemCount(){
		return this->item.size();
		}
		
		int getItemType(int iid){
			
			int counterItem=0;
			int totalItem=item.size();
			
			for(int i=0; i<totalItem; i++){
				if(item[i]==iid)
					counterItem++;
			}
			
			return counterItem;
		}
		
		void setRun(bool run){
			this->run = run;
		}
		
		bool isRun(){
			return this->run;
		}
		
		string getName(){
			return this->name;
		}
		
		int sizeItem(){
			return item.size();
		}
		
		int getItem(int iid){
			return item[iid];
		}
		
		void addItem(int iid){
		item.push_back(iid);
		}
		
		/*Item id:
		0. Heart Potion
		1. Mana Potion 
		2. Big Potion	
		*/
		bool useItem(int iid){
			bool exist;
			int total_item=item.size();
			for(int i=0; i<total_item; i++){
				if(item[i]==iid){
					exist=true;
					item.erase(item.begin()+i);
					break;
				}
			}
			
			if(!exist){
				//play sound effect fail
				return false;
			}else{
				switch(iid){
					case 0:
							hp = hp + (0.2*(float)maxHp) + 35;
							if(hp>maxHp)
								hp=maxHp;
							break;
					case 1:
							mp = mp + (0.3*(float)maxMp) + 5;
							if(mp>maxMp)
								mp=maxMp;
							break;
					case 2: hp = hp + (0.4*(float)maxHp) + 140;
							if(hp>maxHp)
								hp=maxHp;
							break;
				}
				
				return true;
			}
			return false;
		}
		
		bool statUp(int stat_id){
			int temp;
			if(sp>0){
			
			switch(stat_id){
				case 0: 
						this->atk += (int)((float)atk*5/100)+1;
						//DIALOGUE_MAP("You spend your skill point on ATTACK!", true, 1);
						break;
				case 1: 
						temp = maxHp;
						this->maxHp += (int)((float)maxHp*2/100) + 10;
						this->hp += (maxHp-temp);
						//DIALOGUE_MAP("You spend your skill point on HEALTH POINT!", true, 1);
						break;
				case 2: 
						temp = maxMp;
						this->maxMp += (int)((float)maxMp*8/100) + 1;
						this->mp += (maxMp-temp);
						//DIALOGUE_MAP("You spend your skill point on MANA POINT!", true, 1);
						break;
				case 3: 
						temp=critical_chance/15;
						if(temp>1)
							temp=1;
						this->critical_chance += temp+1;
						//DIALOGUE_MAP("You spend your skill point on CRITICAL CHANCE!", true, 1);
						break;
				case 4:
						this->def += (int)((float)def*8/100)+2;
						//DIALOGUE_MAP("You spend your skill point on DEFENSE!", true, 1);
						break;
				
			}
			
			this->sp--;
			return true;
			}
			return false;
		}
		
		void lvlUp(){
			//msg("You leveled up!", 1);
			BATTLE_DIALOGUE("You just leveled up!      @", true, 10);
			this->exp=exp-expNeeded;
			this->expNeeded+=(expNeeded*18/100 + lvl*7);
			this->lvl++;
			iflvlbelow(4,5)
				else
				iflvl(5,8)
					else
					iflvlbelow(9,5)
						else
						iflvl(10,10)
							else
							iflvlbelow(14,6)
								else
								iflvl(15,12)
									else
									iflvlbelow(19,6)
										else
										iflvl(20,12)
										
			//this->sp = sp + 5;
		}
		
		void addExp(int exp){
			this->exp+=exp;
			if(this->exp>=expNeeded){
				lvlUp();
			}
		}
		
		void addGold(int gold){
			this->gold += gold;
		}
		
		int getSp(){
			return this->sp;
		}
		
		void addSp(int sp){
			this->sp += sp;
		}
		
		int getExp(){
			return this->exp;
		}
		
		int getExpNeeded(){
			return this->expNeeded;
		}
		
		int getMp(){
			return this->mp;
		}
		
		void setMp(int mp){
			this->mp = mp;
		}
		
		int getMaxMp(){
			return this->maxMp;
		}
		
		void setMaxMp(int maxMp){
			this->maxMp = maxMp;
		}
		
		void addSkill(Skill *skilltemp){
			skill.push_back(*skilltemp);
		}
		
		int countSkill(){
			return this->skill.size();
		}
		
		int getSkillStatus(int iid){
			return this->skill[iid].getStatus();
		}
		
		int getSkillTurn(int iid){
			return this->skill[iid].getTurn();
		}
		
		int getSkillChance(int iid){
			return this->skill[iid].getChance();
		}
		
		string getSkillName(int iid){
			return this->skill[iid].getName();
		}
		
		int getSkillMp(int iid){
			return this->skill[iid].getMp();
		}
		
		template<class T>
		bool castSkill(int iid, T *target){
			if(skill[iid].getMp()<=this->mp){
				
				if((skill[iid].getMp()==-1 && this->mp==0))
					return false;
					
				skill[iid].cast(target, this->atk, this->maxMp);
				this->mp-=skill[iid].getMp();
				
				if(skill[iid].getMp()==-1)
					this->mp = 0;
					
				return true;
			}
				return false;
		}
		
};

template<class T>
void battleSequence(Player *player, T *monster, bool runnable=true);

class Map{
	
	private:
		int playerCoordinate;          // Player would be 2 digiti (Example: 58 --> Coordinate 5,8)
		vector<int> objectCoordinate;  // Object would be 3 digit (Example: 751 --> Coordinate 7,5 with object type 1)
		vector<Monster*> vecMonster;   // Object type list: 1. Item -- 2. Encounter(Random Monster) -- 3. Specific Monster
		int floor;					   //4. StairUp -- 5. StairDown // 6. Unique Monster(Random Monster)
		Player *player;					 
		int encounter;
		bool cleared;
						
	public:
		
		void setPlayerCoordinate(int playerCoordinate){
			this->playerCoordinate = playerCoordinate;
		}
		
		bool isCleared(){
			return this->cleared;
		}
		
		int getEncounter(){
			return this->encounter;
		}
		
		void addObject(int coord_x, int coord_y, int type){
			coord_x *= 100;
			coord_y *=10;
			objectCoordinate.push_back(coord_x + coord_y + type);
		}
		
		template<class T>
		void addSpecialMonster(T *special, int coord_x, int coord_y){
			vecMonster.push_back(special);
			addObject(coord_x, coord_y, 3);
			clearMsg();
			printEntity();
			printStatus(player);
		}
		
		void checkEvent(bool afterBattle, bool winBattle=true){
			if(floor==1){
				
				if(encounter==4 && afterBattle && !cleared){
					Vampire *vampire = new Vampire(41, 133, 6, 7, floor, 75, 120,100);
					addSpecialMonster(vampire, 1, 1);
				}
				
				if(getpx()==1 && getpy()==1 && afterBattle && winBattle){

					BATTLE_DIALOGUE("[Vampy the Vampire]@Do you know the history of this world?   ", true, 30);
					BATTLE_DIALOGUE("[Vampy the Vampire]@This terrible land was called Alvana"   , true, 30);
					
				}
				
				if(encounter==11 && afterBattle && !cleared && winBattle){
					Berserker *berserker = new Berserker(44, 208, 3, 9, floor, 13, 391, 18, -10, 133);
					addSpecialMonster(berserker, 9, 4);
					SHOW_FULL_UI;
					mciSendString("play heroine_sound.wav", NULL, 0, NULL);
					DIALOGUE_MAP("["+player->getName()+"]@"+"That sound!   ", true, 10)
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[Berserker]@Do you know her? uwu   ", true, 10)
					DIALOGUE_MAP("["+player->getName()+"]@"+"What the hell?. . .   @His sound is very cute -_-   ", true, 10)
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[Berserker]@Hey, if you are her companion, you@should rescue her as fast as possible UWU", true, 10)
					DIALOGUE_MAP("["+player->getName()+"]@"+"Of course i will!   ", true, 10);
					DIALOGUE_MAP("["+player->getName()+"]@"+"(Why did he end his sentence with uwu?)", true, 10);
					DIALOGUE_MAP("[@   That's Berserker. Every turn his@   attack will be increased, but his defense will@   be decreased'", true, 10)
					
				}
				
				if(encounter>=6 && afterBattle && encounter<=7 && winBattle){
					generateObject(2, 1);
					printEntity();
				}
				
				if(encounter==5 && afterBattle && winBattle){
					SHOW_FULL_UI;
					mciSendString("play god_descend.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[Voice from Distant]@I come from that distant, and coming here@to bring you a remedy just in case you@are so not lucky enough.   ", true, 50)
					DIALOGUE_MAP("[@   You received 2x Heart Potion!   ", true, 10)
					DIALOGUE_MAP(PLAYER_NAMETAG + "Well, thanks. But your grammar sucks.   ", true, 10)
					DIALOGUE_MAP("[Voice from Distant]@I cannot hear you! ~ ~   @", true, 10)
					player->addItem(0);
					player->addItem(0);
					printEntity();
					printStatus(player);
				}
				
				if(PLAYER_COORDINATE(9,4) && afterBattle && winBattle){
					reposition_player();
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[Berserker]@hey...", true, 40)
					DIALOGUE_MAP(PLAYER_NAMETAG + "?", true, 40)
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[Berserker]@hey tayo~ uwu", true, 40)
					DIALOGUE_MAP(PLAYER_NAMETAG + "Oh my lord *sigh. @It's a dead meme, stop it'", true, 10)
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[Berserker]@Actually i just wanna tell you something. . .", true, 10)
					DIALOGUE_MAP(PLAYER_NAMETAG + "Oh yeah, i almost forgot.@Please tell me where she is!", true, 10)
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[Berserker]@Don't worry little guy, she's not in danger.", true, 10)
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[Berserker]@Floor 5 is the place that you will find her", true, 10)
					DIALOGUE_MAP(PLAYER_NAMETAG + "Well, i notice that 'Floor 1/5' thingy in my vision.@So it's not a suprise that she is in up there.", true, 20)
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[Berserker]@What a lucky fellow, i don't@have that kind of vision uwu.'", true, 10)
					DIALOGUE_MAP(PLAYER_NAMETAG + "By the way, thank you for the @information. I really appreciated it.", true, 10)
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[Berserker]@By the way too, ugandan knuckle is the best meme uwu.", true, 10)
					DIALOGUE_MAP(PLAYER_NAMETAG + "Hey! Like i said stop uttering a dead. . .", true, 10)
					mciSendString("play explode.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[@   *berserker_explodes", true, 10)
					DIALOGUE_MAP("[@   *"+player->getName()+" takes 51 damage from the explosion!", true, 10)
					player->setHp(player->getHp()-51);
					if(player->getHp()<=0){
						DIALOGUE_MAP(PLAYER_NAMETAG + "Uaaaaaa. . .", true, 20)
						DIALOGUE_MAP("[@   " +player->getName()+" have died from explosion.", true, 10)
						DIALOGUE_MAP("[@   GAME OVER!!!", true, 10)
						DIALOGUE_MAP("[@   LOL    LOLLLL  LOLLLLL@  LOLLLLLLLLLL!!!!", true, 5)
						clearMsg();
						exit(0);
					}
					SHOW_FULL_UI;
					DIALOGUE_MAP(PLAYER_NAMETAG + "Really?. . .   @I feel really glad that i didn't die. . .   ", true, 15)	
					DIALOGUE_MAP("[@    The stair to floor 2 have been opened just now!   ", true, 15)
					cleared = true;
					addObject(9,4,4);
					floor_progress++;
				}
				
				if(PLAYER_COORDINATE(9,4) && afterBattle && !winBattle){
					reposition_player();
					SHOW_FULL_UI;
					DIALOGUE_MAP("[Berserker]@Do you know da wae?", true, 20)
					DIALOGUE_MAP(PLAYER_NAMETAG + "Oh shut up.@It's a dead mem. . .'", true, 20)
				}
				
			}
			
			if(floor==2){
				
				if(encounter==2 && afterBattle && !cleared){
					Zombie *zombie = new Zombie(63, 141, 17, 14, floor, 13, 360, 40, 1, 234);
					addSpecialMonster(zombie, 5, 5);
					SHOW_FULL_UI;
					DIALOGUE_MAP("[@   Zombie just appeared in the center of the map!", true, 15);
					DIALOGUE_MAP("[@   Zombie can infect you with deadly poison @with its normal attack. Be careful!", true, 15);
					mciSendString("play zombie_sound.wav", NULL, 0, NULL);
				}
				
				if(PLAYER_COORDINATE(5,5) && afterBattle && winBattle){
	
					mciSendString("play zombie_sound.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE("[Zombie]Aa17aTa w0 64cOd   ", true, 20)
					mciSendString("stop zombie_sound.wav", NULL, 0, NULL);
					mciSendString("play zombie_sound.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE("[Zombie]41 b3T y1/ d0nT U17D3r5T4nD 1)(1E r161-1T?   ", true, 20)
					BATTLE_DIALOGUE(PLAYER_NAMETAG + ". . . . .   ", true, 20)
					mciSendString("stop zombie_sound.wav", NULL, 0, NULL);
					mciSendString("play zombie_sound.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE("[Zombie]!#*& !a%jh! ##(dsX%). . .   ", true, 20)
					mciSendString("play bacod.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "BAACOOOOOOOOOODDDDDD!!!!   @Udah mati, mau mati lagi, bacod lagi.   ", true, 35)
					BATTLE_DIALOGUE("[Developer]@*whisper   ", true, 10)
					BATTLE_DIALOGUE("[Developer]@woe, settingnya lu pake bahasa inggris   ", true, 10)
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "I'm so sorry. Please don't cut my salary   ", true, 10)
					BATTLE_DIALOGUE("[Developer]@As long as you understand.   ", true, 10)
				}
				
				if(encounter==7 && afterBattle && winBattle){
					SHOW_FULL_UI;
					mciSendString("play duo_laugh.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[@   *noise.............@................@.................", true, 20)
					DIALOGUE_MAP(PLAYER_NAMETAG + "Who is that?   @I heard many people.", true, 10)
					DIALOGUE_MAP("[Duo Vampire]@Pleased to meet you. We are the duo   @that controls the darkness.   ", true, 10)
					DIALOGUE_MAP(PLAYER_NAMETAG + "I think it is more accurate to@call it illusion. Just now i think i heard many people.   ", true, 10)
					DIALOGUE_MAP("[Duo Vampire]@You are the one who killed our Vampy, right?   ", true, 10)
					DIALOGUE_MAP(PLAYER_NAMETAG + "Oh! The one who said that this land was called Alvana.   @Is that your comrades or something?   ", true, 10)
					DIALOGUE_MAP("[Duo Vampire]@It's very distressing that you just talk about Vampy so lightly.   ", true, 10)
					DIALOGUE_MAP(PLAYER_NAMETAG + "What can i do? When i first saw that 'M', i got@intrigued and decide to walk over there.   ", true, 10)
					DIALOGUE_MAP("[Duo Vampire]@You're going to pay!'   ", true, 10)
					Vampire *vampire = new Vampire(57, 231, 1, 18, floor, 20, 212, 28);
					clearMsg();
					
					battleSequence(player, vampire, false);
					
					BATTLE_DIALOGUE("[Fulo the Big Brother]@My brother will avenge you, damn it!   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "You still wanna fight?   ", true, 10);
					Vampire *vampire2 = new Vampire(19, 51, 48, 15, floor, 80, 100);
					
					battleSequence(player, vampire2, false);
					
					BATTLE_DIALOGUE("[Filo the Little Brother]@Uaaaa. . .   ", true, 30);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "He's super weak!   ", true, 10);
					BATTLE_DIALOGUE("[Fulo the Big Brother]@I should never trust my brother after all!   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Hey, your name is Fulo, right?@Please tell me about Alvana before you vanish!   ", true, 10);
					mciSendString("play bgm_duoVampire.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE("[Fulo the Big Brother]@I think there's nothing to lose.   ", true, 10);
					BATTLE_DIALOGUE("[Fulo the Big Brother]@Alvana was a kind land. Even though there's many@races that lives here, dragon, zombie, human, and@including us vampires are living in peace.   ", true, 10);
					BATTLE_DIALOGUE("[Fulo the Big Brother]@But when one of the races hears a seems glamorous@rumors, this place gone from a peaceful@city into this gruelsome tower like dungeon.   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "What kind of rumors is that?@I just can't believe one single rumors cause all this to happend.", true, 10);
					BATTLE_DIALOGUE("[Fulo the Big Brother]@If you die, you will be transported to Isekai or another world.   ", true, 10);
					mciSendString("stop bgm_duoVampire.wav", NULL, 0, NULL);
					mciSendString("play bgm_duoVampire2.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Really? REALLY!!!???@Let me guess, that one race must be human, right?   ", true, 10);
					BATTLE_DIALOGUE("[Fulo the Big Brother]@That's true though. How do you know?   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "I think, soon i will contact that developer.   ", true, 10);
					mciSendString("stop bgm_duoVampire2.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE("[Fulo the Big Brother]@W H O ' S   D E V E L O P E R   ?   ", true, 30);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "I'm exist right now because of my developer.   ", true, 10);
					BATTLE_DIALOGUE("[Fulo the Big Brother]@W H O ' S   D E V E L O P E R   ?   ", true, 30);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Hello. . . are you okay?   ", true, 10);
					BATTLE_DIALOGUE("[Fulo the Big Brother]@I'm okay, even though i will die in a matter of time.", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "My developer didn't dev-. . .   ", true, 10);
					BATTLE_DIALOGUE("[Fulo the Big Brother]@W H O ' S   D E V E L O P E R   ?   ", true, 30);
					mciSendString("play bgm.mp3", NULL, 0, NULL);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Okay, okay developer. You're doing this to@make the story looks much longer, right?'", true, 10);
					BATTLE_DIALOGUE("[Developer]@LOL, how do you know it?   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "I just had this hunch when i heard Fulo's story.   ", true, 10);
					BATTLE_DIALOGUE("[Developer]@Just get out from this endless dialogue!   ", true, 10);
					BATTLE_DIALOGUE("[   @You just got x2 Heart Potion from Fulo's pouch.   ", true, 10);
					player->addItem(0);
					player->addItem(0);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "It did say from Fulo's pouch, but i'm not stealing, okay?@Developer forces me.   ", true, 10);
					BATTLE_DIALOGUE("[Developer]@Can you not complain about every little detail?   ", true, 10);
					player->addExp(vampire->getExpGet()+vampire2->getExpGet());				
				}
				
				if(encounter==9 && afterBattle && winBattle){
					Dragon *dragon = new Dragon(93, 371, 14, 21, floor, 12, 360, 50, 2, 528);
					addSpecialMonster(dragon, 1, 1);
					SHOW_FULL_UI;
					mciSendString("play god_descend.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[@   Something descend from the sky.   ",true,50);
					mciSendString("play bgm.mp3", NULL, 0, NULL);
					DIALOGUE_MAP("[Sky Dragon]@It seems like it is our fate to meet again, shounen.   ",true,10);
					DIALOGUE_MAP(PLAYER_NAMETAG + "There's no way. . . you're from that voice. . .@. . the very narcistic angel and also sucks at first.   ",true,10);
					DIALOGUE_MAP("[Sky Dragon]@Would you be ignorant enough to talk like that?   ",true,10);
					DIALOGUE_MAP(PLAYER_NAMETAG + "Say, are you from Isekai?   ",true,10);
					DIALOGUE_MAP("[Sky Dragon]@Yes. I have stayed in pararrel time as 3 form.@Slime, human, and lastly as dragon.   ",true,10);
					DIALOGUE_MAP(PLAYER_NAMETAG + "Slime?   ",true,10);
					DIALOGUE_MAP("[Sky Dragon]@Truth to be told, my life as slime was a short one.@But i never hope to reincarnate as Human.   ",true,10);
					DIALOGUE_MAP("[Sky Dragon]@But life as a human is not what i expect.@It's full of conflict, sadness, and despair.   ",true,10);
					DIALOGUE_MAP(PLAYER_NAMETAG + "Did you reincarnate on the same world?   ",true,10);
					DIALOGUE_MAP("[Sky Dragon]@Yes, at first i believed i will be transported to Isekai.@But i guess this is not bad.   ",true,10);
					DIALOGUE_MAP(PLAYER_NAMETAG + "HOW ARE YOU GOING TO TAKE RESPONSIBILITY?@Because of you, Alvana becomes a wasteland.   ",true,10);
					DIALOGUE_MAP("[Sky Dragon]@I've heard a prophecy long time ago when i was a human. Alvana will become a wasteland.@So don't blame me because it's going to happen at some point.'   ",true,10);
					DIALOGUE_MAP(PLAYER_NAMETAG + "Alvana was my dreamland.@Alvana was the place that i met her.@I will save my dreamland, by defeating the rumored dragon! YOU!!   ",true,10);
					DIALOGUE_MAP("[Sky Dragon]@Come to me when you are ready to face me!.'   ",true,10);
					
				}
				
				if(PLAYER_COORDINATE(1,1) && afterBattle && winBattle){
					SHOW_FULL_UI;
					mciSendString("play dragon_gone.wav", NULL, 0, NULL);
					mciSendString("play dragon_gone2.wav", NULL, 0, NULL);
					DIALOGUE_MAP("[@   Sky Dragon vanish into the thin sky   ",true,30);
					DIALOGUE_MAP(PLAYER_NAMETAG + "That was too fast!   @My question haven't been answered!'",true,10);
					DIALOGUE_MAP(PLAYER_NAMETAG + "I guess by heading to top floor will answer my question.   '",true,10);
					addObject(5,1,4);
					cleared=true;
					floor_progress++;
				}
			}
			
			if(floor==5){
				if(PLAYER_COORDINATE(9,9) && afterBattle & winBattle){
					
					mciSendString("play bgm.mp3", NULL, 0, NULL);
					
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE("[Berserker]@How can my cuteness lose to you? uwu  ", true, 10)
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "We don't compete over cuteness, you uwu maniac.   ", true, 10)
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE("[Berserker]@Ugandan knuckles still is my best meme. uwu   ", true, 10)
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Ah, this pattern! Please don't explode!   ", true, 10)
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE("[Berserker]@I will not explode. Same tragedy won't happen.   ", true, 10)
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Yeah, tragedy indeed. That was underhanded!   ", true, 10)
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play god_descend.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE("[Sky Dragonfly]@Be glad that i was sent here to aid you   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Ahhhh! Now you reincarnated into dragonfly?   ", true, 10)
					BATTLE_DIALOGUE("[Sky Dragonfly]@Sorry then! I can't help it.@Developers keeps transforming me even before the game begins.   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "I pity you. . .@What do you mean by aiding me?   ", true, 10)
					BATTLE_DIALOGUE("[Sky Dragonfly]@Don't you just realize that you have beaten the final boss?   ", true, 10);
					mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE("[Berserker]@Yes, i'm the final boss. uwu   ", true, 10)
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "What?! You sure re-used many characters, developer.   ", true, 10)
					mciSendString("stop god_descend.wav", NULL, 0, NULL);
					mciSendString("play god_descend.wav", NULL, 0, NULL);
					Sleep(1000);
					BATTLE_DIALOGUE("[Developer]@Hahaha, like i said i don't have many time to implement many different character.   ", true, 10);
					BATTLE_DIALOGUE("[Sky Dragonfly]@Hey! That's my sound effect!   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "This is rough to see.   ", true, 10)
					BATTLE_DIALOGUE("[Developer]@Now, do your job Yuutsukari the Sky Dragonfly!", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Yuutsukari!?   ", true, 10)
					BATTLE_DIALOGUE("[Yuutsukari]@The truth, i was your subconscious mind all along.   ", true, 10);
					mciSendString("stop bgm.mp3", NULL, 0, NULL);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Masaka!?(It' can't be) Are you the one that i possess when i got inside my dreams?", true, 10);
					
					BATTLE_DIALOGUE("[Yuutsukari]@Yes. You have visited Alvana before. You did in this form.   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "But i never remember about being a slime in my dream.   ", true, 10);
					
					BATTLE_DIALOGUE("[Yuutsukari]@Memory can be altered and are easily be forgotten.@Did you remember when you awake in apartement and searching for a refrigerator?   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "I remember that! I found a sweets inside a refrigerator.@All this time, i was possessing you when i awake in my dream?   ", true, 10);
					
					BATTLE_DIALOGUE("[Yuutsukari]@Life is an illusion. But reality is not a fake one.@", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Reality is not fake, huh? I wish reality is fake though.   @ I wish. . .", true, 25);
					
					BATTLE_DIALOGUE("[Yuutsukari]@What do you think? Is it right now just a fake moment, or reality?   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Please tell me the truth.@Am i transported from my original world, or am i in a dream again?   ", true, 10);
					
					BATTLE_DIALOGUE("[Yuutsukari]@They say if you ask your dream guide, they will speak the truth.   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "What about her? The little angel that i met in Alvana?   ", true, 10);
					
					BATTLE_DIALOGUE("[Yuutsukari]@That's just a dream. You won't be able to meet her.@That little angel may still appear though in your dream.   ", true, 10);
					BATTLE_DIALOGUE("[Yuutsukari]@Remember. Wish are a powerful tool in a dreamland.   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "My little angel. . .", true, 10);
					
					addObject(9,7,6);// (10 for little angel)
					addObject(7,7,8);// (12 for dragonfly)
					clearMsg();
					printEntity();
					mciSendString("play god_descend.wav", NULL, 0, NULL);
					Sleep(3000);
					
					BATTLE_DIALOGUE("[Little Angel]@Hello there!   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "My little angel!   ", true, 10);
					
					BATTLE_DIALOGUE("[Little Angel]@Have your swordmanship skill increase lately?   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "You still remember our meeting? Yes, i can meet you    @because my skill keeps growing.   ", true, 10);
					
					BATTLE_DIALOGUE("[Little Angel]@Of course. You're the one who taught me swordmanship.   ", true, 10);
					
					
					BATTLE_DIALOGUE("[Little Angel]@*her voice becomes more distant@[  [You're hero. You may not saved Alvana, but you just opened your way to reality]   ]   ]   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Hey!. . .   ", true, 10);
					
					BATTLE_DIALOGUE("[Little Angel]@*her voice becomes more and more distant@   [      [Yo- sha-- re--rn -- you- re--lty, a-- forg-- -bout m-]      ]@", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "*my vision becomes blurry   ", true, 10);
					clearMsg();
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "*it gone completely black   ", true, 10);
					clearMsg();
					Sleep(2000);
					playerCoordinate = 17;
					objectCoordinate.clear();
					addObject(1,6,7);
					addObject(2,6,7);
					addObject(3,6,7);
					addObject(4,6,7);
					addObject(4,7,7);
					addObject(4,8,7);
					printEntity();
					
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Where am I?   ", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "*looks around   @", true, 10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "It's my bed! Is it just a dream?   @", true, 10);
					BATTLE_DIALOGUE("[@   Alvana was a world that created from Kazuma's dream.   @   Kazuma finally awake from his long dream.   ",true,30)
					BATTLE_DIALOGUE("[@   That was the story supposed to be. . .   @", true, 30);
					
					addObject(3,7,9); //(13 for berserker)
					printEntity();
					mciSendString("play berserker_sound.wav", NULL, 0, NULL);
					BATTLE_DIALOGUE("[Berserker]@Ciao! You looked pretty shocked. uwu   ",true,10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "How!? How did you get in here!?", true, 10);
					BATTLE_DIALOGUE("[Developer]@You know a dream that resulting in awake inside a dream? @That is the kind of situation that you are in right now.   ",true,10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Oh lord. You're going to end the story like this?   ", true, 10);
					BATTLE_DIALOGUE("[Developer]@Of course not!   ",true,10);
					mciSendString("play bgm.mp3", NULL, 0, NULL);
					BATTLE_DIALOGUE("[@   Actually Kazuma just died from Berserker's explosion. He reincarnated as human again.@   Being the world where you can reincarnate really fast, Alvana crumbles down easily.   ",true,10);
					BATTLE_DIALOGUE("[@   This world is indeed from Kazuma's dreamland. Before he cames to Alvana, he dreams about this place.@   He's been dreaming since Alvana was in peace.",true,10);
					BATTLE_DIALOGUE("[@   Dream connected to another world. Death brings us to that another world.   @   Legend said those who cannot dream, will not have a place to stay after he/she dies.   ",true,10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Stop doing that! This is not visual novel!@We don't even have any visual beside the battle sequence!", true, 10);
					BATTLE_DIALOGUE("[@   In the end, Alvana is-  @",true,10);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "Stop!   @", true, 10);
					BATTLE_DIALOGUE("[Developer]@Stop interrupting me!   @", true, 10);
					BATTLE_DIALOGUE("[Developer]@Aaaaahh!! The time is almost up!   @", true, 20);
					BATTLE_DIALOGUE(PLAYER_NAMETAG + "THIS IS NOT A TV SERIES NOR AN ANIME!!!!!!!!!!!   @THERE IS NO NEXT EPISODE!!!!!!!   ", true, 10);
					clearMsg();
					Sleep(1000);
					BATTLE_DIALOGUE("[@   T H A N K   Y O U   F O R   P L A Y I N G  ! !   @", true, 80);
					clearMsg();
					Sleep(3000);
					exit(0);	
				}
			}
				
			
		}
		
		bool playerMovex(int step){
			
			int x;
			int y;
			
			if(playerCoordinate+(step*10)<100 && playerCoordinate+(step*10)>10){
			x = getpx();
			y = getpy();
			gotoxy(x,y);
			cout << ' ';
			playerCoordinate += step*10;
			return true;
			}
			else
				return false;
		}
		
		bool playerMovey(int step){
			
			int x;
			int y;
			
			if((playerCoordinate%10)+(step)<10 && (playerCoordinate%10)+(step)>0){
			x = getpx();
			y = getpy();
			gotoxy(x,y);
			cout << ' ';
			playerCoordinate += step;
			return true;
			}
			else
				return false;
		}
		
		int getPlayerCoordinate(){
			return this->playerCoordinate;
		}
		
				
		int getobjx(int index){
		int x = objectCoordinate[index] / 100;	
		return x;
		}
		
		int getobjy(int index){
		int y = (objectCoordinate[index] / 10) % 10;
		return y;
		}
		
		int getobj_id(int index){
		int id = objectCoordinate[index] % 10;
		return id;
		}
		
		int getpx(){ //get player's coordinate for X axis
			int coord;
			coord = playerCoordinate / 10;
			return coord;
		}
		
		int getpy(){ //for y
			int coord;
			coord = playerCoordinate % 10;
			return coord;
		
		}
		
		void printStatus(Player *player){
			
			stringstream statusPlayer;
			
			statusPlayer << player->getName() skipm << "---------" skipm;
			statusPlayer << "Health Point: " << player->getHp() << "/" << player->getMaxHp()  skipm ;
			statusPlayer << "Mana Point: " << player->getMp() << "/" << player->getMaxMp()  skipm ;
			statusPlayer << "Attack: " << player->getAtk()  skipm;
			statusPlayer << "Defense: " << player->getDef()  skipm ;
			statusPlayer << "Critical Chance: " << player->getCritical_chance() << "%"  skipm;
			statusPlayer << "---------@" << "Level: " << player->getLvl()  skipm ;
			statusPlayer << "Exp: " << player->getExp() << "/" << player->getExpNeeded()  skipm;
			statusPlayer << "Skill Point: " << player->getSp()  skipm ;
			statusPlayer << "Gold: " << player->getGold() skipm;
			statusPlayer << "Floor: " << this->floor << "/5" skipm;	
			statusPlayer << "Encounter: " << this->encounter;
			//msg(statusPlayer.str(), 0);			
			advancedMsg(statusPlayer.str(), 46, 3, '!', false);
			
			int potion=0;
			int mana=0;
			int big_potion=0;
			
			int item_size=player->sizeItem();
			
			for(int i=0; i<item_size; i++){
				switch(player->getItem(i)){
					case 0: potion++;
							break;
					case 1: mana++;
							break;
					case 2: big_potion++;
							break;
				}
			}
			
			stringstream itemPlayer;
			itemPlayer << "(USE)" skipm;
			itemPlayer << "(Z) Heart Potion: " << potion skipm;
			itemPlayer << "(X) Mana Potion: " << mana skipm;
			itemPlayer << "(C) Angel Potion: " << big_potion skipm;
			advancedMsg(itemPlayer.str(), 75, 3, '!', false);
			
			stringstream skillPlayer;
			skillPlayer << "(SPEND SKILL POINT)" skipm;
			skillPlayer << "(1) Health" skipm;
			skillPlayer << "(2) Mana" skipm;
			skillPlayer << "(3) Attack" skipm;
			skillPlayer << "(4) Defense" skipm;
			skillPlayer << "(5) Critical Chance";
			advancedMsg(skillPlayer.str(), 75, 10, '!', false);
			
			stringstream shopPlayer;
			shopPlayer << "(SHOP WITH GOLD)" skipm;
			shopPlayer << "(U) Heart Potion(1000)" skipm;
			shopPlayer << "(J) Mana Potion(800)" skipm;
			shopPlayer << "(M) Big Potion(2800)" skipm;
			shopPlayer << "(O) Skill Point(1600)" skipm;
			shopPlayer << "(P) Skill Point 3(4350)";
			
			advancedMsg(shopPlayer.str(), 102, 3, '!', false);
			
		}
		
		void printEntity(){
			int x;
			int y;
			int id;
			char icon;
			
			int coord_size=objectCoordinate.size();
	
			for(int i=0; i<coord_size; i++){
				x = getobjx(i);
				y = getobjy(i);
				id = getobj_id(i);
				
				switch(id){
					case 1: icon = 'O';
					break;
					case 2: icon = 'X';
					break;
					case 3: icon = 'M';
					break;
					case 4: icon = 'S'; //nanti liat
					break;
					case 5: icon = 's'; //nanti liat juga
					break;
					case 6: icon = 'A';
					break;
					case 8: icon = 'D';
					break;
					case 9: icon = 'B';
					break;
					case 7: icon = '#';
					break;
					
				}
			gotoxy(x,y);
			cout << icon;
			}
			x = getpx();
			y = getpy();
			gotoxy(x,y);
			icon = 'P';
			cout << icon;
			
			int boundaryX=10*BoundaryOfRealityX;
			int boundaryY=10*BoundaryOfDreamY;
			
			for(int i=0; i<boundaryX; i++){
				gotoxyreal(i,0);
				cout << '#';
				gotoxyreal(i,boundaryY);
				cout << '#';
			}
			for(int i=0; i<boundaryY; i++){
				gotoxyreal(0,i);
				cout << '#';
				gotoxyreal(boundaryX, i);
				cout << '#';
			}
			gotoxy(0,30);
		}
		
		void generateObject(int amountMonster=10, int item=4){
			
			int monster=amountMonster;

			int x;
			int y;
			int type;
			vector<int> x_forbidden;
			vector<int> y_forbidden;
			
			switch(floor){
			case 1: ADD_FORBIDDEN(1,1);
					ADD_FORBIDDEN(9,4);
					ADD_FORBIDDEN(1,4);
			break;
			
			case 2:
					ADD_FORBIDDEN(1,4);
					ADD_FORBIDDEN(9,4);
					ADD_FORBIDDEN(5,1);
					ADD_FORBIDDEN(5,5);
					ADD_FORBIDDEN(1,1);
					addObject(1,4,5);
					if(cleared)
						addObject(5,1,4);
				
			break;
			}
			
			type = 2;
			for(int i=0; i<monster; i++){
				bool overlap=false;
				int coord_size=objectCoordinate.size();
				x = rand()%9 + 1;
				y = rand()%9 + 1;
				for(int j=0; j<coord_size; j++){
					if((x==getobjx(j) && y==getobjy(j))||(x==getpx() && y==getpy())){
					overlap = true;
					break;
					}
				}
				
				for(int j=0; j<x_forbidden.size(); j++){
					if(x==x_forbidden[j] && y==y_forbidden[j]){
					overlap = true;
					break;
					}
				}
				
				if(!overlap)
					objectCoordinate.push_back((x*10 + y)*10 + type);
				else
					i--;
			}
		
			type = 1;
			if(item!=0)	
			for(int i=0; i<item; i++){
				bool overlap=false;
				int coord_size=objectCoordinate.size();
				x = rand()%9 + 1;
				y = rand()%9 + 1;
				for(int j=0; j<coord_size; j++){
					if((x==getobjx(j) && y==getobjy(j))||(x==getpx() && y==getpy())){
					overlap = true;
					break;
					}
				}
				
				for(int j=0; j<x_forbidden.size(); j++){
					if(x==x_forbidden[j] && y==y_forbidden[j]){
					overlap = true;
					break;
					}
				}
				
				if(!overlap)
					objectCoordinate.push_back((x*10 + y)*10 + type);
				else
					i--;
					
			}
		}
		
		void updatePlayer(){
			int x = getpx();
			int y = getpy();
			gotoxy(x,y);
			cout << 'P';
		}
		
		void reposition_player(){
			
			int xp=getpx();
			int yp=getpy();
			bool overlap_xmin=false;
			bool overlap_xmax=false;
			bool overlap_ymin=false;
			bool overlap_ymax=false;
			
			int coord_size=objectCoordinate.size();
			
			for(int i=0; i<coord_size; i++){
				if(xp-1==getobjx(i) && yp==getobjy(i)){
					overlap_xmin=true;
				}
				if(xp+1==getobjx(i) && yp==getobjy(i)){
					overlap_xmax=true;
				}
				if(xp==getobjx(i) && yp-1==getobjy(i)){
					overlap_ymin=true;
				}
				if(xp==getobjx(i) && yp+1==getobjy(i)){
					overlap_ymax=true;
				}
			}
			
			if(!overlap_xmin && playerMovex(-1))
				true;
				else if(!overlap_xmax && playerMovex(1))
						true;
						else if(!overlap_ymin && playerMovey(-1))
								true;
								else if(!overlap_ymax && playerMovey(1))
									true;
								
			clearMsg();					
			printEntity();
			printStatus(player);
		}
		
		void checkCollision(){
			int coord_size=objectCoordinate.size();
			for(int i=0; i<coord_size; i++){
				if(getobjx(i)==getpx() && getobjy(i)==getpy()){
				if(getobj_id(i)==1){
					
							stringstream msgItem;
							int amount;
							int item_iid = rand()%100 + 1;
							
							msgItem << "You just got ";
							
							if(item_iid<=8){
								amount = rand()%3 + 1;
								msgItem << amount << " SKILL POINT!";
								player->addSp(amount);
							}else if(item_iid<=28){
								msgItem << "a HEART POTION!";
								player->addItem(0);
							}else if(item_iid<=50){
								msgItem << "a MANA POTION!";
								player->addItem(1);
							}else if(item_iid<=60){
								msgItem << "a HEART POTION and MANA POTION!";
								player->addItem(0);
								player->addItem(1);
							}else{
								amount = 188*(floor*1.1) + rand()%(166*floor);
								msgItem << amount << " GOLD!";
								player->addGold(amount);
							}
							
							mciSendString("play getItem.wav", NULL, 0, NULL);
							advancedMsg(msgItem.str(), 4, 25, '|', true, 25);
							objectCoordinate.erase(objectCoordinate.begin()+i);
							printStatus(player);
							break;
						}
					
					
				if(getobj_id(i)==2){ 
							advancedMsg("YOU ENCOUNTERED A MONSTER!   ", 4, 25, '|', true, 10);
							
							int atkT;
							int hpT;
							int defT;
							int critT;
							int lvlT;
							int goldT;
							int expT;
							
							if(floor==1){
								if(encounter<=5){
									//hpT = rand()%21 + 40;
									hpT = range(40,60);
									atkT = rand()%16 + 25;
									defT = 2 + rand()%4;
									critT = 6 + rand()%6;
									lvlT = 1 + rand()%5;
									goldT = 60 + rand()% 28;
									expT = 20 + 2*lvlT;
								}else{
									hpT = 55 + rand()%26;
									atkT = 35 + rand()%21;
									defT = 8 + rand()%4;
									critT = 6 + rand()%6;
									lvlT = 3 + rand()%5;
									goldT = 92 + rand()%25;
									expT = 24 + 2*(lvlT-2);
								}
							}else if(floor==2){
								if(encounter<=4){
									hpT = range(80,112);
									atkT = range(40,65);
									defT = range(9,13);
									critT = range(8,14);
									lvlT = range(8,13);
									goldT = range(135,188);
									expT = EXPERIENCE(55,5,8,1);
								}else{
									hpT = range(128,177);
									atkT = range(60,83);
									defT = range(13,18);
									critT = range(10,14);
									lvlT = range(13,17);
									goldT = range(159,233);
									expT = EXPERIENCE(181,13,13,1);
								}
							}
							
							
							Monster *imagineryMonster = new Monster(atkT, hpT, defT, lvlT, this->floor, critT, goldT, expT);
							bool result; 
							battleSequence(player, imagineryMonster);
							
							if(player->getHp()<=0){
								checkEvent(true, false);
							}
							else{
								encounter++;
								checkEvent(true, true);
								SHOW_FULL_UI;
							}
							
							if(player->isRun()){
								player->setRun(false);
								reposition_player();
								break;
							}
							
							CHECK_GAMEOVER;
							
							stringstream expgained;
							string expgained_str = "Congratulation!    @You gained ";
							
							expgained << expT << " exp!";
							expgained_str += expgained.str();
							BATTLE_DIALOGUE(expgained_str, true, 10);
							player->addExp(imagineryMonster->getExpGet());
							//msg(expgained_str, 1);
							
							player->addGold(imagineryMonster->getGold());
							//encounter++;
							//hold();
							
							clearMsg();
							objectCoordinate.erase(objectCoordinate.begin()+i);
							printEntity();
							printStatus(player);
							//checkEvent(true);
							break;
			}
			if(getobj_id(i)==3){
							int special_iid=-1;
							for(int a=0; a<coord_size; a++){
								if(objectCoordinate[a]%10==3)
									special_iid++;
								if(i==a)
									break;
							}
							switch(vecMonster[special_iid]->getId()){
							case 1: battleSequence(player, vecMonster[i]);
									break;
							case 3: battleSequence(player, (Vampire*)vecMonster[special_iid]);
									break;
							case 4: battleSequence(player, (Berserker*)vecMonster[special_iid]);
									break;
							case 5: battleSequence(player, (Zombie*)vecMonster[special_iid]);
									break;
							case 6: battleSequence(player, (Dragon*)vecMonster[special_iid]);
									break;
							}
							
							if(player->isRun()){
								player->setRun(false);
								reposition_player();
								break;
							}
							
							if(player->getHp()<=0)
								checkEvent(true, false);
							else{
								encounter++;
								checkEvent(true, true);
								SHOW_FULL_UI;
							}
								
								
								
							CHECK_GAMEOVER;
							
							int bonus_exp=0;
							int bonus_gold=0;
							
							switch(vecMonster[special_iid]->getId()){
								case 3: bonus_exp = 46*((float)floor*0.8);
										bonus_gold = 15*vecMonster[special_iid]->getLvl()*((float)floor*0.9);
										break;
								case 4: bonus_exp = 50*((float)floor*0.7);
										bonus_gold = 18*vecMonster[special_iid]->getLvl()*((float)floor*0.8);
										break;
							}
							
							stringstream expgained;
							string expgained_str = "Congratulation!@You gained ";
							expgained << ((vecMonster[special_iid]->getLvl())+66)*((float)floor*1.2)+bonus_exp<< " exp!";
							expgained << ((vecMonster[special_iid]->getExpGet())) + bonus_exp << " exp!";
							expgained_str += expgained.str();
							BATTLE_DIALOGUE(expgained_str, true,10);

							
							player->addExp((vecMonster[special_iid]->getExpGet()) + bonus_exp);
							player->addGold(vecMonster[special_iid]->getGold() + bonus_gold);
							
							
							clearMsg();
							objectCoordinate.erase(objectCoordinate.begin()+i);
							vecMonster.erase(vecMonster.begin()+special_iid);
							printEntity();
							printStatus(player);
							//checkEvent(true);
							
			}
		break;
		}
			
			}
			checkEvent(false);
		}
		
		void playerMove(char input){
			switch(input){
				case 'W': if(playerMovey(-1))
						updatePlayer();
						break;
				case 'A': if(playerMovex(-1))
						updatePlayer();
						break;
				case 'S': if(playerMovey(1))
						updatePlayer();
						break;
				case 'D': if(playerMovex(1))
						updatePlayer();
						break;
				case 'U': if(player->getGold()>=1000){
						player->addItem(0);
						player->setGold(player->getGold()-1000);
						DIALOGUE_MAP("[@   Heart Potion(x1) succesfully purchased!",true,10)
						printStatus(player);
						}else DIALOGUE_MAP("[@   Not enough money!",true,10)
						break;
				case 'J': if(player->getGold()>=800){
						player->addItem(1);
						player->setGold(player->getGold()-800);
						DIALOGUE_MAP("[@   Mana Potion(x1) succesfully purchased!",true,10)
						printStatus(player);
						}else DIALOGUE_MAP("[@   Not enough money!",true,10)
						break;
				case 'M': if(player->getGold()>=2800){
						player->addItem(2);
						player->setGold(player->getGold()-2800);
						DIALOGUE_MAP("[@   Big Potion(x1) succesfully purchased!",true,10)
						printStatus(player);
						}else DIALOGUE_MAP("[@   Not enough money!",true,10)
						break;
				case 'O': if(player->getGold()>=1600){
						player->addSp(1);
						player->setGold(player->getGold()-1600);
						DIALOGUE_MAP("[@   Skill Point(x1) succesfully purchased!",true,10)
						printStatus(player);
						}else DIALOGUE_MAP("[@   Not enough money!",true,10)
						break;
				case 'P': if(player->getGold()>=4350){
						player->addSp(3);
						player->setGold(player->getGold()-4350);
						DIALOGUE_MAP("[@   Skill Point(x3) succesfully purchased!",true,10)
						printStatus(player);
						}else DIALOGUE_MAP("[@   Not enough money!",true,10)
						break;
				
				
			}
			//PlaySound(TEXT("E:\\Project\\drum-hitclap2.wav"), NULL, SND_FILENAME | SND_ASYNC);
			if(input=='W' || input=='S' || input=='A' || input=='D'){
			PlaySound("sfxwalk.wav", GetModuleHandle(NULL), SND_FILENAME | SND_ASYNC);
			checkCollision();
			}else{
				bool success;
				switch(input){
					case '1': 
							success = player->statUp(hpstat);
							break;
					case '2':
							success = player->statUp(mpstat);
							break;
					case '3':
							success = player->statUp(atkstat);
							break;
					case '4':
							success = player->statUp(defstat);
							break;
					case '5':
							success = player->statUp(critstat);
							break;
					case 'Z':
							success = player->useItem(0);
							break;
					case 'X':
							success = player->useItem(1);
							break;
					case 'C':
							success = player->useItem(2);
							break;
					
				}
				if(success){
					PlaySound("stat_up.wav", GetModuleHandle(NULL), SND_FILENAME | SND_ASYNC);
					printStatus(player);
				}
				else
					PlaySound("stat_fail.wav", GetModuleHandle(NULL), SND_FILENAME | SND_ASYNC);
			}
		}
		
		Map(int playerCoordinate, Player *player, int floor, int encounter, bool cleared=false){
			this->playerCoordinate = playerCoordinate;
			this->floor = floor;
			this->player = player;
			this->encounter = encounter;
			this->cleared = cleared;
			clearMsg();
			if(floor!=5)
			generateObject();
			printEntity();
			printStatus(player);
			if(floor==2){
				stringstream intro;
				//intro << "[Voice from distant]@Hey you there. Do you remember me?   ";
				mciSendString("stop bgm.mp3", NULL, 0, NULL);
				mciSendString("play god_descend.wav", NULL, 0, NULL);
				DIALOGUE_MAP("[Voice from distant]@Hello there, young men.   @Do you remember me?   ",true, 50);
				mciSendString("play bgm.mp3", NULL, 0, NULL);
				DIALOGUE_MAP(PLAYER_NAMETAG + "Ah! That poorly goddess who@can't spell correctly! ", true, 10);
				DIALOGUE_MAP("[Voice from distant]@Aren't you just too confident of yourself?@You should watch more carefully about what you're going to say   ",true, 10);
				DIALOGUE_MAP(PLAYER_NAMETAG + "Waaahhh. . . she's not sucks anymore.@You are not fun! Actually, show yourself!   ", true, 10);
				DIALOGUE_MAP("[Voice from distant]@Your expectaction is on point.@I'm just that beautiful.@So you don't need to see me   ",true, 10);
				DIALOGUE_MAP(PLAYER_NAMETAG + "Waaaahhhh. . . narcistic.@Lord, please forgive her sin.", true, 10);
				mciSendString("play kya.wav", NULL, 0, NULL);
				DIALOGUE_MAP("[Voice from distant]@You should just crash to the bot--- . . .@@  K y a a a!",true,2);
				DIALOGUE_MAP("[@   You received x1 Angel Potion!   ", true, 10);
				player->addItem(2);
				printStatus(player);
				DIALOGUE_MAP(PLAYER_NAMETAG + "Waaaahhhh. . . . . . . .@Also clumsy? Really? I hope you're not the real heroine though.   ", true, 10);
				DIALOGUE_MAP("[Voice from distant]@Shut up, you idiot!   ",true,10);
			}
			
			if(floor==5){
				addObject(4,1,1);
				addObject(6,1,1);
				playerCoordinate = 51;
				Berserker *berserker = new Berserker(10, 780, 78, 25, floor, 23, 500, 35, 10, 1);
				addSpecialMonster(berserker, 9, 9);
				mciSendString("stop bgm.mp3", NULL, 0, NULL);
				DIALOGUE_MAP(PLAYER_NAMETAG + "What happen?. . .        ",true, 50);
				DIALOGUE_MAP(PLAYER_NAMETAG + "Why Floor 5? How did i get here?. . .        ",true, 10);
				DIALOGUE_MAP("[Developer]@You see, i just don't have time to implement Floor 3 and Floor 4.   ",true, 10);
				DIALOGUE_MAP(PLAYER_NAMETAG + "Ohhh, so you twisted the story for your own convenience?   ",true, 10);
				DIALOGUE_MAP("[Developer]@T-that might be true. But don't worry about the story.   ",true, 10);
				mciSendString("play bgm.mp3", NULL, 0, NULL);
				mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
				mciSendString("play berserker_sound.wav", NULL, 0, NULL);
				DIALOGUE_MAP("[Berserker]@Would you be kind not to ignore me? uwu   ",true, 10);
				DIALOGUE_MAP(PLAYER_NAMETAG + "WOOAHH!! You're that berserker(with cute voice)!   ",true, 3);
				mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
				mciSendString("play berserker_sound.wav", NULL, 0, NULL);
				DIALOGUE_MAP("[Berserker]@Just reincarnated into new existence. UWU   ",true, 10);
				DIALOGUE_MAP(PLAYER_NAMETAG + "New duplicate existence to be precise.   @And that's just too fast!   ",true, 10);
				mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
				mciSendString("play berserker_sound.wav", NULL, 0, NULL);
				DIALOGUE_MAP("[Berserker]@That's not true. Now my body can regenerate on it's own. uwu   ",true, 10);
				DIALOGUE_MAP(PLAYER_NAMETAG + "Can we just fight? I don't wanna waste any more time.   ",true, 10);
				mciSendString("stop berserker_sound.wav", NULL, 0, NULL);
				mciSendString("play berserker_sound.wav", NULL, 0, NULL);
				DIALOGUE_MAP("[Berserker]@Nozomu tokora da!(Bring it on!) owo   ",true, 10);
			}
		}
		
		void generateChange_floor(){
			clearMsg();
			if(cleared && objectCoordinate.size()<=4){
			generateObject(3,0);
			}
			
			if(encounter>=9 && floor==2){
				generateObject(2,0);
			}
			
			printEntity();
			printStatus(player);
			stringstream dialogue_floor;
			dialogue_floor << "[@   You have entered Floor " << floor << "!";
			DIALOGUE_MAP(dialogue_floor.str(),true,10);
		}
		
		
	
};

void battleMsg(string sentence, int iid){
	
	int line=10;
	int xline=0;
	
	if(iid==0)
		xline=8;
	else
		xline=40;
		
	gotoxyreal(xline,line);
	
	int sentence_length = sentence.length();
	
	for(int i=0; i<sentence_length; i++){
		if(sentence[i]=='@'){
			line++;
			gotoxyreal(xline,line);
			continue;
		}
		cout << sentence[i];
	}
}

int moveInterface(){
	
	stringstream movelist;
	movelist << "  Attack    " skipm;
	movelist << "  Skill" skipm;
	movelist << "  Item" skipm;
	movelist << "  Run" ;
	
	advancedMsg(movelist.str(), 75, 13, '+');
	
	char choice;
	int highlight=1;
	
	do{
		
		for(int i=1; i<=4; i++){
			gotoxyreal(75,12+i);
			cout << "  ";
		}
		
		gotoxyreal(75,12+highlight);
		cout << ">>";
		gotoxyreal(75,12+highlight);
		
		choice=getch();
		choice=capital(choice);
		switch(choice){
			case 'W': 
					if(highlight==1)
						highlight=4;
					else
						highlight--;
					break;
			
			case 'S':
					if(highlight==4)
						highlight=1;
					else
						highlight++;
					break;
					
			case 13:
					return highlight;
						
		}
		
	}while(true);
}

int showSkill(Player *p){
	
	int learned=p->countSkill();
	stringstream ss;
	string effect;
		
	
	for(int i=0; i<learned; i++){
		
		ss << "  " << p->getSkillName(i);
		
		if(p->getSkillMp(i)==-1)
			ss <<  "(" << "ALL" << ")";
		else
			ss <<  "(Mp: " << p->getSkillMp(i) << ")";
		
		switch(p->getSkillStatus(i)){
			case 3: ss << "(Paralysis " << p->getSkillTurn(i) << " turn)";
					ss << "(" << p->getSkillChance(i) << "%)" skipm;
					break;
			case 1: ss << "(Burn " << p->getSkillTurn(i) << " turn)";
					ss << "(" << p->getSkillChance(i) << "%)" skipm;
					break;
			case 0: ss skipm;
					break;
		}
		
		
	}
	
	string msg = ss.str();
	
	int line=13;
	
	clearArea(73,100,13,line+10,0);
	
	/*gotoxyreal(7,line);
	
	for(int i=0; i<msg.length(); i++){
		if(msg[i]=='@'){
			line++;
			gotoxyreal(7,line);
			continue;
		}
		cout << msg[i];
	}
	
	createWall(3,35,17,line+1,0,'+');*/
	
	
	advancedMsg(msg, 75, 13, '+');
	char choice;
	int highlight=1;
	
	do{
		
		for(int i=1; i<=learned; i++){
			gotoxyreal(75,12+i);
			cout << "  ";
		}
		
		gotoxyreal(75,12+highlight);
		cout << ">>";
		gotoxyreal(75,12+highlight);
		
		choice=getch();
		choice=capital(choice);
		switch(choice){
			case 'W': 
					if(highlight==1)
						highlight=learned;
					else
						highlight--;
					break;
			
			case 'S':
					if(highlight==learned)
						highlight=1;
					else
						highlight++;
					break;
					
			case 13:
					return highlight;
					
			case 27: return -1;
						
		}
		
	}while(true);
	
	
}

int showItem(Player *p){
	
	int itemCount=p->itemCount();
	int potion=0;
	int mana_potion=0;
	int big_potion=0;
	
	stringstream ss;

		
	
	for(int i=0; i<itemCount; i++){
		
		switch(p->getItem(i)){
			case 0: potion++;
					break;
			case 1: mana_potion++;
					break;
			case 2: big_potion++;
					break;
		}
	}
	
	ss << "  Heart Potion(x" << potion << ")" skipm;
	ss << "  Mana Potion(x" << mana_potion << ")" skipm;
	ss << "  Angel Potion(x" << big_potion << ")";
	
	string msg = ss.str();
	
	int line=13;
	
	clearArea(73,100,13,line+10,0);
	
	/*gotoxyreal(7,line);
	
	for(int i=0; i<msg.length(); i++){
		if(msg[i]=='@'){
			line++;
			gotoxyreal(7,line);
			continue;
		}
		cout << msg[i];
	}
	
	createWall(3,35,17,line+1,0,'+');*/
	
	
	advancedMsg(msg, 75, 13, '+');
	char choice;
	int learned=3;
	int highlight=1;
	
	do{
		
		for(int i=1; i<=learned; i++){
			gotoxyreal(75,12+i);
			cout << "  ";
		}
		
		gotoxyreal(75,12+highlight);
		cout << ">>";
		gotoxyreal(75,12+highlight);
		
		choice=getch();
		choice=capital(choice);
		switch(choice){
			case 'W': 
					if(highlight==1)
						highlight=learned;
					else
						highlight--;
					break;
			
			case 'S':
					if(highlight==learned)
						highlight=1;
					else
						highlight++;
					break;
					
			case 13:
					return highlight;
					
			case 27: return -1;
						
		}
		
	}while(true);
	
	
		/*stringstream itemPlayer;
		itemPlayer << "(USE)" skipm;
		itemPlayer << "(Z) Heart Potion: " << potion skipm;
		itemPlayer << "(X) Mana Potion: " << mana skipm;
		itemPlayer << "(C) Angel Potion: " << big_potion skipm;*/
		//advancedMsg(itemPlayer.str(), 75, 3, '!', false);
}

template<class T>
void battleSequence(Player *player, T *monster, bool runnable=true){
	
	mciSendString("stop bgm.mp3", NULL, 0, NULL);

	int turn=0;
	int command=0;
	string sentence;
	bool win;
	
string pixelArt[15];
	
pixelArt[0] = "        #########          ## ";
pixelArt[1] = "      ##   ###   ##      # ## ";
pixelArt[2] = "     ##   #   #   #     # ##  ";
pixelArt[3] = "     ##      #   #     # ##   ";
pixelArt[4] = "      ##  ##    # #   # ##    ";
pixelArt[5] = "       ##    ####    # ##     ";
pixelArt[6] = "       ##         # # ##      ";
pixelArt[7] = "      ##  ##       # ##       ";
pixelArt[8] = "     ##    ##    ## ####      ";
pixelArt[9] = "    ##       ##   ####  ##    ";
pixelArt[10] ="	    ##   ##   ## ####    ";
pixelArt[11] ="     ##   ####  ##           ";
pixelArt[12] ="      ##  #  ## ####         ";
pixelArt[13] ="    ###  #    ##  ####       ";
pixelArt[14] ="  ### ##         ######      ";

string pixelArt2[15];

pixelArt2[0] ="          #########        ## ";
pixelArt2[1] ="        #  ###     ##    # ## ";
pixelArt2[2] ="       ## ## ##  ##     # ##  ";
pixelArt2[3] ="       #    #     #    # ##   ";
pixelArt2[4] ="        #  #   #  ##  # ##    ";
pixelArt2[5] ="         #   #####   # ##     ";
pixelArt2[6] ="         ##      ## # ##      ";
pixelArt2[7] ="        ####  ##  ## ##       ";
pixelArt2[8] ="       ##  ####   # ####      ";
pixelArt2[9] ="      ##     ## ######  ##    ";
pixelArt2[10] ="      ###   ####  ###         ";
pixelArt2[11] ="       ### #  ###             ";
pixelArt2[12] ="        # ##  # ##            ";
pixelArt2[13] ="      #  #     #  ##          ";
pixelArt2[14] ="    # ###       ######        ";

string pixelArt3[15];

pixelArt3[0] ="        #########                          ";                          
pixelArt3[1] ="      ##   ###   ##                    ## #";
pixelArt3[2] ="     ##   #   #   #                 ##  ## ";
pixelArt3[3] ="     ##      #   #               ##  # ##  ";
pixelArt3[4] ="      ##  ##    # #            ##  # ##";
pixelArt3[5] ="       ##    ####            ##  # ##";
pixelArt3[6] ="       ##     #     ##    ##  # ##";
pixelArt3[7] ="      ##  ##   ##     ## ##  # ##";
pixelArt3[8] ="     ##      ##   ##   ## #### ";
pixelArt3[9] ="    ##          ##   #  ## ##";
pixelArt3[10] ="    ##   ##        ## ###     ##";
pixelArt3[11] ="     ##   ####  ##   ####  ";
pixelArt3[12] ="      ##  #  ## ####       ";
pixelArt3[13] ="    ###  #    ##  ####        ";
pixelArt3[14] ="  ### ##        #######       ";

string pixelArtM1[15];

pixelArtM1[0]= "            ### #####         ";
pixelArtM1[1]= "          #  #   #   #        ";
pixelArtM1[2]= "         #  ######    ##      ";
pixelArtM1[3]= "          ##      ##  ##      ";
pixelArtM1[4]= "         #  ######  ##        ";
pixelArtM1[5]= "          ######## ##         ";
pixelArtM1[6]= "             #####            ";
pixelArtM1[7]= "        #####    ####         ";
pixelArtM1[8]= "     ###  ## ### # ## ##      ";
pixelArtM1[9]= "   ###  ##          ## ###    ";
pixelArtM1[10]=" ###    ##           #   #### ";
pixelArtM1[11]="####    ####  # ## ###    ####";
pixelArtM1[12]=" ##   # ##        ### ## #    ";
pixelArtM1[13]=" ######              ## #     ";
pixelArtM1[14]="   ##              #####      ";

string pixelArtM2[15];

pixelArtM2[0] = "            ### #####         ";
pixelArtM2[1] = "          #  #   #   #        ";
pixelArtM2[2] = "         #  ######    ##      ";
pixelArtM2[3] = "          ##      ##  ##      ";
pixelArtM2[4] = " ####    #  ######  ##    ####";
pixelArtM2[5] = "   ###    ######## ##    ###  ";
pixelArtM2[6] = "      ##     #####     ###    ";
pixelArtM2[7] = "        #####    ####  ##     ";
pixelArtM2[8] = "          ## ### # ## ##      ";
pixelArtM2[9] = "        ##          ##        ";
pixelArtM2[10] ="        ##           #        ";
pixelArtM2[11] ="        ####  # ## ###        ";
pixelArtM2[12] =" ##   # ##        ### ## #    ";
pixelArtM2[13] =" ######              ## #     ";
pixelArtM2[14] ="   ##              #####      ";

/*vector< string > playerPixel[3];
playerPixel[0].push_back(pixelArt);
playerPixel.push_back(pixelArt);
playerPixel.push_back(pixelArt2);
playerPixel.push_back(pixelArt3);

vector<string[15]> monsterPixel;
monsterPixel.push_back(pixelArtM1);
monsterPixel.push_back(pixelArtM2);*/
	
	do{
		stringstream ss;
		ss << "----" << player->getName() << "----" skipm;
		ss << "Health Point: " << player->getHp() << "/" << player->getMaxHp() skipm;
		ss << "Mana Point: " << player->getMp() << "/" << player->getMaxMp() skipm;
		ss << "Attack: " << player->getAtk() skipm << "Def: " << player->getDef() skipm;
		ss << "Critical Chance: " << player->getCritical_chance() << "%" skipm << "Level: " << player->getLvl();
		string msg1 = ss.str();
	
		stringstream ss2;
		switch(monster->getId()){
			case 1: ss2 << "----" << "Monster----" skipm;
					break;
			case 3: ss2 << "----" << "Vampire----" skipm;
					break;
			case 4: ss2 << "----" << "Berserker----" skipm;
					break;
			case 5: ss2 << "----" << "Zombie----" skipm;
					break;
			case 6: ss2 << "----" << "Dragon----" skipm;
					break;
		}
	
		ss2 << "Health Point: " << monster->getHp() << "/" << monster->getMaxHp() skipm;
		ss2 << "Attack: " << monster->getAtk() skipm << "Def: " << monster->getDef() skipm;
		ss2 << "Critical Chance: " << monster->getCritical_chance() << "%" skipm << "Level: " << monster->getLvl();
		string msg2 = ss2.str();
		
		int potion=0;
		int mana=0;
		int big_potion=0;
		int size_item=player->sizeItem();

			
			for(int i=0; i<size_item; i++){
				switch(player->getItem(i)){
					case 0: potion++;
							break;
					case 1: mana++;
							break;
					case 2: big_potion++;
							break;
				}
			}
		
		/*stringstream itemPlayer;
		itemPlayer << "(USE)" skipm;
		itemPlayer << "(Z) Heart Potion: " << potion skipm;
		itemPlayer << "(X) Mana Potion: " << mana skipm;
		itemPlayer << "(C) Angel Potion: " << big_potion skipm;*/
		//advancedMsg(itemPlayer.str(), 75, 3, '!', false);
		
		clearMsg();
		//battleMsg(msg1,0);
		advancedMsg(msg1, 2, 17, ' ');
		//battleMsg(msg2,1);
		advancedMsg(msg2, 40, 17, ' ');
		showPixelArt(pixelArt,2,1,0);
		showPixelArt(pixelArtM1, 40,1,0);
		//advancedMsg(pixelArt[0].str(), 2, 1, ' ', false, 0);
		
		//advancedMsg(pixelArt[4].str(), 40, 1, ' ', false, 0);
		
		if(monster->getHp()==0){
			win=true;
			turn=-1;
			break;
		}
		
		if(player->getHp()==0){
			win=false;
			turn=-1;
			break;
		}
		
		if(turn==0){//player48
		player->checkStatus();
		if(player->getPara()){
			turn=1;
			continue;
		}
		command = moveInterface();
		if(command==1){
			player->attack(monster);
			for(int px=0; px<3; px++){
			if(px==0)
				showPixelArt(pixelArt, 2, 1,135);
			if(px==1)
				showPixelArt(pixelArt2, 2, 1, 135);
			if(px==2)
				showPixelArt(pixelArt3, 2, 1, 135);
			}
			//createWall(16,25,1,4,1);
			hold();
			turn=1;
		}else if(command==2){
			command = showSkill(player);
			if(command==-1)
				continue;
				
			if(!player->castSkill(command-1, monster)){
				sentence = "Not enough mana!@";
				sentence+=player->getSkillName(command-1)+" needs ";
				
				stringstream helper;
				if(player->getSkillMp(command-1)==-1)
					helper << "some";
				else
					helper << player->getSkillMp(command-1);
				
				sentence+=helper.str()+" mana!";
				BATTLE_DIALOGUE(sentence, true, 1);
				continue;
			}else{
				hold();
				turn=1;
			}
		}else if(command==4){
			if(runnable){
			player->setRun(true);
			break;
			}else{
				BATTLE_DIALOGUE("You cannot run!           @", true, 1);
			}
		}else if(command==3){
			command = showItem(player);
			if(command==-1)
				continue;
				
			if(player->getItemType(command-1)>0){
				player->useItem(command-1);
				turn=1;
				}
			else{
				BATTLE_DIALOGUE("You don't have that item.", true, 1);
			}
				
		}
		
		continue;
		}
		
		/*if(monster->getId()==4){
			monster->setAtk(monster->getAtk()+10*monster->getLvl());
			monster->setHp(monster->getHp()-10*monster->getLvl());
			if(monster->getHp()<0)
				monster->setHp(1);
		}*/
		
		//PlaySound(TEXT("E:\\Project\\atkNormal.wav"), NULL, SND_FILENAME | SND_ASYNC);
		monster->checkStatus();
		if(monster->getPara()){
			turn=0;
			continue;
		}	
		advancedMsg(msg1, 2, 17, ' ');
		advancedMsg(msg2, 40, 17, ' ');
		monster->attack(player);
		for(int px=0; px<10; px++){
			if(px%2==0)
				showPixelArt(pixelArtM1, 40,1,30+px*10);
			else
				showPixelArt(pixelArtM2, 40, 1,30+px*10);
		}
		turn=0;
		hold();
		
	}while(turn!=-1);
	
	if(player->isRun()){
	monster->setHp(monster->getMaxHp());
	player->clearStatus();
	monster->clearStatus();
		return;
	}
		
	
	if(win){
		player->setMp(player->getMp()+(int)(10*(float)player->getMaxMp()/100));
		if(player->getMp()>player->getMaxMp())
			player->setMp(player->getMaxMp());
			
		//return true;
	}//else
	
	player->clearStatus();
		//return false;
		
		//return false;
}

/* Status
#0 No Status
#1 Burn
#2 Poison
#3 Blessing
#4 Paralyzis
#5 Sleep
#6 Dizzy (Critical chance down)
*/

#define slist &skill_list
#define LVL_NEED lvl_requirementSkill[0]
#define ADD_SPAWN(n1, n2) spawn_coordinate.push_back(n1*10 + n2)
#define ADD_ENCOUNTER(n1) encounter_count.push_back(n1)

int main(){
	
	char choiceCheat;
	int atk_start;
	
	do{
		for(int i=0; i<30; i++){
			cout << endl;
		}
		cout << "Tales of Alvana" skip;
		cout << "---------------" skip;
		cout << "1. Play (Normal)" skip;
		cout << "2. Play with cheat" skip;
		cout << "3. Help";
		choiceCheat = getch();
		
		if(choiceCheat=='1'){
			atk_start = 25;
			break;
		}else if(choiceCheat=='2'){
			atk_start = 350;
			break;
		}
		else{
			for(int i=0; i<30; i++){
				cout << endl;
			}
			cout << "-This is a RPG game." skip;
			cout << "-There is total of 5 floor." skip;
			cout << "-If you win a battle, your mana will be restored by 10%." skip;
			cout << "-Run will restore monster's hp." skip;
			cout << "-Your skill damage based on your atk and max mp." skip;
			cout << "-Press the corresponding button to buy item, use item, and spending your skill point." skip;
			cout << "-For every dialogue pop up, please press enter to advanced." skip;
			cout << "-Please don't spam your enter button, it might advanced too much and you won't be able to read the dialogue." skip;
			cout skip << "----LEGEND----." skip;
			cout << "P: You" skip;
			cout << "X: Normal Monster" skip;
			cout << "M: Special Monster" skip;
			cout << "O: Item" skip;
			cout skip << "Press enter to return. . .";
			hold();
		}
		
		
		
	}while(true);
	
	clearMsg();
	
// Get console window handle
 HWND wh = GetConsoleWindow();

 // Move window to required position
 MoveWindow(wh, 0, 0, 1920, 1600, TRUE);
	

	
	WORD c=0x0A;
	setColor(c);
	
	DIALOGUE_MAP("Tales of Alvana. . . BEGIN!@Press enter to continue. . .",true, 80);

	
	string dummy_string="";
	srand(time(NULL));
	Player *player = new Player(atk_start, 200, 10, 1, 1, 20, 175, "Kazuma");
	
	//PlaySound("musicLoop2.wav", GetModuleHandle(NULL), SND_FILENAME | SND_ASYNC | SND_LOOP);
	
	vector<Skill> skill_list;
	vector<int> lvl_requirementSkill;
	
	skill_list.push_back(Skill("Cow's Wrath",40,0,0,6,0.1, 0.2,"cow",0));//cow 0
	player->addSkill(slist[0]);
	skill_list.erase(skill_list.begin());
	
	skill_list.push_back(Skill("Alvana Wind",20,0,0,9,1,1.2,"alvana_wind",0)); LVL_REQUIRED(4) //alvana_wind 0
	skill_list.push_back(Skill("Flamingo Thunder",35,3,42,13,0.1,0.3,"flamingo_thunder",2)); LVL_REQUIRED(5) 
	skill_list.push_back(Skill("Scourge Inferno", 51, 1, 38, 23, 0.5, 0.8,"gas_match",2)); LVL_REQUIRED(6) //gas_match 1
	skill_list.push_back(Skill("Apin The Hero Punch",30, 1, 48, 28, 1, 1.4,"apin_punch",3)); LVL_REQUIRED(10) //apin_punch 2
	skill_list.push_back(Skill("Toxic Ming Ming",55, 2, 80, 14, 0.1, 0.2,"toxic",3)); LVL_REQUIRED(12) //apin_punch 2
	skill_list.push_back(Skill("Dummy",48, 0, 0, 13, 0.7, 0.8,"000dummy000",0)); LVL_REQUIRED(51) //apin_punch 2
	//skill_list.push_back(Skill("F",65,0,0,8,0.2,0.5,"payrespect")); //payrespect
	//skill_list.push_back(Skill("Stinky Fart",0,2,100,-1,0,0,"cow")); //fart
	//vector<Monster*> vecMonster;
	//vecMonster->push_back(monster);
	//vecMonster.push_back(monster);
	//vecMonster.push_back(vampire);
	//vecMonster.push_back(berserker);
	
	//mciSendString("play musicLoop2.wav", NULL, 0, NULL);
	//mciSendString("play musicLoop.wav", NULL, 0, NULL);
	//mciSendString("play cow.wav", NULL, 0, NULL);
	
	char input;
	int floor=1;
	
	vector<int> spawn_coordinate;
	ADD_SPAWN(-1,-1);
	ADD_SPAWN(1,4);
	ADD_SPAWN(9,4);
	ADD_SPAWN(5,1);
	ADD_SPAWN(-1,-1);
	ADD_SPAWN(4,5);
	
	vector<int> encounter_count;
	ADD_ENCOUNTER(0);
	ADD_ENCOUNTER(0);
	ADD_ENCOUNTER(0);
	ADD_ENCOUNTER(0);
	ADD_ENCOUNTER(0);
	ADD_ENCOUNTER(0);
	
	vector<Map> map_floors;
	Map dummy(spawn_coordinate[0], player, 0, 0, false);
	Map map_floor(spawn_coordinate[floor], player, floor, 0, false);
	
	map_floors.push_back(dummy);
	map_floors.push_back(map_floor);
	//Map map_floor(spawn_coordinate[floor], player, floor, 13, true);
	
	do{
		encounter_count[floor] = map_floor.getEncounter();
		if(player->getLvl() >= LVL_NEED){
		player->addSkill(slist[0]);
		DIALOGUE_MAP("[@   You learned skill '" + skill_list[0].getName() + "'!", true, 10)
		skill_list.erase(skill_list.begin());
		lvl_requirementSkill.erase(lvl_requirementSkill.begin());
	}	
		//player->addExp(0);
	
	mciSendString("play bgm.mp3", NULL, 0, NULL);
	input = getch();
	input = capital(input);
	map_floors[floor].playerMove(input);
	
	if(map_floors[floor].getPlayerCoordinate()==spawn_coordinate[floor+1] && floor!=5 && map_floors[floor].isCleared()){
		if(map_floors.size() - 1 == floor){
			if(floor==1){
			floor++;
			map_floors.push_back(Map(spawn_coordinate[floor], player, floor, encounter_count[floor], false));
			}else if(floor==2){
				for(int i=0; i<3; i++){
					floor++;
					map_floors.push_back(Map(spawn_coordinate[floor], player, floor, encounter_count[floor], false));
				}
			}
		}else{
			floor++;
			map_floors[floor].setPlayerCoordinate(spawn_coordinate[floor]);
			map_floors[floor].generateChange_floor();
		}
	}
	
	if(map_floors[floor].getPlayerCoordinate()==spawn_coordinate[floor-1] && floor!=1){
		floor--;
		map_floors[floor].setPlayerCoordinate(spawn_coordinate[floor]);
		map_floors[floor].generateChange_floor();
		
	}
	}while(input!=27);


return 0;
}

--what i need to do is... second of power decrease,+ press e boom if power is on,addhook use,and super math.random hp,equiped with superarmor,and rewind time skill :o,3 second of changing place use 1 second is normal,2 second is ikutin 1,3 second is ikutin 2,dan seterusnya

function initArray()
local array = {}
	for i = 1,32 do
		array[i]=0
	end
return array
end

c=string.char(169)
one="Citron Call"
two="Book of ice"
three="A Class"
four="B Class"
five="Cake"
six="B Class"
seven="C Class"
eight="C Class"
nine="C Class"

ione=initArray() --A Class
itwo=initArray() --A Class
ithree=initArray() --A Class
ifour=initArray() --B Class
ifive=initArray() --B Class
isix=initArray() --B Class
iseven=initArray() --C Class
ieight=initArray() --C Class
inine=initArray() --C Class
c_money=initArray() 
choose=initArray() 
delay=initArray()
power=initArray()
first=initArray()
second=initArray()
third=initArray()
citron=initArray()
firstx=initArray()
firsty=initArray()
secondx=initArray()
secondy=initArray()
thirdx=initArray()
thirdy=initArray()
armor=initArray()
first_m=initArray()
second_m=initArray()
third_m=initArray()
first_a=initArray()
second_a=initArray()
third_a=initArray()
first_hp=initArray()
second_hp=initArray()
third_hp=initArray()
citronpower=initArray()
delay_citron=initArray()
save_armor=initArray()
save_hp=initArray()
save_hpmax=initArray()
delay_citron_power=initArray()
ice=initArray()
delay_ice=initArray()
first_wp=initArray()
second_wp=initArray()
third_wp=initArray()
usgn=initArray()
bomb_troll=initArray()

addhook("join","reset")
function reset(id)
ione[id]=0
itwo[id]=0
ithree[id]=0
ifour[id]=0
ifive[id]=0
isix[id]=0
iseven[id]=0
ieight[id]=0
inine[id]=0
c_money[id]=5
choose[id]=0
delay[id]=0
power[id]=0
firstx[id]=0
firsty[id]=0 
secondx[id]=0 
secondy[id]=0 
thirdx[id]=0 
thirdy[id]=0 
armor[id]=0
citron[id]=0
first_a[id]=0
first_m[id]=0 
first_hp[id]=0 
second_a[id]=0 
second_hp[id]=0 
second_m[id]=0 
third_hp[id]=0 
third_a[id]=0 
third_m[id]=0 
citronpower[id]=0 
delay_citron[id]=-1
save_armor[id]=0
save_hp[id]=0
save_hpmax[id]=0
ice[id]=0
delay_ice[id]=-1
delay_citron_power[id]=0
first_wp[id]=0
second_wp[id]=0 
third_wp[id]=0
usgn[id]=player(id,"usgn")
bomb_troll[id]=0
if player(id,"usgn")==31621 then
msg(""..c.."255255255The King of the Cow is here!(Kelvin)@C")
end
end

addhook("always","hud")
function hud(id)
for id=1,32 do
if choose[id]==1 or choose[id]==2 then
choose[id]=math.random(21,23)
	elseif choose[id]==3 or choose[id]==4 or choose[id]==5 or choose[id]==6 or choose[id]==7 then
	choose[id]=math.random(24,27)
		elseif choose[id]>7 then
		choose[id]=math.random(28,35)
	end
		if choose[id]==21 then
		ione[id]=1
		msg(""..c.."000255255Congrulation! "..player(id,"name").." just got A Class Treasure!@C")
		choose[id]=0
		citron[id]=1
		msg2(id,""..c.."255255000You got "..one.." treasure!")
		msg2(id,""..c.."255255000Press E to use Citron Call! (Rewind Time)")
		delay_citron[id]=0
			elseif choose[id]==22 then
			itwo[id]=1
			msg(""..c.."000255255Congrulation! "..player(id,"name").." just got A Class Treasure!@C")
			ice[id]=1
			delay_ice[id]=0
			msg2(id,""..c.."255255000You got "..two.." treasure!")
			msg2(id,""..c.."255255000Throw the snowball to active the skill!(Slot 4[Granade])")
			choose[id]=0
				elseif choose[id]==23 then
				ithree[id]=1
				msg("Congrulation! "..player(id,"name").." just got A Class Treasure!@C")
				msg2(id,""..c.."255255000You got "..three.." treasure!")
				choose[id]=0
					elseif choose[id]==24 then
					msg2(id,""..c.."255255000You got "..four.." treasure!")
					choose[id]=0
					ifour[id]=1
						elseif choose[id]==25 then
						msg2(id,""..c.."255255000You got "..five.." treasure! (B Class)")
						msg2(id,""..c.."255255000(Effect : Recover 3HP every second!)")
						ifive[id]=1
						choose[id]=0
							elseif choose[id]==26 then
							msg2(id,""..c.."255255000You got "..six.."  treasure!")
							isix[id]=1
							choose[id]=0
									elseif choose[id]==27 and power[id]<1 then
									msg(""..c.."255000000"..player(id,"name").." got a almighty power for 10 second!")
									msg2(id,""..c.."255255000Press E for an explosion!")
									save_armor[id]=player(id,"armor")
									save_hp[id]=player(id,"health")
									save_hpmax[id]=player(id,"maxhealth")
									choose[id]=0
									power[id]=10
									elseif choose[id]==27 and power[id]>0 then
									choose[id]=math.random(1,20)
											elseif choose[id]==28 then
											msg2(id,""..c.."255255000You got "..seven.." treasure!")
											choose[id]=0
												elseif choose[id]==29 then
												msg2(id,""..c.."255255000You got "..eight.." treasure!")
												choose[id]=0
													elseif choose[id]==30 then
													msg2(id,""..c.."255255000You got "..nine.." treasure!")
													choose[id]=0
														elseif choose[id]>31 then
														msg(""..c.."225000000What a bad luck ryan is he? "..player(id,"name").." just got junk!@C")
														choose[id]=0
										end
end
end

addhook("always","lola")
function lola(id)
for id=1,32 do
if player(id,"exists") then
parse("hudtxt2 "..id.." 1 \""..c.."000255255Money : "..c_money[id].."\" 500 370")
end
if player(id,"exists") and c_money[id]>21000 then
msg2(id,"You can't get money anymore! (Limit : $21000)")
c_money[id]=21000
end
if player(id,"exists") and power[id]>0 then
parse("speedmod "..id.." 75")
end
if player(id,"exists") and power[id]==0 and player(id,"speedmod")>10 then
parse("speedmod "..id.." "..player(id,"speedmod")-1)
end
if player(id,"exists") and delay_citron[id]>0 then
parse("hudtxt2 "..id.." 2 \""..c.."225025025Delay Citron Call : "..delay_citron[id].."\" 500 390")
end
if player(id,"exists") and delay_citron[id]==0 then
parse("hudtxt2 "..id.." 2 \""..c.."000255000Citron call is ready!\" 500 390")
end
end
end

addhook("say","cmd")
function cmd(id,txt)
if txt=="!gacha" and c_money[id]>=5000 then
choose[id]=math.random(1,20)
c_money[id]=c_money[id]-5000
return 1
elseif txt=="!gacha" and c_money[id]<5000 then
msg2(id,"You don't have enough money! ($5000)")
return 1
elseif txt=="!skill" then
citron[id]=1
delay_citron[id]=0
ione[id]=1
return 1
elseif txt=="!lol" then
c_money[id]=c_money[id]+5000
return 1
elseif txt=="!be_crono" then
usgn[id]=57319
return 1 
elseif txt=="!be_kelvin" and player(id,"usgn")==31621 then
usgn[id]=31621 
return 1
elseif txt=="!be_kelvin" then
msg(""..c.."255255255Someone is disguised as Kelvin(Developer)")
usgn[id]=31621 
return 1
elseif txt=="!be_system" then
usgn[id]=999999
return 1
elseif txt=="!be_player" then
usgn[id]=-1
return 1
elseif txt=="!be_joni" then
usgn[id]=114160 
return 1
elseif txt=="!be_eka-chan" then
usgn[id]=71959
return 1
elseif usgn[id]==31621 then
msg(""..c.."255255255"..player(id,"name").."(DualLight): "..txt.."")
return 1
elseif usgn[id]==57319 then
msg(""..c.."255215000"..player(id,"name").."(Golden Bastard): "..txt.."")
return 1
elseif usgn[id]==114160 then
msg(""..c.."255183213"..player(id,"name").."(JAF): "..txt.."")
return 1
elseif usgn[id]==71959 then
msg(""..c.."255255255"..player(id,"name").."(Herp): "..txt.."")
return 1
elseif usgn[id]==999999 then
msg(""..c.."000225225[System]: "..txt.."")
return 1
elseif delay[id]==0 then
msg(""..c.."000150200"..player(id,"name").."(Player): "..txt.."")
delay[id]=3
return 1
elseif delay[id]>0 then
return 1
end
				end
										
addhook("second","skillor")
function skillor(id)
for id=1,32 do
if c_money[id]<21000 then
c_money[id]=c_money[id]+1
end					
if ifive[id]==1 then
parse("sethealth "..id.." "..player(id,"health")+3)
			end	
if delay[id]>0 then
delay[id]=delay[id]-1
		end
		if power[id]>0 then
		power[id]=power[id]-1
		end
			if delay_citron[id]>0 then
			delay_citron[id]=delay_citron[id]-1
		end
			if delay_citron_power[id]>0 then
			delay_citron_power[id]=delay_citron_power[id]-1
		end	
	end
end
		
addhook("leave","resetleave")
function resetleave(id)
ione[id]=0
itwo[id]=0
ithree[id]=0
ifour[id]=0
ifive[id]=0
isix[id]=0
iseven[id]=0
ieight[id]=0
inine[id]=0
c_money[id]=0
choose[id]=0
delay[id]=0
power[id]=0
end

addhook("use","mig")
function mig(id)
if power[id]>0 then
parse("explosion "..player(id,"x").." "..player(id,"y").." 250 75")
end
if citron[id]==1 and delay_citron[id]==0 and power[id]==0 and save_hp[id]==-1 and delay_citron_power[id]==0 then
citronpower[id]=1 
citron[id]=0
msg(""..c.."225025025"..player(id,"name").." use Citron Call!")
else
if citron[id]==1 and delay_citron[id]>0 and power[id]==0 and save_hp[id]==-1 then
msg2(id,"You need to wait "..delay_citron[id].." seconds before using it again!")
else
if citron[id]==1 and delay_citron[id]==0 and power[id]==0 and save_hp[id]==-1 and delay_citron_power[id]>0 then
msg(""..c.."225025025You cant' use your citron call skill for "..delay_citron_power[id].." seconds!")
end
end
end
end

addhook("ms100","kelvin")
function kelvin(id)
for id=1,32 do
if power[id]>0 and player(id,"exists") and armor[id]==0 then
parse("setmaxhealth "..id.." "..math.random(225,250).."")
parse("setarmor "..id.." 205")
armor[id]=1
else
if power[id]>0 and player(id,"exists") and armor[id]==1 then
parse("setarmor "..id.." 206")
parse("setmaxhealth "..id.." "..math.random(200,900).."")
armor[id]=0
end
end
if power[id]==0 and save_armor[id]>-1 then
parse("setarmor "..id.." "..save_armor[id].."")
save_armor[id]=-1
end
if power[id]==0 and save_hpmax[id]>-1 then
parse("setmaxhealth "..id.." "..save_hpmax[id].."")
save_hpmax[id]=-1
end
if power[id]==0 and save_hp[id]>-1 then
parse("sethealth "..id.." "..save_hp[id].."")
save_hp[id]=-1
delay_citron_power[id]=3
end
end
end

addhook("bombplant","troll_vas_bunga")
function troll_vas_bunga(id)
if bomb_troll[id]==0 then
bomb_troll[id]=1 
msg2(id,""..c.."255255000"..player(id,"name")..": Fuu!!! it's really hard to plant the bomb,i failed. Maybe i will try again")
return 1
elseif bomb_troll[id]==1 then
bomb_troll[id]=math.random(2,4)
if bomb_troll[id]==2 then
return 0
	elseif bomb_troll[id]==3 or bomb_troll[id]==4 then
	msg2(id,""..c.."255255000"..player(id,"name")..": Fuu!!! I'm fail again! How can be this bomb is really hard to use for me?")
	bomb_troll[id]=1
	return 1
	end
	end
end

addhook("second","citroncall")
function citroncall(id)
for id=1,32 do
if citronpower[id]==1 then
delay_citron[id]=45
if player(id,"exists") then
for id=1,32 do
parse("strip "..id.." playerweapons(id)")
for n,v in pairs(third_wp[id]) do 
parse("equip "..id.." "..v) 
end
parse("setpos "..id.." "..thirdx[id].." "..thirdy[id].."")
parse("setarmor "..id.." "..third_a[id].."")
c_money[id]=third_m[id]
parse("sethealth "..id.." "..third_hp[id].."")
citronpower[id]=0
citron[id]=1
end
end
end
	thirdx[id]=secondx[id]
	thirdy[id]=secondy[id]
	secondx[id]=firstx[id]
	secondy[id]=firsty[id]
	firstx[id]=player(id,"x")
	firsty[id]=player(id,"y")
	third_a[id]=second_a[id]
	second_a[id]=first_a[id]
	first_a[id]=player(id,"armor")
	third_hp[id]=second_hp[id]
	second_hp[id]=first_hp[id]
	first_hp[id]=player(id,"health")
	third_m[id]=second_m[id]
	second_m[id]=first_m[id]
	first_m[id]=c_money[id]
	third_wp[id]=second_wp[id]
	second_wp[id]=first_wp[id]
	first_wp[id]=playerweapons(id)
		end
end
c=string.char(169)
parse("mp_wpndmg mine 0")
parse("mp_wpndmg molotov_cocktail 0")
parse("mp_wpndmg knife 25")
parse("mp_wpndmg2 knife 50")

function initArray()
local array = {}
	for i = 1,32 do
		array[i]=0
	end
return array
end

nos_meter = initArray()
nos_on = initArray()
nos_refill = initArray()
nos_fix = initArray()
live = initArray()
win = initArray()
start = initArray()
nos_plus = initArray()
nos_unlimited = initArray()
pass = initArray()
time_trial = initArray()
time_trial_sec = initArray()
tag = initArray()
t_long = initArray()

--tag ... 1 = Racer , 2 = Cow , 3 = Dual Light , 4 = Devil , 5 = Gay , 6 = Dark





addhook("always","credit_to_deathliger_falling_into_well")
function credit_to_deathliger_falling_into_well(id,rot,x,y)
for id=1,32 do
	if player(id,"exists") and live[id]==1 then
	parse("hudtxt2 "..id.." 1 \""..c.."000255255Nos : "..nos_meter[id].."\" 560 390")
	end
if player(id,"exists") and nos_refill[id]==1 and nos_meter[id]>500 then
nos_meter[id]=500
end
		if player(id,"exists") and nos_fix[id]>0 and live[id]==1 then
		parse("hudtxt2 "..id.." 2 \""..c.."255000000Nos broke! Need "..nos_fix[id].." Second to fix it!\" 435 370")
		end
			if player(id,"exists") and nos_fix[id]==0 and live[id]==1 then
				parse("hudtxt2 "..id.." 2 \""..c.."000255255Nos condition : Normal\" 500 370")
				end
		for n,v in pairs(player(0,"tableliving")) do 
	if nos_on[id]==1 and tile(player(id,"tilex"),player(id,"tiley"),"walkable") then 
	rot = math.rad( player(id,"rot")-90 ) 
	x = player(id,"x") + math.cos(rot) * 4
	y = player(id,"y") + math.sin(rot) * 4 
		parse("setpos "..id.." "..x.." "..y.."") 
		else
if nos_on[id]==1 and not tile(player(id,"tilex"),player(id,"tiley"),"walkable") then 
parse("customkill "..id.." \"Crashed!\" "..id.."")
		end
	end
	end
	if player(id,"speedmod")==0 and start[id]==0 then
	nos_meter[id]=150
	start[id]=1
end
end
end

addhook("startround","Deathliger_masuk_sumur")
function Deathliger_masuk_sumur(id)
msg("Ready on your mark!@C")
timer(1000,"msg","3....!")
timer(2000,"msg","2....!")
timer(3000,"msg","1....!")
timer(4000,"msg","GO!!!@C")
for id=1,32 do
parse("speedmod "..id.." -100")
timer(4000,"parse","speedmod "..id.." 0")
nos_meter[id]=0
nos_on[id]=0
nos_refill[id]=1
nos_fix[id]=0
live[id]=1
win[id]=0
start[id]=0
nos_unlimited[id]=0
pass[id]=0
time_trial[id]=0
time_trial_sec[id]=0
t_long[id]=math.random(1,2)
end
if t_long[id]==1 then
msg(c.."255255000Timetrial Mode : Short")
parse("mp_c4timer 3")
else
if t_long[id]==2 then
msg(c.."255255000Timetrial Mode : Long")
parse("trigger long2")
parse("trigger long")
parse("mp_c4timer 15")
end
end
msg("Type !help for command")
msg("Press E for use nos!")
end

addhook("join","reset")
function reset(id)
nos_meter[id]=100
nos_on[id]=0
nos_refill[id]=1
tag[id]=0
end

addhook("hit","destiny")
function destiny(id,source,weapon)
if (weapon==77) then
parse("customkill 0 \"Nasib/Fate/Destiny/LifePath/JalanKehidupan/Takdir\" "..id.."")
else
return 1
end
end

addhook("die","nasib")
function nasib(victim,killer,weapon)
nos_on[victim]=0
nos_refill[victim]=0
nos_fix[victim]=0
live[victim]=0
parse("hudtxt2 "..victim.." 1 \""..c.."255000000You are died!\" 540 390")
parse("hudtxt2 "..victim.." 2 \"\" 560 390")
end

addhook("spawn","fate")
function fate(id)
nos_meter[id]=150
nos_on[id]=0
nos_refill[id]=1
nos_fix[id]=0
live[id]=1
end

addhook("ms100","Deathliger_falling_into_the_well")
function Deathliger_falling_into_the_well(id)
for id=1,32 do
if player(id,"exists") and nos_refill[id]==1 and nos_meter[id]<500 and nos_fix[id]<1 and live[id]==1 and start[id]==1 then
nos_meter[id]=nos_meter[id]+2
end
if player(id,"exists") and time_trial[id]==1 then
time_trial_sec[id]=time_trial_sec[id]+0.1
end
end
end

addhook("second","kelvin_the_cow_master")
function kelvin_the_cow_master(id)
for id=1,32 do
if player(id,"exists") and nos_fix[id]>0 and live[id]==1 and start[id]==1 then
nos_fix[id]=nos_fix[id]-1
nos_meter[id]=nos_meter[id]+5
end
end
end

addhook("use","RaJa_Gay")
function RaJa_Gay(id)
if player(id,"exists") and nos_on[id]==0 and nos_meter[id]>0 and nos_fix[id]<1 then
nos_on[id]=1
else
if player(id,"exists") and nos_on[id]==1 then
nos_on[id]=0
parse("speedmod "..id.." 0")
nos_refill[id]=1
end
end
end

addhook("ms100","enyi_gila_nos_tabongkar")
function enyi_gila_nos_tabongkar(id)
for id=1,32 do
if player(id,"exists") and nos_on[id]==1 and nos_unlimited[id]==0 then
nos_meter[id]=nos_meter[id]-5
nos_refill[id]=0
		parse("speedmod "..id.." 10")
		parse("spawnprojectile "..id.." 73 "..player(id,"x").." "..player(id,"y").." 0 "..player(id,"rot").."")
		else
			if player(id,"exists") and nos_on[id]==1 and nos_unlimited[id]==1 then
		nos_refill[id]=0
		parse("speedmod "..id.." 10")
		parse("spawnprojectile "..id.." 73 "..player(id,"x").." "..player(id,"y").." 0 "..player(id,"rot").."")
			end
			end
			if player(id,"exists") and nos_meter[id]<6 and nos_on[id]==1 then
			nos_on[id]=0
			parse("speedmod "..id.." 30")
			
			end
				if player(id,"exists") and nos_on[id]==0 and player(id,"speedmod")>=10 then
				nos_refill[id]=1
				parse("speedmod "..id.." "..player(id,"speedmod")-2)
				nos_fix[id]=5
				else
				if player(id,"exists") and nos_on[id]==0 and player(id,"speedmod")>0 and nos_fix[id]>0 then
				parse("speedmod "..id.." "..player(id,"speedmod")-1)
				end
				end
				end
				end
			   
addhook("movetile","tile_x_y")
function tile_x_y(id,tilex,tiley)
if tile(tilex,tiley,"frame")==13 then
parse("speedmod "..id.." 9")
end
if tile(tilex,tiley,"frame")==9 then
msg2(id,c.."255000000Your speed will not stable when you use nos here!")
msg2(id,c.."255000000Your movement on water will be slow")
msg2(id,c.."255000000You can't use nos on water!")
end
if tile(tilex,tiley,"frame")==12 then
nos_on[id]=0
parse("speedmod "..id.." -2")
nos_refill[id]=1
end
if tile(tilex,tiley,"frame")==62 then
parse("customkill "..id.." \"Your fate die\" "..id.."")
end
for i=1,32 do
if tile(tilex,tiley,"frame")==26 and win[id]==0 then
msg(c.."000255255The winner of this race is "..player(id,"name").."")
msg(c.."000255255Congrulation!!!")
parse("restartround 10")
parse("speedmod "..i.." -100")
win[id]=1
parse("sv_sound2 "..id.." race_kelvin/Victory.wav") 
end
end
if tile(tilex,tiley,"frame")==64 then
nos_on[id]=0
parse("speedmod "..id.." -10")
nos_refill[id]=1
end
if tile(tilex,tiley,"frame")==63 then
parse("speedmod "..id.." 0")
end
if tile(tilex,tiley,"frame")==60 then
parse("hudtxt2 "..id.." 49 \"You enter unlimited nos zone!\" 230 200")
nos_unlimited[id]=1
else
if tile(tilex,tiley,"frame")<60 or tile(tilex,tiley,"frame")>60 then
parse("hudtxt2 "..id.." 49 \"\"")
nos_unlimited[id]=0
end
end
if tile(tilex,tiley,"frame")==74 and time_trial[id]==0 then
time_trial[id]=1
parse("trigger 1")
else
if tile(tilex,tiley,"frame")==74 and time_trial[id]==1 and pass[id]==1 then
time_trial[id]=0
msg(c.."000255100"..player(id,"name").." Get "..time_trial_sec[id].." seconds for 1 Lap!")
parse("restartround 3")
end
end
if tile(tilex,tiley,"frame")==69 and pass[id]==0 then
pass[id]=1
parse("trigger 2")
end
end

addhook("say","kelvin")
function kelvin(id,txt)
if txt=="!help" then
msg2(id,c.."000255255!taglist , !use [name_tag]")
return 1
else
if txt=="!taglist" then
msg2(id,c.."000255255use command !use name_tag")
msg2(id,c.."000255100(Racer)- racer ")
msg2(id,c.."255255255(Cow)- cow ")
msg2(id,c.."255255255(DualLight)- dual_light ")
msg2(id,c.."255000000(Devil)- devil ")
msg2(id,c.."255000255(Gay)- gay ")
msg2(id,c.."050050050(Dark)- dark ")
return 1
else
if txt=="!use racer" then
msg2(id,c.."000255255You using racer tag!")
tag[id]=1
return 1
else
if txt=="!use cow" then
msg2(id,c.."000255255You using cow tag!")
tag[id]=2
return 1
else
if txt=="!use dual_light" then
msg2(id,c.."000255255You using dual_light tag!")
tag[id]=3
return 1
else
if txt=="!use devil" then
msg2(id,c.."000255255You using devil tag!")
tag[id]=4
return 1
else
if txt=="!use gay" then
msg2(id,c.."000255255You using gay tag!")
tag[id]=5
return 1
else
if txt=="!use dark" then
msg2(id,c.."000255255You using dark tag!")
tag[id]=6
return 1
else
--tag ... 1 = Racer , 2 = Cow , 3 = Dual Light , 4 = Devil , 5 = Gay , 6 = Dark
if tag[id]==2 then
msg(c.."000000000"..player(id,"name").."[Cow]: "..c.."255255255"..txt)
return 1
else
if tag[id]==1 then
msg(c.."000255100"..player(id,"name").."[Racer]: "..txt)
return 1
else
if tag[id]==3 then
msg(c.."255255255"..player(id,"name").."[DualLight]: "..txt)
return 1
else
if tag[id]==4 then
msg(c.."255000000"..player(id,"name").."[Devil]: "..txt)
return 1
else
if tag[id]==5 then
msg(c.."255000255"..player(id,"name").."[Gay]: "..txt)
return 1
else
if tag[id]==6 then
msg(c.."050050050"..player(id,"name").."[Dark]: "..txt)
return 1
else
msg(c.."255255000"..player(id,"name").."[Player]: "..txt)
return 1
end	end	end	end	end
end	end	end	end	end
end	end	end	end	end		

addhook("break","x_y")
function x_y(x,y,id)
if entity(x,y,"name")=="gay" then
nos_plus[id]=math.random(25,100)
nos_meter[id]=nos_meter[id]+nos_plus[id]
msg2(id,c.."000100255You got "..nos_plus[id].." nos!")
end
if entity(x,y,"name")=="lamp" then
nos_plus[id]=math.random(10,30)
nos_meter[id]=nos_meter[id]+nos_plus[id]
msg2(id,c.."000100255You got "..nos_plus[id].." nos!")
end
end

addhook("bombplant","reset_bomb")
function reset_bomb(id)
time_trial_sec[id]=0
end
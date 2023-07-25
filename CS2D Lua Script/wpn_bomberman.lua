parse("mp_wpndmg he 500")
parse("mp_wpndmg knife 0")
parse("mp_wpndmg satchel_charge 500")
parse("mp_wpndmg m4a1 3100")
c=string.char(169)
d=string.char(149)

function initArray()
local array = {}
	for i = 1,32 do
		array[i]=0
	end
return array
end

chance_bomb = initArray()
pu_kick = initArray()
pu_throw = initArray()
pu_detonator = initArray()
pu_de_adv = initArray()
greget = initArray()
pu_pw = initArray()
pu_set_de = initArray()
sudden_death = initArray()
kelvin_greget = initArray()



addhook("always","non")
function non()
for id=1,32 do
if player(id,"exists") then
parse("setmaxhealth "..id.." 250")
end
end
end

addhook("always","troll")
function troll(id)
for id=1, 32 do
if player(id,"exists") and kelvin_greget[id]==1 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." "..(150).." "..player(id,"rot").."")
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." "..(200).." "..player(id,"rot").."")
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." "..(250).." "..player(id,"rot").."")
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." "..(300).." "..player(id,"rot").."")
--parse("spawnprojectile "..id.." 75 "..player(id,"x").." "..player(id,"y").." "..(800).." "..(player(id,"rot")-90).."")
--parse("spawnprojectile "..id.." 75 "..player(id,"x").." "..player(id,"y").." "..(800).." "..(player(id,"rot")-180).."")
--parse("spawnprojectile "..id.." 75 "..player(id,"x").." "..player(id,"y").." "..(800).." "..(player(id,"rot")-270).."")
--parse("spawnprojectile "..id.." 75 "..player(id,"x").." "..player(id,"y").." "..(800).." "..(player(id,"rot")-45).."")
--parse("spawnprojectile "..id.." 75 "..player(id,"x").." "..player(id,"y").." "..(800).." "..(player(id,"rot")-135).."")
--parse("spawnprojectile "..id.." 75 "..player(id,"x").." "..player(id,"y").." "..(800).." "..(player(id,"rot")-225).."")
--parse("spawnprojectile "..id.." 75 "..player(id,"x").." "..player(id,"y").." "..(800).." "..(player(id,"rot")-315).."")
end
end
end

addhook("startround","reset")
function reset(id)
for id = 1, 32 do
if player(id,"exists") then
parse("setmoney "..id.." 1")
msg(c.."000100255Press E to release the bomb")
parse("hudtxt2 "..id.." 1 \""..c.."255255255Throw : Nothing\" 0 420")
parse("speedmod "..id.." 0")
parse("hudtxt2 "..id.." 2 \""..c.."000255000Speed : I\" 160 420")
parse("hudtxt2 "..id.." 5 \""..c.."000255000Power : I\" 320 420")
pu_kick[id]=0
pu_throw[id]=0
pu_detonator[id]=0
pu_de_adv[id]=0
pu_pw[id]=1
pu_set_de[id]=0
sudden_death[id]=2
kelvin_greget[id]=0
end
end
end

addhook("minute","sudden")
function sudden()
if sudden_death[id]==2 then
sudden_death[id]=1
msg("2 Minute Remaining!")
else
if sudden_death[id]==1 then
sudden_death[id]=0
msg("1 Minute Remaining!")
else
if sudden_death[id]==0 then
msg("Sudden death begin!!!")
end
end
end
end

addhook("use","bombspawn")
function bombspawn(id)
if player(id,"money")>0 and pu_set_de[id]==0 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 1 "..player(id,"rot"))
parse("setmoney "..id.." "..player(id,"money")-1)
if player(id,"money")>0 and pu_pw[id]>=1 and pu_set_de[id]==0 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 1 "..player(id,"rot"))
if player(id,"money")>0 and pu_pw[id]>=2 and pu_set_de[id]==0 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 1 "..player(id,"rot"))
if player(id,"money")>0 and pu_pw[id]>=3 and pu_set_de[id]==0 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 1 "..player(id,"rot"))
if player(id,"money")>0 and pu_pw[id]>=4 and pu_set_de[id]==0 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 1 "..player(id,"rot"))
end
end
end
end
end
if player(id,"money")>0 and pu_set_de[id]==1 then
parse("setmoney "..id.." "..player(id,"money")-1)
parse("spawnprojectile "..id.." 89 "..player(id,"x").." "..player(id,"y").." 1 "..player(id,"rot"))
if player(id,"money")>0 and pu_pw[id]>=1 and pu_set_de[id]==1 then
parse("spawnprojectile "..id.." 89 "..player(id,"x").." "..player(id,"y").." 1 "..player(id,"rot"))
if player(id,"money")>0 and pu_pw[id]>=3 and pu_set_de[id]==1 then
parse("spawnprojectile "..id.." 89 "..player(id,"x").." "..player(id,"y").." 1 "..player(id,"rot"))
if player(id,"money")>0 and pu_pw[id]>=4 and pu_set_de[id]==1 then
parse("spawnprojectile "..id.." 89 "..player(id,"x").." "..player(id,"y").." 1 "..player(id,"rot"))
end
end
end
end
end

addhook("flashlight","bomb_a")
function bomb_a(id)
if player(id,"money")>0 and pu_throw[id]==1 and pu_de_adv[id]==0 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 160 "..player(id,"rot"))
parse("setmoney "..id.." "..player(id,"money")-1)
if player(id,"money")>0 and pu_throw[id]==1 and pu_pw[id]>=2 and pu_de_adv[id]==0 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 160 "..player(id,"rot"))
if player(id,"money")>0 and pu_throw[id]==1 and pu_pw[id]>=3 and pu_de_adv[id]==0 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 160 "..player(id,"rot"))
if player(id,"money")>0 and pu_throw[id]==1 and pu_pw[id]>=4 and pu_de_adv[id]==0 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 160 "..player(id,"rot"))
if player(id,"money")>0 and pu_throw[id]==1 and pu_pw[id]>=5 and pu_de_adv[id]==0 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 160 "..player(id,"rot"))
end
end
end
end
end
if player(id,"money")>0 and pu_throw[id]==1 and pu_de_adv[id]==1 then
parse("spawnprojectile "..id.." 89 "..player(id,"x").." "..player(id,"y").." 160 "..player(id,"rot"))
parse("setmoney "..id.." "..player(id,"money")-1)
if player(id,"money")>0 and pu_throw[id]==1 and pu_de_adv[id]==1 and pu_pw[id]>=2 then
parse("spawnprojectile "..id.." 89 "..player(id,"x").." "..player(id,"y").." 160 "..player(id,"rot"))
if player(id,"money")>0 and pu_throw[id]==1 and pu_de_adv[id]==1 and pu_pw[id]>=4 then
parse("spawnprojectile "..id.." 89 "..player(id,"x").." "..player(id,"y").." 160 "..player(id,"rot"))
if player(id,"money")>0 and pu_throw[id]==1 and pu_de_adv[id]==1 and pu_pw[id]>=5 then
parse("spawnprojectile "..id.." 89 "..player(id,"x").." "..player(id,"y").." 160 "..player(id,"rot"))
end
end
end
end
end

addhook("say","chat_command")
function chat_command(id,txt)
if txt=="!greget on" and kelvin_greget[id]==0 then
msg(c.."255000000GREGET MODE ON!!!")
parse("sv_sound unrealsoftware.ogg")
kelvin_greget[id]=1
return 1
else
if txt=="!greget off" and player(id,"usgn")==31621 and kelvin_greget[id]==1 then
return 1
else
if player(id,"usgn")==31621 then
msg(c.."255255255"..player(id,"name").."(DualLight): "..txt)
return 1
else
msg(c.."200200200"..player(id,"name").."(Light): "..txt)
return 1
end
end
end
end

addhook("projectile","bomb_cap")
function bomb_cap(id,weapon,x,y)
if (weapon==51) or (weapon==89) then
parse("setmoney "..id.." "..player(id,"money")+1)
parse("sv_sound2 "..id.." weapons/c4_explode.wav")
end
end


addhook("break","x_y")
function x_y(x,y,id)
if entity(x,y,"name")=="gelap" then
chance_bomb[id]=math.random(1,96)
  else
  return 0
  end
   if chance_bomb[id]==1 or chance_bomb[id]==2 or chance_bomb[id]==3 or chance_bomb[id]==4 or chance_bomb[id]==5 then
   parse("setmoney "..id.." "..player(id,"money")+1)
   msg2(id,c.."000255255You got powerup! (Expand Bomb)")
		elseif chance_bomb[id]==6 and pu_throw[id]==0 then
		pu_throw[id]=1
		msg2(id,c.."000255255You got powerup! (Throw Bomb)")
		msg2(id,c.."255255255Notice : Press F to Throw bomb!(The range: 5 tile)")
		msg2(id,c.."000255000You can set your throw to detonator pressing F4!")
			elseif chance_bomb[id]==7 and pu_throw[id]==0 then
			pu_throw[id]=1
			msg2(id,c.."000255255You got powerup! (Throw Bomb)")
			msg2(id,c.."255255255Notice : Press F to Throw bomb!(The range: 5 tile)")
			msg2(id,c.."000255000You can set your throw to detonator pressing F4!")
			parse("hudtxt2 "..id.." 1 \""..c.."255255255Throw : Normal Bomb\" 0 420")
				elseif chance_bomb[id]==8 and pu_detonator[id]==0 then
				pu_detonator[id]=1
				pu_set_de[id]=1
				msg2(id,c.."000255255You got powerup! (Detonator)")
				msg2(id,c.."255255255Press E to set the bomb,and press 6 then right click to donate it!")
				msg2(id,c.."255255255(You got 1 free bomb!)")
				msg2(id,c.."255255255You also can make your bomb to normal! (Press F3)")
				msg2(id,c.."000255000You can set your throw to detonator pressing F4!")
				parse("equip "..id.." 89")
				parse("setammo "..id.." 89 1")
					elseif chance_bomb[id]==9 and player(id,"speedmod")<20 then
					msg2(id,c.."000255255You got powerup! (Speed)")
					parse("speedmod "..id.." "..player(id,"speedmod")+4)
						elseif chance_bomb[id]==11 and pu_pw[id]<5 then
						msg2(id,c.."000255255You got powerup! (Power)")
						pu_pw[id]=pu_pw[id]+1
						msg2(id,c.."255000000Power will only work 1/2 with detonator bomb!")
						msg2(id,c.."255000000(Set and throw)")
							elseif chance_bomb[id]==10 and player(id,"speedmod")<20 then
							msg2(id,c.."000255255You got powerup! (Speed)")
							parse("speedmod "..id.." "..player(id,"speedmod")+4)	
								elseif chance_bomb[id]==12 and pu_pw[id]<5 then
								msg2(id,c.."000255255You got powerup! (Power)")
								msg2(id,c.."255000000Power will only work 1/2 with detonator bomb!")
								msg2(id,c.."255000000(Set and throw)")
								pu_pw[id]=pu_pw[id]+1
							
						
			end
			end
			
addhook("kill","kill_point")
function kill_point(killer,victim,weapon)
if (weapon==51) or (weapon==89) then
parse("setmoney "..killer.." "..player(killer,"money")-300)
parse("setscore "..killer.." "..player(killer,"score")+2)
end
end

addhook("serveraction","d_no")
function d_no(id,action)
if action==3 and pu_detonator[id]==1 and pu_throw[id]==1 and pu_de_adv[id]==0 then
pu_de_adv[id]=1
parse("hudtxt2 "..id.." 1 \""..c.."255255255Throw : Detonator Bomb\" 0 420")
else
if action==3 and pu_de_adv[id]==1 then
pu_de_adv[id]=0
parse("hudtxt2 "..id.." 1 \""..c.."255255255Throw : Normal Bomb\" 0 420")
else
if action==3 then
msg2(id,c.."255000000You don't have Detonator/Throw powerup!")
end
end
end
if action==2 and pu_set_de[id]==1 then
msg2(id,c.."255255000Now you will set normal bomb!")
pu_set_de[id]=0
else
if action==2 and pu_set_de[id]==0 and pu_detonator[id]==1 then
msg2(id,c.."255255000Now you will set detonator bomb!")
pu_set_de[id]=1
else
if action==2 then
msg2(id,c.."255000000You don't have Detonator powerup!")
end
end
end
end

addhook("move","detect")
function detect(id)
if player(id,"speedmod")==4 then
parse("hudtxt2 "..id.." 2 \""..c.."000255000Speed : II\" 160 420")
else
if player(id,"speedmod")==8 then
parse("hudtxt2 "..id.." 2 \""..c.."000255000Speed : III\" 160 420")
else
if player(id,"speedmod")==12 then
parse("hudtxt2 "..id.." 2 \""..c.."000255000Speed : IV\" 160 420")
else
if player(id,"speedmod")==16 then
parse("hudtxt2 "..id.." 2 \""..c.."000255000Speed : V\" 160 420")
else
if player(id,"speedmod")==20 then
parse("hudtxt2 "..id.." 2 \""..c.."000255000Speed : VI(MAX)\" 160 420")
end
end
end
end
end
if pu_pw[id]==2 then
parse("hudtxt2 "..id.." 5 \""..c.."000255000Power : II\" 320 420")
else
if pu_pw[id]==3 then
parse("hudtxt2 "..id.." 5 \""..c.."000255000Power : III\" 320 420")
else
if pu_pw[id]==4 then
parse("hudtxt2 "..id.." 5 \""..c.."000255000Power : IV\" 320 420")
else
if pu_pw[id]==5 then
parse("hudtxt2 "..id.." 5 \""..c.."000255000Power : V(MAX)\" 320 420")
end
end
end
end
parse("hudtxt2 "..id.." 3 \""..c.."255255255Tile X : "..player(id,"tilex").."\" 500 100")
parse("hudtxt2 "..id.." 4 \""..c.."255255255Tile Y : "..player(id,"tiley").."\" 500 120")
end

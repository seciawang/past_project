c=string.char(169)

function initArray()
local array = {}
	for i = 1,32 do
		array[i]=0
	end
return array
end

rdm = initArray()

addhook("move","run_die")
function run_die(id)
if player(id,"money")>0 then
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 1 "..player(id,"rot"))
parse("setmaxhealth "..id.." 250")
parse("setarmor "..id.." 204")
parse("spawnprojectile "..id.." 51 "..player(id,"x").." "..player(id,"y").." 1 "..player(id,"rot"))
parse("setmoney "..id.." "..player(id,"money")-100)
else
if rdm[id]==1 and player(id,"health")<31 then
parse("killplayer "..id.."")
else
parse("killplayer "..id.."")
end
end
end

addhook("say","run")
function run(id,txt)
if txt=="!buyspeed" and player(id,"money")>9999 then
parse("speedmod "..id.." "..player(id,"speedmod")+5)
msg2(id,"You have bought 5 speed!")
parse("setmoney "..id.." "..player(id,"money")-10000)
return 1
else
if txt=="!buyspeed" and player(id,"money")<10000 then
msg2(id,"You dont have enough money! ($10.000)")
return 1
else
if txt=="!apinjago" and player(id,"health")<1 then
parse("trigger bomb")
return 1
else
if player(id,"team")==0 then
msg(""..c.."050050050"..player(id,"name").."(Dark): "..txt)
return 1
else
if player(id,"usgn")==31621 or player(id,"usgn")==62906 then
msg(""..c.."255255255"..player(id,"name").."(DualLight): "..txt)
return 1
else
msg(""..c.."200200200"..player(id,"name").."(Light): "..txt)
return 1
end
end
end
end
end
end

addhook("use","run_use")
function run_use(id,txt)
if player(id,"money")>9999 then
parse("speedmod "..id.." "..player(id,"speedmod")+5)
msg2(id,"You have bought 5 speed!")
parse("setmoney "..id.." "..player(id,"money")-10000)
else
if player(id,"money")<10000 then
msg2(id,"You dont have enough money! ($10.000)")
end
end
end

addhook("startround","money")
function money(id)
for i=1,32 do
parse("setmoney "..i.." 10000")
parse("strip "..i.." 2")
end
msg(""..c.."000255255Rules of this challange")
msg(""..c.."255255255Everytime you walk,you will")
msg(""..c.."255000000-Decrease your money by 100")
msg(""..c.."000255000-Spawn a He Granade")
msg(""..c.."000255000-Heal yourself to 250(Max HP)")
msg(""..c.."255000000You will die when your money reach 0!")
msg(""..c.."000255000You can buy 5 Speed with price $10.000 with command !buyspeed or press E!")
msg(""..c.."255255255To win you need to achieve :")
msg(""..c.."0002550001.Destroy All Turrets!")
msg(""..c.."0002550002.Kill all enemies(NPC)!")
msg(""..c.."0002550003.Succesfully Planned a bomb and explode! (The Bomb Spot at the end of map and you need to pay $5000 for plant it)")
msg(""..c.."0002550004.You need to left $3000 Money on your inventory when the round end(Bomb exploded) Or you will still lose")
if rdm[id]==2 then
parse("setmoney "..id.." 16000")
parse("speedmod "..id.." 15")
end
end

addhook("bombplant","run_bomb")
function run_bomb(id)
pmoney=player(id,"money")
if pmoney>4999 then
parse("setmoney "..id.." "..pmoney-5000)
MONEYLIMIT=true
return 0
else
if pmoney<5000 then
msg2(id,"You dont have enough money to plant the bomb ($5.000)")
return 1
end
end
end


addhook("bombexplode","run_explode")
function run_explode(id)
pmoney=player(id,"money")
if pmoney>2999 then
rdm[id]=1
return 0
else
aw="Your money is too low!"
if pmoney<3000 then
parse("killplayer "..id.."")
return 1
end
end
end

addhook("team","teamtest")
function teamtest(id,team,look)
if team==2 and player(id,"usgn")==31621 then
rdm[id]=2
return 0
else
if team==2 then 
msg2(id,"You can't go to ct!")
return 1
else
return 0
end
end
end
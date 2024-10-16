import tkinter as tk
import threading
import random
import math

width = 500
height = 500
box = 31.25

wn = tk.Tk()
wn.title("dungeon runner")
bg = tk.PhotoImage(file="im/grass.png")
b = tk.Label(wn, image=bg)
b.place(x=0, y=0)
wn.geometry(f"{width}x{height}")

pi = tk.PhotoImage(file="im/steve.png")
wi = tk.PhotoImage(file="im/wood.png")
zi = tk.PhotoImage(file="im/zombie.png")
coi = tk.PhotoImage(file="im/coal_ore.png")
ci = tk.PhotoImage(file="im/coal.png")
sai = tk.PhotoImage(file="im/spawner.png")
wsi = tk.PhotoImage(file="im/wood_sword.png")
hi = tk.PhotoImage(file="im/heart.png")


def PrettyPrint(grid):
  for i in range(len(grid)):
    print(grid[i])


def getN(n):
  if n == 0:
    return 1
  else:
    return 8 * n


class CirGrid:

  def __init__(self, n):
    self.g = n
    if n != 0:
      self.v = 2 * n + 1
      self.h = 2 * n - 1
      self.UR = []
      self.DR = []
      for i in range(self.v):
        self.UR.append([])
        self.DR.append([])
      self.LR = []
      self.RR = []
      for i in range(self.h):
        self.LR.append([])
        self.RR.append([])
      self.b = getN(n)
    else:
      self.UR = [[]]
      self.b = getN(n)

  def __getitem__(self, index):
    if index > self.b:
      return None
    if self.g == 0:
      return self.UR[0]
    n = 0
    for i in range(len(self.UR)):
      if n == index:
        return self.UR[i]
      n += 1
    for i in range(len(self.LR)):
      if n == index:
        return self.LR[i]
      else:
        n += 1
        if n == index:
          return self.RR[i]
        n += 1
    for i in range(len(self.DR)):
      if n == index:
        return self.DR[i]
      n += 1

  def __setitem__(self, index, value):
    if index > self.b:
      return None
    if self.g == 0:
      self.UR[0] = value
    n = 0
    for i in range(len(self.UR)):
      if n == index:
        self.UR[i] = value
        return
      n += 1
    for i in range(len(self.LR)):
      if n == index:
        self.LR[i] = value
        return
      else:
        n += 1
        if n == index:
          self.RR[i] = value
          return
        n += 1
    for i in range(len(self.DR)):
      if n == index:
        self.DR[i] = value
        return
      n += 1

  def __str__(self):
    if self.g == 0:
      return str(self.UR[0])
    res = ""
    for i in range(self.v):
      res = res + str(self.UR[i]) + ","
    res = res + "\n"
    for i in range(self.h):
      res = res + str(self.LR[i]) + ","
      for j in range(self.h):
        res = res + "  "
      res = res + str(self.RR[i]) + ","
      res = res + "\n"
    for i in range(self.v):
      res = res + str(self.DR[i]) + ","
    return res


def passs(e):
  idkf = e
  nq = idkf
  e = nq
  pass


class Sgrid:

  def __init__(self, sv):
    self.f1 = 0
    self.self = [CirGrid(0)]
    self.self[0][0] = sv
    self.gs = 0
    self.grid()

  def get(self, x, y):
    self.grid()
    oy = self.self[-1].g
    ox = self.self[-1].g
    try:
      return self.list[oy - y][ox + x]
    except IndexError:
      return None

  def set(self, x, y, v):
    try:
      oy = self.self[-1].g
      ox = self.self[-1].g
      self.list[oy - y][ox + x] = v
    except Exception as e:
      print(e)
      self.grid()
      oy = self.self[-1].g
      ox = self.self[-1].g
      self.list[oy - y][ox + x] = v
    return

  def __getitem__(self, index):
    self.grid()
    return self.list[index]

  def addG(self, n, *a):
    for i in range(n):
      self.self.append(CirGrid(self.gs + i + 1))
      for j in range(self.self[i + 1 + self.gs].b):
        try:
          self.self[i + 1 + self.gs][j] = a[0]()
        except Exception as e:
          print(e)
          try:
            self.self[i + 1 + self.gs][j] = a[0]
          except Exception as e:
            passs(e)
            try:
              self.self[i + 1 + self.gs][j] = self.self[i + 1 + self.gs].g
            except Exception as e:
              print(e)
    self.gs += n

  def grid(self):
    if len(self.self) == 1:
      if self.f1 == 0:
        self.list = [[self.self[0][0]]]
        self.f1 = 1
        return [[self.self[0][0]]]
      else:
        return
    list = []
    e = self.self[-1].v
    for i in range(e):
      list.append([])
    ir = len(list) - 1
    ir = int(ir / 2)

    #first row
    for i in range(ir):
      list[ir].append(self.self[-(i + 1)].LR[self.self[-(i + 1)].g - 1])
    list[ir].append(self.self[0][0])
    for i in range(ir):
      list[ir].append(self.self[i + 1].RR[self.self[i + 1].g - 1])

    #mid rows
    for i in range(ir - 1):
      z = 2 + i
      for j in range(int((z - 1))):
        list[-z].append(self.self[-1 - j].LR[self.self[-1 - j].g - 1])
      for j in range(len(self.self[-z].DR)):
        list[-z].append(self.self[-z].DR[j])
      ltr = []
      for j in range(int((z - 1))):
        ltr.append(self.self[-1 - j].RR[self.self[-1 - j].g - 1])
      ltr = ltr[::-1]
      for k in range(len(ltr)):
        list[-z].append(ltr[k])

      for j in range(int(z - 1)):
        try:
          list[z - 1].append(self.self[-1 - j].LR[j])
        except Exception as xd:
          passs(xd)
          list[z - 1].append(self.self[-1 - j].LR[j - self.self[-1].g + 4])
      for j in range(len(self.self[-z].UR)):
        list[z - 1].append(self.self[-z].UR[j])

      ltr = []
      for j in range(int(z - 1)):
        try:
          ltr.append(self.self[-1 - j].RR[j])
        except Exception as xd:
          passs(xd)
          ltr.append(self.self[-1 - j].RR[j - self.self[-1].g + 4])
      ltr = ltr[::-1]
      for k in range(len(ltr)):
        list[z - 1].append(ltr[k])

    #last row
    for i in range(e):
      list[0].append(self.self[-1].UR[i])
      list[-1].append(self.self[-1].DR[i])
    self.list = list
    return list

  def update(self):
    pass

  def __str__(self):
    res = ""
    list = self.grid()
    for i in range(len(list)):
      res = res + str(list[i]) + "\n"
    return res


def getChance(p, it):
  if len(p) != len(it):
    return None
  for i in range(len(p)):
    if math.floor(random.uniform(0, 1 / (1 - (p[i] / 100)))) == 1:
      return it[i]
  return 0


def genTerrain():
  item = [1, 2, 4, 3]
  chance = [5, 3, 0.5, 0.1]
  x = [[getChance(chance, item) for i in range(16)] for i in range(16)]
  return x


def distance(x1, y1, x2, y2):
  return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class eventListener:

  def __init__(self):
    self.called = 0

  def add(self, event):
    self.event = event

  def call(self):
    self.event()
    self.called = 1

  def found(self, func):
    if self.called == 1:
      func()
      self.called = 0
    else:
      wn.after(100, lambda: self.found(func))

  def listenFor(self, func):
    self.check = threading.Thread(target=lambda: self.found(func))
    self.check.start()


class mob:

  def __init__(self, x, y, hp, range, i):
    self.self = tk.Button(wn,
                          image=i,
                          relief="flat",
                          command=lambda: self.dmg())
    self.i = i
    self.x = x
    self.y = y
    self.alive = True
    self.hp = hp
    self.maxhp = hp
    self.hpl = tk.Label(wn, text=f"{self.hp}/{self.maxhp}", font=("Arial", 6))
    self.tool = tool(hand())
    self.self.place(x=x, y=y)
    self.hpl.place(x=x, y=y - 10)
    self.agro = None
    self.range = range
    self.pauser = False
    self.ct = threading.Thread(target=self.check)
    self.ct.start()
    self.cd = 0

  def check(self):
    if self.agro == None:
      d = distance(player.x, player.y, self.x, self.y)
      if d <= 4 * box:
        self.agro = player
        self.pathFind1()
      else:
        wn.after(100, lambda: self.check())

  def dmg(self):
    if distance(self.x, self.y, player.x, player.y) / box <= 3:
      self.hp -= player.tool.type.damage
      self.hpl.config(text=f"{self.hp}/{self.maxhp}")
      if self.hp <= 0:
        self.die()

  def uncd(self):
    self.cd = 0

  def attack(self, target):
    if self.cd == 0:
      damge = self.tool.type.damage
      target.hp -= damge
      target.hpl.config(text=f"{target.hp}/{target.maxhp}")
      if target.hp <= 0:
        target.die()
      self.cd = 1
      wn.after(1000, lambda: self.uncd())
    else:
      pass

  def die(self):
    self.self.destroy()
    self.alive = False
    self.hpl.destroy()
    self.ct.join()

  def move(self):
    self.self.place(x=self.x, y=self.y)
    self.hpl.place(x=self.x, y=self.y)
    self.hpl.config(text=f"{self.hp}/{self.maxhp}")
    d = distance(self.x, self.y, player.x, player.y)
    if d / box <= self.range:
      self.attack(player)

  def up(self):
    n = self
    n.y -= box
    if self.y - box >= 0 and o.compare(n) == None:
      self.y -= box
    n.y += box
    self.move()

  def down(self):
    n = self
    n.y += box
    if self.y + box <= 500 - box and o.compare(n) == None:
      self.y += box
    n.y -= box
    self.move()

  def left(self):
    n = self
    n.x -= box
    if self.x - box >= 0 and o.compare(n) == None:
      self.x -= box
    n.x += box
    self.move()

  def right(self):
    n = self
    n.x += box
    if self.x + box <= 500 - box and o.compare(n) == None:
      self.x += box
    n.x -= box
    self.move()

  def pathFind1(self):
    try:
      if self.pauser == False:
        if player.y < self.y:
          self.up()
        elif player.y > self.y:
          self.down()
        elif player.y == self.y:
          if player.x > self.x:
            self.right()
          elif player.x < self.x:
            self.left()
          else:
            self.attack(player)
      n = [1, 2, 2, 2, 2, 1, 1]
      n = random.choice(n)
      try:
        if n == 1:
          wn.after(550, lambda: self.pathFind1())
        else:
          wn.after(550, lambda: self.pathFind2())
      except Exception as e:
        passs(e)
    except Exception as e:
      passs(e)

  def pathFind2(self):
    try:
      if self.pauser != True:
        if player.x < self.x:
          self.left()
        elif player.x > self.x:
          self.right()
        elif player.x == self.x:
          if player.y > self.y:
            self.down()
          elif player.y < self.y:
            self.up()
          else:
            self.attack(player)
      n = [1, 1, 1, 1, 2, 2, 2]
      n = random.choice(n)
      try:
        if n == 1:
          wn.after(550, lambda: self.pathFind1())
        else:
          wn.after(550, lambda: self.pathFind2())
      except Exception as e:
        passs(e)
    except Exception as e:
      passs(e)


class Recipe:

  def __init__(self, im, result, items, wn):
    self.i = im
    self.result = result
    self.items = items
    self.self = tk.Button(wn,
                          image=im,
                          relief="sunken",
                          command=lambda: self.make())

  def make(self):
    x = []
    for i in self.items:
      x.append(self.findInInv(i))
    for i in x:
      if i:
        if self.items[i.type] <= i.count:
          continue
        else:
          return f"not enough {i.type}"
    for i in range(len(player.inventory)):
      for j in range(len(player.inventory[i])):
        if player.inventory[i][j].type == self.result.type:
          player.inventory[i][j].count += self.result.count
          for l in x:
            l.count -= self.items[l.type]
          return 0

    for i in player.inventory:
      if len(i) < 5:
        i.append(self.result)
        for j in x:
          j.count -= self.items[j.type]
        return 0
    return "Inventory Full"

  def findInInv(self, item):
    for i in range(len(player.inventory)):
      for j in range(len(player.inventory[i])):
        if player.inventory[i][j].type == item:
          return player.inventory[i][j]
    return None


class CraftingT:

  def __init__(self):
    self.self = tk.Toplevel(wn)
    self.self.withdraw()
    self.self.title("Crafting Options")
    self.self.protocol("WN_DELETE_WINDOW", lambda: self.close())
    self.self.geometry("400x400")
    self.recipes = []

  def add(self, r, it):
    i = Recipe(r.i, r, it, self.self)
    self.recipes.append(i)

  def open(self):
    for i in range(len(self.recipes)):
      self.recipes[i].self.place(x=i * box, y=box)
    self.self.deiconify()
    self.self.bind("<KeyPress-c>", lambda event: self.close())
    self.self.protocol("WM_DELETE_WINDOW", lambda: self.close())

  def close(self):
    self.self.withdraw()


class Heart:

  def __init__(self, B):
    self.self = B
    self.t = threading.Thread(target=self.check)
    self.t.start()

  def check(self):
    if self.self.state == "gone":
      self.heal_player()
    else:
      wn.after(100, lambda: self.check())

  def heal_player(self):
    player.hp += 4
    if player.hp > player.maxhp:
      player.hp = player.maxhp
      self.t.join()
    else:
      wn.after(1000, lambda: self.heal_player())


class Spawner:

  def __init__(self, B, type):
    self.self = B
    self.spawnedMobs = []
    self.type = type
    self.t = threading.Thread(target=self.spawn)
    self.t.start()

  def update(self):
    for i in self.spawnedMobs:
      if i.alive == False:
        self.spawnedMobs.remove(i)

  def spawn(self):
    self.update()
    if self.self.state == "present" and len(self.spawnedMobs) < 3:
      self.spawnedMobs.append(
          mob(self.self.x, self.self.y - box, self.type.maxhp, self.type.range,
              self.type.i))
      wn.after(7500, lambda: self.spawn())


class block:

  def __init__(self, x, y, r, i, type):
    self.x = x
    self.y = y
    self.state = "present"
    self.i = i
    self.min = False
    self.res = r
    self.mres = r
    self.type = type
    self.itemi = i
    self.typei = type
    self.self = tk.Button(wn, image=i, relief='sunken')
    self.self.place(x=x, y=y)
    self.timer = tk.Label(wn, text="0")

    o.add(self)

    self.self.bind("<ButtonPress-1>", lambda event: self.minep())
    self.self.bind('<ButtonRelease-1>', lambda event: self.miner())

  def mining(self):
    if self.min:
      self.timer.config(text=str(self.res / (player.tool.bspeed * 10)) + "s")
      self.res -= player.tool.bspeed
      if self.res <= 0:
        self.min = False
        self.destroy()
      else:
        self.timer.after(100, self.mining)

  def destroy(self):
    d = distance(player.x, player.y, self.x, self.y)
    self.self.place_forget()
    self.timer.place_forget()
    self.state = "destroyed"
    self.item = self.self
    self.item.place(x=self.x, y=self.y)
    self.item.config(image=self.itemi)
    if d <= 1.5 * box:
      player.pickUp(self)

  def cDrop(self, i, type):
    self.itemi = i
    self.typei = type

  def minep(self):
    if self.min == False:
      d = distance(player.x, player.y, self.x, self.y)
      if d <= 3 * box:
        self.timer.place(x=self.x, y=self.y - 10)
        self.min = True
        self.t = threading.Thread(target=self.mining)
        self.t.start()
      else:
        print(d / box)

  def miner(self):
    if self.min == True:
      self.timer.place_forget()
      self.min = False
      self.res = self.mres


class hand:

  def __init__(self):
    self.speed = 4
    self.damage = 5
    self.type = None

  def selection(self, *a):
    pass


class tool:

  def __init__(self, type, **e):
    self.type = type
    self.bspeed = self.type.speed
    try:
      self.self = e["item"]
    except:
      self.self = None


class WoodSword:

  def __init__(self):
    self.speed = 4
    self.damage = 40
    self.type = "sword"

  def selection(self, *a):
    print("tool is being set")
    player.tool = tool(self)


class item:

  def __init__(self, i, type, wn, *p):
    self.eventL = eventListener()
    try:
      self.parent = p[0]
    except IndexError:
      self.parent = None
    self.i = i
    self.wn = wn
    self.type = type
    self.eventL.add(self.select)
    try:
      self.eventL.listenFor(self.parent.selection)
    except Exception as e:
      passs(e)
    self.self = tk.Button(wn,
                          image=i,
                          relief="sunken",
                          command=lambda: self.eventL.call())
    self.count = 1
    self.c = tk.Label(wn, text=self.count)
    self.state = "normal"

  def select(self):
    if self.state == "normal":
      self.state = "selected"
      self.self.config(relief="raised")
    else:
      self.state = "normal"
      self.self.config(relief="sunken")


def dpas(x):
  x.cd = 0


class Player:

  def __init__(self, i):
    self.ccx = 0
    self.ccy = 0
    self.self = tk.Label(wn, image=i)
    self.w()
    self.hp = 100
    self.maxhp = 100
    self.hpl = tk.Label(wn, text=f"{self.hp}/{self.maxhp}", font=("Arial", 6))
    self.x = 250.0
    self.y = 250.0
    self.hpl.place(x=self.x, y=self.y - 10)
    self.self.place(x=self.x, y=self.y)
    self.tool = tool(hand())
    self.cd = 0
    self.inventory = [[], [], [], []]

  def w(self):
    self.Iwn = tk.Toplevel(wn)
    self.Iwn.protocol("WM_DELETE_WINDOW", lambda: self.closeInv())
    self.Iwn.withdraw()

  def move(self):
    self.self.place(x=self.x, y=self.y)
    self.hpl.place(x=self.x, y=self.y - 10)
    self.hpl.config(text=f"{self.hp}/{self.maxhp}")
    x = o.compare(self)
    if x:
      if x.state == "destroyed":
        self.pickUp(x)

  def pickUp(self, d):
    x = item(d.itemi, d.typei, self.Iwn)
    for i in self.inventory:
      for j in i:
        if j.type == x.type:
          j.count += 1
          d.item.place_forget()
          d.state = "gone"
          o.remove(d)
          return 0
    for i in self.inventory:
      if len(i) < 5:
        i.append(x)
        d.item.place_forget()
        d.state = "gone"
        o.remove(d)
        return 0
    error = tk.Label(wn, text="inventory full", fg="red")
    error.place(x=250, y=0)
    wn.after(1000, error.place_forget)

  def die(self):
    self.self.destroy()
    self.hpl.destroy()
    self.Iwn.destroy()
    error = tk.Label(wn, text="you died", fg="red", font=("Arial", 100))
    error.place(x=0, y=0)
    wn.after(3000, lambda: close())

  def openInv(self):
    self.Iwn.deiconify()
    self.Iwn.title("inventory")
    self.Iwn.geometry("300x200")
    for i in range(len(self.inventory)):
      for j in range(len(self.inventory[i])):
        self.inventory[i][j].self.place(x=j * 32.5, y=i * 32.5)
        self.inventory[i][j].c.place(x=j * 32.5, y=i * 32.5)
        self.inventory[i][j].c.config(text=self.inventory[i][j].count)
    self.Iwn.bind("<KeyPress-e>", lambda event: self.closeInv())

  def closeInv(self):
    self.Iwn.withdraw()

  def up(self, e):
    passs(e)
    if self.cd == 0:
      n = self
      n.y -= box
      x = o.compare(n)
      n.y += box
      if self.y - box >= 0:
        if x == None or x.state != "present":
          self.y -= box
          self.move()
      else:
        if test.get(opencc[0], opencc[1] + 1) == None:
          test.addG(1, lambda: genTerrain())
          unload()
          load(test.get(opencc[0], opencc[1] + 1), [opencc[0], opencc[1] + 1])
          self.y += box * 15
          self.move()
        else:
          unload()
          load(test.get(opencc[0], opencc[1] + 1), [opencc[0], opencc[1] + 1])
          self.y += box * 15
          self.move()
      self.cd = 1
      wn.after(100, lambda: dpas(self))

  def down(self, e):
    passs(e)
    if self.cd == 0:
      n = self
      n.y += box
      x = o.compare(n)
      n.y -= box
      if self.y + box <= 500 - box:
        if x == None or x.state != "present":
          self.y += box
          self.move()
      else:
        if test.get(opencc[0], opencc[1] - 1) == None:
          test.addG(1, lambda: genTerrain())
          unload()
          load(test.get(opencc[0], opencc[1] - 1), [opencc[0], opencc[1] - 1])
          self.y -= box * 15
          self.move()
        else:
          unload()
          load(test.get(opencc[0], opencc[1] - 1), [opencc[0], opencc[1] - 1])
          self.y -= box * 15
          self.move()
      self.cd = 1
      wn.after(100, lambda: dpas(self))

  def left(self, e):
    passs(e)
    if self.cd == 0:
      n = self
      n.x -= box
      x = o.compare(n)
      n.x += box
      if self.x - box >= 0:
        if x == None or x.state != "present":
          self.x -= box
          self.move()
      else:
        if test.get(opencc[0] - 1, opencc[1]) == None:
          test.addG(1, lambda: genTerrain())
          unload()
          load(test.get(opencc[0] - 1, opencc[1]), [opencc[0] - 1, opencc[1]])
          self.x += box * 15
          self.move()
        else:
          unload()
          load(test.get(opencc[0] - 1, opencc[1]), [opencc[0] - 1, opencc[1]])
          self.x += box * 15
          self.move()
      self.cd = 1
      wn.after(100, lambda: dpas(self))

  def right(self, e):
    passs(e)
    if self.cd == 0:
      n = self
      n.x += box
      x = o.compare(n)
      n.x -= box
      if self.x + box <= 500 - box:
        if x == None or x.state != "present":
          self.x += box
          self.move()
      else:
        if test.get(opencc[0] + 1, opencc[1]) == None:
          test.addG(1, lambda: genTerrain())
          unload()
          load(test.get(opencc[0] + 1, opencc[1]), [opencc[0] + 1, opencc[1]])
          self.x -= box * 15
          self.move()
        else:
          unload()
          load(test.get(opencc[0] + 1, opencc[1]), [opencc[0] + 1, opencc[1]])
          self.x -= box * 15
          self.move()
      self.cd = 1
      wn.after(100, lambda: dpas(self))


openc = [[None for i in range(16)] for i in range(16)]
opencc = [0, 0]


class objects:

  def __init__(self, *args):
    self.self = []
    for i in args:
      self.self.append(i)

  def add(self, *args):
    for i in args:
      self.self.append(i)

  def compare(self, a):
    x = a.x
    y = a.y
    for i in self.self:
      if i.x == x and i.y == y:
        return i
    return None

  def remove(self, a):
    if a in self.self:
      self.self.remove(a)


def load(x, cc):
  for i in range(16):
    for j in range(16):
      if x[i][j] == 0:
        openc[i][j] = "air"
      if x[i][j] == 1:
        openc[i][j] = block(j * box, i * box, random.randint(100, 250), wi,
                            "wood")
      elif x[i][j] == 2:
        openc[i][j] = block(j * box, i * box, random.randint(200, 250), coi,
                            "coal_ore")
        openc[i][j].cDrop(ci, "coal")
      elif x[i][j] == 3:
        openc[i][j] = Spawner(block(j * box, i * box, 100, sai, "spawner"),
                              mob(j * box, i * box - box, 100, 1.5, zi))
      elif x[i][j] == 4:
        openc[i][j] = Heart(block(j * box, i * box, 100, hi, "heart"))
  global opencc
  opencc = cc


def unload():
  res = [[None for i in range(16)] for i in range(16)]
  for i in range(16):
    for j in range(16):
      if isinstance(openc[i][j], Spawner):
        for k in openc[i][j].spawnedMobs:
          k.die()
        openc[i][j].type.die()
        openc[i][j].self.self.place_forget()
        if openc[i][j].self.state == "present":
          openc[i][j].self.state = "nic"
        else:
          res[i][j] = 0
        o.remove(openc[i][j].self)
      elif isinstance(openc[i][j], Heart):
        openc[i][j].self.self.place_forget()
        if openc[i][j].self.state == "present":
          openc[i][j].self.state = "nic"
        else:
          res[i][j] = 0
        o.remove(openc[i][j].self)
      elif isinstance(openc[i][j], block):
        o.remove(openc[i][j])
        openc[i][j].self.place_forget()
        if openc[i][j].type == "coal_ore":
          if openc[i][j].state == "present":
            res[i][j] = 2
            openc[i][j].self.state = "nic"
          elif openc[i][j].state == "destroyed":
            openc[i][j].state = "gone"
            res[i][j] = 0
          else:
            res[i][j] = 0
        elif openc[i][j].type == "wood":
          if openc[i][j].state == "present":
            res[i][j] = 1
            openc[i][j].self.state = "nic"
          elif openc[i][j].state == "destroyed":
            openc[i][j].state = "gone"
            res[i][j] = 0
          else:
            res[i][j] = 0
      else:
        res[i][j] = 0
  test.set(opencc[0], opencc[1], res)


o = objects()

player = Player(pi)

table = CraftingT()
table.add(item(wsi, "wooden_sword", player.Iwn, WoodSword()), {"wood": 2})

test = Sgrid(genTerrain())
test.addG(1, lambda: genTerrain())

load(test.get(0, 0), [0, 0])

for i in range(2):
  print("")


def close():
  wn.destroy()


wn.bind("<KeyPress-w>", lambda event: player.up(event))
wn.bind("<KeyPress-s>", lambda event: player.down(event))
wn.bind("<KeyPress-a>", lambda event: player.left(event))

wn.bind("<KeyPress-d>", lambda event: player.right(event))
wn.bind("<KeyPress-e>", lambda event: player.openInv())
wn.bind("<KeyPress-c>", lambda event: table.open())

wn.mainloop()
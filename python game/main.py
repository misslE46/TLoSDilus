from enemy import Enemy
from medic_bag import Medic_bag
from doors import Door
from wall import Wall
from player import Player
from bullet import Bullet
from shooting_enemy import Shooting_Enemy
import random
import tkinter as tk
import threading

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas_int = tk.Canvas(root, width = 600, height = 150, bg = "grey")
        self.canvas_int.pack()
        self.canvas =tk.Canvas(root, width = 600, height = 600, bg = "black")
        self.canvas.pack()
        self.rooms=[1]
        self.current_room=self.rooms[0]
        self.current_room_number=0
        self.player = Player(self.canvas, 250, 250)
        self.health_bar = self.canvas_int.create_text(300, 25, text = f"Здоровье: {self.player.health}", font =("Arial", 14), fill = "black")
        self.room_bar = self.canvas_int.create_text(300, 50, text = f"Комната: {self.current_room_number+1}", font =("Arial", 14), fill = "black")

        self.enemies = [

            Enemy(self.canvas, 10, 10),
            Enemy(self.canvas, 580, 580),
            Enemy(self.canvas, 10, 580),
            Enemy(self.canvas, 580, 10)
        ]
        self.enemy_room=[
            [10,10],
            [580,580],
            [10,580],
            [580,10]
        ]
        self.doors=[
            #2двери
            Door(self.canvas,0,275,5,325),
            Door(self.canvas,598,275,600,325),

        ]

        self.walls = [
            #края
            Wall(self.canvas, 0, 0, 600,8),
            Wall(self.canvas, 0, 0, 8,275),
            Wall(self.canvas, 0, 325, 8,600),
            Wall(self.canvas, 0, 592, 600,600),
            Wall(self.canvas, 592, 0, 600,275),
            Wall(self.canvas, 592, 325, 600,600),
            #2вертик
            Wall(self.canvas, 288, 50, 312,250),
            Wall(self.canvas, 288, 350, 312, 550),
            #2горизонт
            Wall(self.canvas,  50,288,250,312),
            Wall(self.canvas,  350, 288, 550,312),

        ]
        self.room1=[
            [0, 0, 600,8],
            [0, 0, 8,275],
            [0, 325, 8,600],
            [0, 592, 600,600],
            [592, 0, 600,275],
            [592, 325, 600,600],
            [288, 50, 312,250],
            [288, 350, 312, 550],
            [50,288,250,312],
            [350, 288, 550,312],
        ]
        self.room2=[
            [0, 0, 600,8],
            [0, 0, 8,275],
            [0, 325, 8,600],
            [0, 592, 600,600],
            [592, 0, 600,275],
            [592, 325, 600,600],
            [288, 50, 312,250],
            [288, 350, 312, 550],
        ]
        self.room3=[
            [0, 0, 600,8],
            [0, 0, 8,275],
            [0, 325, 8,600],
            [0, 592, 600,600],
            [592, 0, 600,275],
            [592, 325, 600,600],
            [50,288,250,312],
            [350, 288, 550,312],
        ]
        self.room4=[
            [0, 0, 600,8],
            [0, 0, 8,275],
            [0, 325, 8,600],
            [0, 592, 600,600],
            [592, 0, 600,275],
            [592, 325, 600,600],
            [288, 350, 312, 550],
            [350, 288, 550,312],
        ]
        self.room5=[
            [0, 0, 600,8],
            [0, 0, 8,275],
            [0, 325, 8,600],
            [0, 592, 600,600],
            [592, 0, 600,275],
            [592, 325, 600,600],
            [288, 50, 312,250],
            [50,288,250,312],
        ]

        self.medic_bags=[]


        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.update_movement()
        

    def key_press(self, event):
        key = event.keysym.lower()
        if key in ("w", "a", "s", "d","left","up","down","right"):
            self.player.keys_pressed.add(key)

    def key_release(self, event):
        key = event.keysym.lower()
        self.player.keys_pressed.discard(key)

    def update_movement(self):
        player_coords = self.canvas.coords(self.player.rect)
        for key in self.player.keys_pressed:
            if key == "w" :
                self.move_player(0, -4)
            elif key == "s":
                self.move_player(0, 4)
            elif key == "a":
                self.move_player(-4, 0)
            elif key == "d":
                self.move_player(4, 0)
            elif key == "up":
                self.use_sword(player_coords[0],player_coords[1]-20,player_coords[2],player_coords[3]-20)
            elif key == "down":
                self.use_sword(player_coords[0],player_coords[1]+20,player_coords[2],player_coords[3]+20)
            elif key == "left":
                self.use_sword(player_coords[0]-20,player_coords[1],player_coords[2]-20,player_coords[3])
            elif key == "right":
                self.use_sword(player_coords[0]+20,player_coords[1],player_coords[2]+20,player_coords[3])
        self.enemy_chase()
        self.root.after(16, self.update_movement)
        self.check_enemy_collision()
        self.check_bullet_collision()

    def enemy_chase(self):
        player_coords = self.canvas.coords(self.player.rect)
        for enemy in self.enemies:
            enemy_coords = self.canvas.coords(enemy.rect)
            if player_coords[0]==enemy_coords[0]:
                enemy.dx=0
                enemy.ddx=0
            elif player_coords[0]<enemy_coords[0]:
                enemy.dx=-3
                enemy.ddx=player_coords[0]-enemy_coords[0]
            elif player_coords[0]>enemy_coords[0]:
                enemy.dx=3
                enemy.ddx=player_coords[0]-enemy_coords[0]


            if player_coords[1]==enemy_coords[1]:
                enemy.dy=0
                enemy.ddy=0
            elif player_coords[1]<enemy_coords[1]:
                enemy.dy=-3
                enemy.ddy=player_coords[1]-enemy_coords[1]
            elif player_coords[1]>enemy_coords[1]:
                enemy.dy=3
                enemy.ddy=player_coords[1]-enemy_coords[1]




    
    def check_enemy_collision(self):
        player_coords = self.canvas.coords(self.player.rect)
        for enemy in self.enemies:
            enemy_coords = self.canvas.coords(enemy.rect)
            for wall in self.walls:
                wall_coords = self.canvas.coords(wall.rect)
                if (enemy_coords[2] > wall_coords[0] and enemy_coords[0] < wall_coords[2] and
                    enemy_coords[3] > wall_coords[1] and enemy_coords[1] < wall_coords[3]):
                    #print('враг ударился')
                    if enemy_coords[0] < wall_coords[0]:
                        enemy.dx-=7
                        
                    if enemy_coords[1] > wall_coords[1]:
                        enemy.dy+=7
                        
                    if enemy_coords[2] > wall_coords[2]:
                        enemy.dx+=7
                        
                    if enemy_coords[3] < wall_coords[3]:
                        enemy.dy-=7
                        
                    
                    
                    
                if (player_coords[2] > enemy_coords[0] and player_coords[0] < enemy_coords[2] and player_coords[3] > enemy_coords[1] and player_coords[1] < enemy_coords[3]):
                    self.player.health -= 0.1
                    self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: {int(self.player.health)}")
                    if self.player.health <= 0:
                        self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: 0")
                        self.game_over()


    def use_sword(self, x1, y1,x2,y2):
        sword=self.canvas.create_rectangle(x1, y1, x2, y2, fill = "blue", outline= 'grey', width=0)
        for enemy in self.enemies:
            enemy_coords = self.canvas.coords(enemy.rect)
            if enemy.health==0:
                self.medic_bags.append(Medic_bag(self.canvas,enemy_coords[0]+5,enemy_coords[1]+5))
                self.enemies.remove(enemy)
                self.canvas.delete(enemy.rect)
            if (enemy_coords[2] > x1 and enemy_coords[0] < x2 and
                enemy_coords[3] > y1 and enemy_coords[1] < y2):
                if enemy_coords[0] < x1:
                    enemy.health-=1
                    
                elif enemy_coords[1] > y1:
                    enemy.health-=1
                    
                elif enemy_coords[2] > x2:
                    enemy.health-=1
                    
                elif enemy_coords[3] < y2:
                    enemy.health-=1
                    
        def del_sword():
                self.canvas.delete(sword)
        timer = threading.Timer(0.01, del_sword)
        timer.start()
        
    

    def move_player(self, dx, dy):
        self.canvas.move(self.player.rect, dx, dy)
        if self.check_collision():
            self.canvas.move(self.player.rect, -dx, -dy)

    def check_collision(self):
        player_coords = self.canvas.coords(self.player.rect)
        #print(player_coords)
        for medic_bag in self.medic_bags:
            medic_bag_coords = self.canvas.coords(medic_bag.rect)
            if (player_coords[2] > medic_bag_coords[0] and player_coords[0] < medic_bag_coords[2] and
                player_coords[3] > medic_bag_coords[1] and player_coords[1] < medic_bag_coords[3]):
                self.player.health += 20
                self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: {int(self.player.health)}")
                self.medic_bags.remove(medic_bag)
                self.canvas.delete(medic_bag.rect)
        for door in self.doors:
            door_coords = self.canvas.coords(door.rect)
            if (player_coords[2] > door_coords[0] and player_coords[0] < door_coords[2] and
                player_coords[3] > door_coords[1] and player_coords[1] < door_coords[3]):
                    #левая
                    if player_coords[0] > door_coords[0]:
                        self.move_player(560,0)
                        if self.current_room==self.rooms[0]:
                            self.current_room=self.rooms[-1]
                            self.current_room_number=len(self.rooms)-1
                            print(self.current_room,self.current_room_number+1)
                            self.canvas_int.itemconfig(self.room_bar, text = f"Комната: {self.current_room_number+1}")
                            for wall in self.walls:
                                self.canvas.delete(wall.rect)
                            for medic_bag in self.medic_bags:
                                self.canvas.delete(medic_bag.rect)
                            for bullet in Bullet.bullets:
                                self.canvas.delete(bullet.oval)
                            for enemy in self.enemies:
                                self.canvas.delete(enemy.rect)
                            self.walls.clear()
                            self.enemies.clear()
                            self.medic_bags.clear()
                            Bullet.bullets.clear()
                            #####
                            if self.current_room==1:
                                for wall in self.room1:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==2:
                                for wall in self.room2:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==3:
                                for wall in self.room3:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==4:
                                for wall in self.room4:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==5:
                                for wall in self.room5:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                        else:
                            self.current_room_number-=1
                            self.current_room=self.rooms[self.current_room_number]
                            print(self.current_room,self.current_room_number+1)
                            self.canvas_int.itemconfig(self.room_bar, text = f"Комната: {self.current_room_number+1}")
                            for wall in self.walls:
                                self.canvas.delete(wall.rect)
                            for medic_bag in self.medic_bags:
                                self.canvas.delete(medic_bag.rect)
                            for bullet in Bullet.bullets:
                                self.canvas.delete(bullet.oval)
                            for enemy in self.enemies:
                                self.canvas.delete(enemy.rect)
                            self.walls.clear()
                            self.enemies.clear()
                            self.medic_bags.clear()
                            Bullet.bullets.clear()
                            ######
                            if self.current_room==1:
                                for wall in self.room1:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==2:
                                for wall in self.room2:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==3:
                                for wall in self.room3:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==4:
                                for wall in self.room4:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==5:
                                for wall in self.room5:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                    
                    #правая
                    
                    elif player_coords[0] < door_coords[0]:
                        self.move_player( -560,0)
                        if self.current_room==self.rooms[-1]:
                            self.rooms.append(random.randint(2,5))
                            self.current_room=self.rooms[-1]
                            self.current_room_number+=1
                            print(self.current_room,self.current_room_number+1)
                            self.canvas_int.itemconfig(self.room_bar, text = f"Комната: {self.current_room_number+1}")
                            for wall in self.walls:
                                self.canvas.delete(wall.rect)
                            for medic_bag in self.medic_bags:
                                self.canvas.delete(medic_bag.rect)
                            for bullet in Bullet.bullets:
                                self.canvas.delete(bullet.oval)
                            for enemy in self.enemies:
                                self.canvas.delete(enemy.rect)
                            self.walls.clear()
                            self.enemies.clear()
                            self.medic_bags.clear()
                            Bullet.bullets.clear()
                            ######
                            if self.current_room==1:
                                for wall in self.room1:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==2:
                                for wall in self.room2:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==3:
                                for wall in self.room3:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==4:
                                for wall in self.room4:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==5:
                                for wall in self.room5:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                        else:
                            self.current_room_number+=1                            
                            self.current_room=self.rooms[self.current_room_number]
                            print(self.current_room,self.current_room_number+1)
                            self.canvas_int.itemconfig(self.room_bar, text = f"Комната: {self.current_room_number+1}")
                            for wall in self.walls:
                                self.canvas.delete(wall.rect)
                            for medic_bag in self.medic_bags:
                                self.canvas.delete(medic_bag.rect)
                            for bullet in Bullet.bullets:
                                self.canvas.delete(bullet.oval)
                            for enemy in self.enemies:
                                self.canvas.delete(enemy.rect)
                            self.walls.clear()
                            self.enemies.clear()
                            self.medic_bags.clear()
                            Bullet.bullets.clear()
                            ######
                            if self.current_room==1:
                                for wall in self.room1:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==2:
                                for wall in self.room2:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==3:
                                for wall in self.room3:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==4:
                                for wall in self.room4:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                            elif self.current_room==5:
                                for wall in self.room5:
                                    x1=wall[0]
                                    y1=wall[1]
                                    x2=wall[2]
                                    y2=wall[3]
                                    self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                                for enemy in self.enemy_room:
                                    x=enemy[0]
                                    y=enemy[1]
                                    i=random.randint(0,1)
                                    if i==0:
                                        self.enemies.append(Enemy(self.canvas,x,y))
                                    else:
                                        self.enemies.append(Shooting_Enemy(self.canvas,x,y))
               
        for wall in self.walls:
            wall_coords = self.canvas.coords(wall.rect)
            if (player_coords[2] > wall_coords[0] and player_coords[0] < wall_coords[2] and
                player_coords[3] > wall_coords[1] and player_coords[1] < wall_coords[3]):
                return True
        return False

    
    

    def check_bullet_collision(self):
        player_coords = self.canvas.coords(self.player.rect)
        
        #print(len(Bullet.bullets))
        for bullet in Bullet.bullets[:]:
            bullet_coords = self.canvas.coords(bullet.oval)
            if (player_coords[2] > bullet_coords[0] and player_coords[0] < bullet_coords[2] and player_coords[3] > bullet_coords[1] and player_coords[1] < bullet_coords[3]):
                self.player.health -= 10
                self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: {int(self.player.health)}")
                if self.player.health <= 0:
                    self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: 0")
                    self.game_over()
                Bullet.bullets.remove(bullet)
                self.canvas.delete(bullet.oval)
            for wall in self.walls:
                wall_coords = self.canvas.coords(wall.rect)
                if (bullet_coords[2] > wall_coords[0] and bullet_coords[0] < wall_coords[2] and
                    bullet_coords[3] > wall_coords[1] and bullet_coords[1] < wall_coords[3]):
                    if len(Bullet.bullets)!=0:
                        Bullet.bullets.remove(bullet)
                    self.canvas.delete(bullet.oval)
        #self.root.after(50, self.check_bullet_collision)
    def game_over(self):
        self.canvas_int.create_text(300, 50, text = "ПОТРАЧЕНО", font =("Arial", 30), fill ="red")
        for medic_bag in self.medic_bags:
            self.canvas.delete(medic_bag.rect)
        for bullet in Bullet.bullets:
            self.canvas.delete(bullet.oval)
        for enemy in self.enemies:
            self.canvas.delete(enemy.rect)
        self.enemies.clear()
        self.medic_bags.clear()
        Bullet.bullets.clear()
        self.canvas.delete(self.player.rect)
        
        

root = tk.Tk()
game = Game(root)
root.mainloop()
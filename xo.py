#Состояния
#0 Неопределённости
#2 Ничья
#5 Победа ai -5 Победа player
ai=""
player=""

def generator(current_pos,side,current_lvl,root):
    global counter
    #Лист с нодами потомками
    node_poss=list()
    #Оценки текущего уровня. Ключ=клетка поля. Значение=оценка.
    node_grades=list()
    #Оценки уровня 0 с координатой позиции
    final_grades=dict()
    for i in range(9):
        if current_pos[i]!="":
            node_poss.append(None)
            continue
        new_pos=list(current_pos)
        new_pos[i]=side
        #Генерация новой позиции и счётчик+1
        node_poss.append(new_pos)
        counter+=1
        end_grade=end_state(new_pos)
        #print("Оценка=",end_grade)
        #Генератор по рекурсии
        #Не вызываем, если достигнута крайняя нода или предельный уровень анализа
        #print("cur_lvl=",current_lvl," max=",max_lvl)
        if current_lvl<max_lvl and end_grade==0:
            end_grade=generator(new_pos,invert_side(side),current_lvl+1,counter)        
        #Оценки в массив, потом выбираем MinMax
        #print("!"," ",end_grade)
        node_grades.append(end_grade)
        if current_lvl==0:
            final_grades[i]=end_grade    
    graph[root]=node_poss
    #Оценка min max
    responce=""
    #print("Оценки ноды ",node_grades)
    #Если ход AI-max 
    if side==ai:
        #print("A")
        responce=max(node_grades)
    #Если ход Human-min      
    else:
        #print("h")        
        responce=min(node_grades)
    if current_lvl==0:
        print(final_grades)
        responce=max_pair(final_grades,1)
    return responce

#Если op=1, выдать толко ключ с мин/макс значением
def min_pair(arg,op=0):
    key=None
    mn=float("inf")
    for k,v in arg.items():
        if v<mn:
            mn=v
            key=k
    if op==0: 
        return {key:mn}
    else:
        return key
def max_pair(arg,op=0):
    key=None
    mx=float("-inf")
    for k,v in arg.items():
        if v>mx:
            mx=v
            key=k
    if op==0: 
        return {key:mx}
    else:
        return key
#    
def invert_side(arg):
    if arg=="X":
        return "O"
    else:
        return "X"

#Проверка на достижение крайней игровой позиции
#На входе позиция
def end_state(arg):
    #print(arg)
    result=2
    end_of_game=list()
    end_of_game.append([0,1,2])
    end_of_game.append([3,4,5])
    end_of_game.append([6,7,8])
    
    end_of_game.append([0,3,6])
    end_of_game.append([1,4,7])
    end_of_game.append([2,5,8])

    end_of_game.append([0,4,8])
    end_of_game.append([2,4,6])
    #Победа?
    for i in end_of_game:
        #print(arg[i[0]]," ",arg[i[1]]," ",arg[i[2]])
        if ((arg[i[0]]==ai)
        and (arg[i[1]]==ai)
        and (arg[i[2]]==ai)):
            return 5
        if ((arg[i[0]]==player)
        and (arg[i[1]]==player)
        and (arg[i[2]]==player)):
            return -5
    #Ничья?
    for i in arg:
        if i=="":
            result=0
            break
    return result

#Печать позиции в стиле ХО
def print_pos(arg):
    print("{0:->7}".format(""))
    print("|{0: >1}|{1: >1}|{2: >1}|".format(arg[0],arg[1],arg[2]))
    print("{0:->7}".format(""))
    print("|{0: >1}|{1: >1}|{2: >1}|".format(arg[3],arg[4],arg[5]))
    print("{0:->7}".format(""))
    print("|{0: >1}|{1: >1}|{2: >1}|".format(arg[6],arg[7],arg[8]))
    print("{0:->7}".format(""))
    
def print_co_pos(arg):
    for i in arg:
        if i==None:continue
        print_pos(i)
        print()
#Очистка поля
def clear_pos():
    return ["","","","","","","","",""]     
#
def player_move(arg):
    while True:
        try:
            position=int(input("Ваш ход:"))            
        except Exception:
            print("Ошибка ввода. Введите число от 0 до 8")
        else:
            return position

#main        
lvl=0
game_field=clear_pos()
player=""
while player!="X" and player!="O":
    player=input("Выберите сторону X или О:")
ai=invert_side(player)
if player=="X":player_move_first=True

max_lvl=2
graph=dict()

#main()
d={0:8,1:3,2:-1}
#print(min_pair(d))
#print(max_pair(d))
#print("Мой ход=",generator(current_pos,"X",lvl,0))
#Игровой цикл
while True:
    counter=0
    #Игрок за Х
    if player_move_first:
        position=player_move(game_field)
        game_field[position]=player
        if end_state(game_field)!=0:
            break
        print_pos(game_field)
        
    position=generator(game_field,ai,lvl,0)
    game_field[position]=ai
    if end_state(game_field)!=0:
        break
    print_pos(game_field)
    player_move_first=True
print("Игра окончена!")

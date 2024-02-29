from time import sleep

# criando uma string multilinhas
robot_art = r"""

      |0: {head_name}
      |Is available: {head_status}
      |Attack: {head_attack}
      |Defense: {head_defense}
      |Energy consumption: {head_energy_consump}
              ^
              |                  |1: {weapon_name}
              |                  |Is available: {weapon_status}
     ____     |    ____          |Attack: {weapon_attack}
    |oooo|  ____  |oooo| ------> |Defense: {weapon_defense}
    |oooo| '    ' |oooo|         |Energy consumption: {weapon_energy_consump}
    |oooo|/\_||_/\|oooo|
    `----' / __ \  `----'           |2: {left_arm_name}
   '/  |#|/\/__\/\|#|  \'           |Is available: {left_arm_status}
   /  \|#|| |/\| ||#|/  \           |Attack: {left_arm_attack}
  / \_/|_|| |/\| ||_|\_/ \          |Defense: {left_arm_defense}
 |_\/    O\=----=/O    \/_|         |Energy consumption: {left_arm_energy_consump}
 <_>      |=\__/=|      <_> ------> |
 <_>      |------|      <_>         |3: {right_arm_name}
 | |   ___|======|___   | |         |Is available: {right_arm_status}
// \\ / |O|======|O| \  //\\        |Attack: {right_arm_attack}
|  |  | |O+------+O| |  |  |        |Defense: {right_arm_defense}
|\/|  \_+/        \+_/  |\/|        |Energy consumption: {right_arm_energy_consump}
\__/  _|||        |||_  \__/
      | ||        || |          |4: {left_leg_name}
     [==|]        [|==]         |Is available: {left_leg_status}
     [===]        [===]         |Attack: {left_leg_attack}
      >_<          >_<          |Defense: {left_leg_defense}
     || ||        || ||         |Energy consumption: {left_leg_energy_consump}
     || ||        || || ------> |
     || ||        || ||         |5: {right_leg_name}
   __|\_/|__    __|\_/|__       |Is available: {right_leg_status}
  /___n_n___\  /___n_n___\      |Attack: {right_leg_attack}
                                |Defense: {right_leg_defense}
                                |Energy consumption: {right_leg_energy_consump}

"""

colors = {
    "Black":   '\x1b[90m',
    "Blue":   '\x1b[94m',
    "Cyan":   '\x1b[96m',
    "Green":   '\x1b[92m',
    "Magenta":  '\x1b[95m',
    "Red":    '\x1b[91m',
    "White":   '\x1b[97m',
    "Yellow":   '\x1b[93m',
}

# PARTE 1
class Part():
    # ADICIONADO o atributo "part_status" para retornar de início todas as partes "True"
    def __init__(self, name: str, attack_level=0, defense_level=0, energy_consumption=0, part_status = True):
        self.name = name
        self.attack_level = attack_level
        self.defense_level = defense_level
        self.energy_consumption = energy_consumption
        self.part_status = part_status

    # retorna um dicionário preenchendo as informações das partes do robô
    def get_status_dict(self):
        formatted_name = self.name.replace(" ", "_").lower()
        return {
            "{}_name".format(formatted_name): self.name.upper(),
            "{}_status".format(formatted_name): self.is_available(),
            "{}_attack".format(formatted_name): self.attack_level,
            "{}_defense".format(formatted_name): self.defense_level,
            "{}_energy_consump".format(formatted_name): self.energy_consumption,
        }

    # MODIFICADO para quando o nivel de defesa chegar a zero, o status da parte ficar "False"
    def reduce_edefense(self, attack_level):
        self.defense_level -= attack_level
        if self.defense_level <= 0:
            self.defense_level = 0
            self.part_status = False

    # MODIFICADO para retornar o status das partes do robô
    def is_available(self):
        return self.part_status
        # return self.defense_level >= 0        # deixar partes disponíveis "True"


class Robot:

    def __init__(self, name, color_code):
        self.name = name
        self.color_code = color_code
        self.energy = 100
        self.parts = [
            Part("Head", attack_level=5, defense_level=10, energy_consumption=5),
            Part("Weapon", attack_level=15, defense_level=0, energy_consumption=10),
            Part("Left Arm", attack_level=3, defense_level=20, energy_consumption=10),
            Part("Right Arm", attack_level=6, defense_level=20, energy_consumption=10),
            Part("Left Leg", attack_level=4, defense_level=20, energy_consumption=15),
            Part("Right Leg", attack_level=8, defense_level=20, energy_consumption=15),
        ]


    def print_status(self):
        print(self.color_code)

        #   formatando para string o robot_art, (**) desempacota o return "part_status" e pega as chaves e
        #   valores do "get_part_status" e preenche nas partes reservadas do "robot_art {}"
        str_robot = robot_art.format(**self.get_part_status())

        self.greet()
        self.print_energy()
        print(str_robot)
        print(colors["White"])  # cor default


    def greet(self):    # saudação
        print("Hello, my name is", self.name)

    def print_energy(self): # energia
        print("We have", self.energy, " percent energy left")


    # PARTE 3
    def get_part_status(self):
        part_status = {}
        for part in self.parts:
            #   obtendo o status de cada parte do robo no status_dict e adicionando no part_status
            status_dict = part.get_status_dict()
            part_status.update(status_dict)
        return part_status

    # retorna se o status da parte do robô está "True" ou "False"
    def is_there_available_part(self):
        for part in self.parts:
            if part.is_available():
                return True
        return False

    # ADICIONADO para retornar somente as partes disponíveis do robô para atacar
    def is_available_part(self, part_index):
        return self.parts[part_index].is_available()

    # MODIFICADO para retornar somente energia > 0 (robô está ligado!)
    def is_on(self):
        return self.energy > 0


    # PARTE 4
    def attack(self, enemy_robot, part_to_use, part_to_attack):

        # ADICIONADO para verificar quando o usuário realizar um ataque com energia insuficiente
        if self.energy < self.parts[part_to_use].energy_consumption:
            print(f"\n\033[91m{self.name.capitalize()}, you don't have energy enough to attack.\n\033[0m")

        # seleciona a parte que sera atacada do robo inimigo no dict parts, em seguida, chama o
        # método "reduce_edefense" (da parte selecionada do robo), passando como atributo o nivel
        # de ataque do robo que está atacando
        enemy_robot.parts[part_to_attack].reduce_edefense(self.parts[part_to_use].attack_level)
        self.energy -= self.parts[part_to_use].energy_consumption

        # ADICIONADO para impedir energia negativa
        if self.energy <= 0:
            self.energy = 0


# PARTE 5
# construindo o robô
def build_robot():
    robot_name = input("Robot name: ")
    color_code = choose_color()
    robot = Robot(robot_name, color_code)
    robot.print_status()
    return robot

# escolhendo a cor do robô
def choose_color():
    available_colors = colors
    print("\nAvailable colors:")
    for key, value in available_colors.items():
        print(value, key)
    print(colors["White"])  # cor default
    # ADICIONADO para validação do inputs
    while True:
        chosen_color = input("Choose a color: ").capitalize()
        if chosen_color not in available_colors:
            print("\033[91mInvalid color. Please choose a valid color.\033[0m\n")
        else:
            break
    color_code = available_colors[chosen_color]
    return color_code

# ADICIONADO funções para deixar o código mais "limpo"
def welcome():
    welcome = "w e l c o m e   t o   t h e   g a m e  !".upper()
    f_title = f'\033[41m\n{" "*100}\n\n'
    print(f'{f_title}{" "}\033[0m\033[1m{welcome.center(98, " ")}\033[41m{" "}\n{f_title}\033[0m')

def lets_play():
    letsPlay = "l e t ` s   p l a y   ! ! !".upper()
    f_title = f'\n\033[1;91m{"X"*100}\n'
    print(f'{f_title}\033[0m\n\033[1m{letsPlay.center(100, " ")}\n{f_title}\n\033[0m')


# PARTE 6
# inicializando o jogo
def play():
    playing = True

    welcome()
    sleep(5)
    print(f'\n\n\033[31m{"-"*40}\n|{"Datas for player 1:".center(38," ")}|\n{"-"*40}\n\033[0m')
    robot_one = build_robot()       # construção robô 1
    sleep(5)

    welcome()
    sleep(5)
    print(f'\n\n\033[31m{"-"*40}\n|{"Datas for player 2:".center(38," ")}|\n{"-"*40}\n\033[0m')
    robot_two = build_robot()       # construção robô 2
    sleep(5)

    current_robot = robot_one
    enemy_robot = robot_two
    rount = 0

    while playing:
        # verifica de quem é a vez de jogar cada partida
        if rount % 2 == 0:
            current_robot = robot_one
            enemy_robot = robot_two
        else:
            current_robot = robot_two
            enemy_robot = robot_one



        lets_play()
        sleep(2)
        # ADICIONADO para mostra o nome do robô que joga a partida
        turn = current_robot.name + "'s turn"
        print(f'\n\033[3;97;40m{turn.upper().center(60, " ")}\n\033[0m\n\n')

        current_robot.print_status()

        # MODIFICADO para verificar se a escolha de ataque do usuário é uma parte disponível do seu robô
        while True:
            print("What part should I use to attack?:")
            part_to_use = int(input("Choose a number part: "))

            # ADICIONADO para validação do inputs
            if part_to_use < 0 or part_to_use > 5:
                print("\033[91mInvalid input. Please choose a number between 0 and 5.\n\033[0m")
            elif not current_robot.is_available_part(part_to_use):
                print("\033[91mOps... This part is not available. Choose another part!\n\033[0m")
            else:
                break

        print(f'\n\n{"=+"*40}\n\n')  # apenas uma separação visual dos robôs
        enemy_robot.print_status()

        # MODIFICADO para verificar se a escolha do usuário é uma parte disponível do robô inimigo
        while True:
            print("Which part of the enemy should we attack?")
            part_to_attack = int(input("Choose an enemy number part to attack: "))

            # ADICIONADO para validação do inputs
            if part_to_attack < 0 or part_to_attack > 5:
                print("\033[91mInvalid input. Please choose a number between 0 and 5.\n\033[0m")
            elif not enemy_robot.is_available_part(part_to_attack):
                print("\033[91mThis enemy part has been destroyed. Choose another part!\n\033[0m")
            else:
                break


        # o robô atual vai atacar o robo inimigo no "par_to_attack" com a "part_to_use"
        current_robot.attack(enemy_robot, part_to_use, part_to_attack)
        rount += 1
        sleep(5)

        # ADICIONADO variáveis para um "print()" mais "limpo" no código
        f_title =f'\n\n{"H"*100}\n\n'
        game_over = f'{f_title}|{"Game Over !  {} won !".format(enemy_robot.name).center(98, " ")}|{f_title}'
        congrats = f'{f_title}|{"Congratulations {} !  You won !".format(current_robot.name).center(98, " ")}|{f_title}'

        # ADICIONADO para verifica se o robô tem energia suficiente para atacar
        if not current_robot.is_on():
            print('\033[1;91m', game_over.upper(),"\033[0m")
            playing = False

        # encerra o jogo quando todas as partes do robô inimigo são destruidas
        if not enemy_robot.is_on() or enemy_robot.is_there_available_part() == False:
            print('\033[1;92m', congrats.upper(), "\033[0m")
            playing = False

    # ADICONADO um loop caso o jogador queira jogar novamente
    playAgain = input("\n\nDo you want to play again? (yes/no): ").lower()
    if (playAgain == "yes" or playAgain == "y"):

        newPlay = play()
    elif (playAgain == "no" or playAgain == "n"):
        print("\nOk. Until later!")
    else:
        print("\nSorry... Invalid Input. Until later!")

play()
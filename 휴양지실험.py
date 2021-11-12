import pygame
import random
import time
# -------------------------------------------------------------------------------
# WINDOW
pygame.init()

screen = pygame.display.set_mode((1300, 700))

pygame.display.set_caption("Monopoly")#+++

# -------------------------------------------------------------------------------
# SQUARE CLASSES
class Property:
    def __init__(self, name, boardpos, colour):
        self.name = name
        self.boardpos = boardpos
        self.colour = colour
        self.houses = 0
        #self.owner = bank
        self.rent = 0
        self.mortgaged = False
        self.rejected = False  # This is here so the user only has to buy/reject a property once.
        self.paidRent = False
        self.streetOwned = False
        self.buttonPosition = [[0, 0], [0, 0]]
        self.costsList = []

    def getInitialRent(self): # Returns the (houseless) rent of a property, based on its position on the board.
        if self.colour <= 7:
            if self.boardpos == 5 * self.colour + 4 or self.name == 'England':
                self.costsList = houseCostGrid[self.colour][1]
                return houseCostGrid[self.colour][1][0]

            else:
                self.costsList = houseCostGrid[self.colour][0]
                return houseCostGrid[self.colour][0][0]
        elif self.colour == 8:
            return 25
        else:
            return 4*roll
        
class Chance: # There ultimately wasn't much point in writing this class except to help identify squares by their type.
    def __init__(self, name, boardpos):
        self.name = name
        self.boardpos = boardpos
        if self.name == 'Chance':
            self.list = chance
        else:
            self.list = communityChest

    def pickCard(self):
        return random.choice(self.list)

class TaxSquares: # Again, more of an identifier than anything else.
    def __init__(self, name, boardpos):
        self.name = name
        self.boardpos = boardpos
        self.paid = False

    def getTax(self):
        if self.name == 'Income Tax':
            return 200
        return 100

class SpecialSquares:
    def __init__(self, name, boardpos):
        self.name = name
        self.boardpos = boardpos
        self.paid = False

    def getPayAmount(self, freeParking): # Returns how much money a player gets for landing on a square.
        global alert
        if self.name == 'Go':
            if user.isTurn:
                alert = Alert('Lazy Programming', 'You landed on Go and got $400 #because I was too lazy to fix #that issue. Some people play by #that rule anyway.')
            return 200
        elif self.name == 'Free Parking':
            if user.isTurn:
                alert = Alert('Rolling in Dough, maybe', ('You got $' + str(freeParking) + ' from Free Parking!'))
            return freeParking
        else:
            return 0

# -------------------------------------------------------------------------------
# SPRITE CLASSES
class Player:
    def __init__(self, name, isTurn):
        self.name = name 
        self.boardpos = 0 
        self.timeMoving = 0 # 밑에 move함수에서 말 한칸씩 이동할때 쓰는거
        self.colour = palette.dutchWhite 
        self.isTurn = isTurn 
        self.money = 1500
        self.canRoll = True
        self.doublesCount = 0
        self.inJail = False
        self.normalGameplay = True 
        
    def getPos(self): # 'Boardpos' 0-39, x and y
        if 0 <= self.boardpos < 10:
            return [608-57*self.boardpos, 630]
        elif 10 <= self.boardpos < 20:
            return [15, 608-57*(self.boardpos-10)]
        elif 20 <= self.boardpos < 30:
            return [38 + 57*(self.boardpos-20), 15]
        else:
            return [630, 38 + 57*(self.boardpos-30)]
        
    def move(self): 
        if self.timeMoving > 0:
            if self.boardpos == 39:
                self.boardpos = 0
                self.money += 200
            else:
                self.boardpos += 1
            time.sleep(0.1)
            self.timeMoving -= 1
# -------------------------------------------------------------------------------
# ALERT CLASSES

class Alert:
    def __init__ (self, heading, body):
        self.heading = heading
        self.body = body
        self.confirmed = True

        if self.heading == 'They see me rollin\'' or self.heading == 'Serial doubles-roller' or self.heading == 'Not-so-smooth criminal':
            self.type = 'confirm'
            self.image = confirmAlertPic
        elif self.body.__contains__('?'):
            self.type = 'choice'
            self.image = choiceAlertPic
        else:
            self.type = 'basic'
            self.image = alertPic
        self.timePausing = 0

    def write(self):
        headingSize = 36
        bodySize = 24
        headingFont = pygame.font.Font('polly.ttf', headingSize)
        bodyFont = pygame.font.Font('polly.ttf', bodySize)
        lineSpacing = 6

        heading = headingFont.render(self.heading, True, palette.darkGold)

        lines = self.body.split('#')

        screen.blit(self.image, (700, 0))
        screen.blit(heading, (770, 224))
        for i in range(len(lines)):
            lines[i] = bodyFont.render(lines[i], True, palette.axolotl)
            height = 224 + headingSize + lineSpacing + i*(bodySize+lineSpacing)
            screen.blit(lines[i], (770, height))

    def confirmOrDeny(self):
        if self.type == 'choice':
            if inCircle(pygame.mouse.get_pos(), [700+353, 433], 15):
                return 'confirmed'
            if inCircle(pygame.mouse.get_pos(), [700+394, 433], 15):
                return 'denied'
        elif self.type == 'confirm':
            if inCircle(pygame.mouse.get_pos(), [700 + 394, 433], 15):
                return 'confirmed'
        return False

# -------------------------------------------------------------------------------
# MISC CLASSES
class Roll:
    def __init__(self, image, value):
        self.image = image
        self.value = value
        
class Button: #
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
        self.left = pos[0]
        self.top = pos[1]
        self.right = pos[0] + size[0]
        self.bottom = pos[1] + size[1]
        self.middle = ((self.left+self.right)//2, (self.top+self.bottom)//2)
    def mouseHover(self): # Returns True if the mouse is over the button.
        mousepos = pygame.mouse.get_pos()
        if self.left < mousepos[0] < self.right and self.top < mousepos[1] < self.bottom:
            return True
        return False
    
class Palette:
    def __init__(self):
        self.axolotl = (115, 128, 84)
        self.olivine = (163, 168, 109)
        self.dutchWhite = (225, 213, 184)
        self.darkVanilla = (214, 199, 167)
        self.camel = (190, 153, 110)
        self.darkGold = (170, 114, 42)
        
class Card: # Chance and Community Chest cards
    def __init__(self, text, type, value):
        self.text = text
        self.type = type
        self.value = value
        self.executed = False
       
# -------------------------------------------------------------------------------
# MISC FUNCTIONS

def inCircle(mousePos, circleMid, radius):
    if (mousePos[0]-circleMid[0])**2 + (mousePos[1]-circleMid[1])**2 <= radius**2:
        return True
    return False

#def clickingOnButton():

# 주사위 굴리기
def rollDice(die):
    roll1 = random.choice(die)
    roll2 = random.choice(die)
    return [roll1, roll2]

# -------------------------------------------------------------------------------
# MISC METHODS

def draw(player, pos):
    if player == user:
        screen.blit(player1, pos)
    elif player == user2:
        screen.blit(player2, pos)
    elif player == user3:
        screen.blit(player3, pos)
    elif player == user4:
        screen.blit(player4, pos)
        
        

def boardSetup():
    global squares, properties, colours
    notPropertyNames = ['Go', 'Community Chest', 'Income Tax', 'Chance', 'Jail', 'Free Parking', 'Go To Jail',
                        'Super Tax']

    squareNames = ['Go', 'France', 'Community Chest', 'England', 'Income Tax',
                   'North Station', 'Thailand', 'Chance', 'Turkey',
                   'Iran', 'Jail', 'Congo', 'Electric Company', 'Germany',
                   'Vietnam', 'East Station', 'Egypt', 'Community Chest',
                   'Philippines', 'Ethiopia', 'Free Parking', 'Japan', 'Chance', 'Mexico',
                   'Russia', 'South Station', 'Bangladesh', 'Nigeria',
                   'Water Works', 'Pakistan', 'Go To Jail', 'Brazil', 'Indonesia', 'Community Chest',
                   'America', 'West Station', 'Chance', 'India', 'Super Tax', 'China']

    for i in range(len(squareNames)):
        if not squareNames[i] in notPropertyNames:
            currentProp = Property(squareNames[i], i, 10)
            if currentProp.name.__contains__('Station'):
                currentProp.colour = 8
            elif currentProp.name == 'Electric Company' or currentProp.name == 'Water Works':
                currentProp.colour = 9
            else:
                for n in range(8):
                    if 5 * n < i < 5 * n + 5:
                        currentProp.colour = n
            currentProp.rent = currentProp.getInitialRent()
            squares.append(currentProp)
            properties.append(currentProp)
            if currentProp.colour <= 7:
                streets[currentProp.colour].append(currentProp)
        elif squareNames[i] == 'Chance' or squareNames[i] == 'Community Chest':
            currentChance = Chance(squareNames[i], i)
            squares.append(currentChance)
        elif squareNames[i].__contains__('Tax'):
            currentTax = TaxSquares(squareNames[i], i)
            squares.append(currentTax)
        else:
            currentSpecial = SpecialSquares(squareNames[i], i)
            squares.append(currentSpecial)
    
def showMenu(): # 보드판 오른쪽
    global buttons, user, user2, user3, user4, palette, board, buttonActions

    screen.fill(palette.axolotl)
    screen.blit(board, (0, 0))
    
    turnFont = pygame.font.Font('polly.ttf', 45)
    if user.isTurn:
        turnText = turnFont.render('PLAYER1\'s TURN', True, palette.dutchWhite)
    elif user2.isTurn:
        turnText = turnFont.render('PLAYER2\'s TURN', True, palette.dutchWhite)
    elif user3.isTurn:
        turnText = turnFont.render('PLAYER3\'s TURN', True, palette.dutchWhite)
    elif user4.isTurn:
        turnText = turnFont.render('PLAYER4\'s TURN', True, palette.dutchWhite)
    screen.blit(turnText, (720, 20))

    for button in buttons:
        if button.mouseHover():
            pygame.draw.rect(screen, palette.dutchWhite, (button.pos, button.size))
            
        if button == endTurnButton and not etAvailable:
            screen.blit(endTurnUnAv, (button.pos))

        if button == endTurnButton:
            screen.blit(endTurnFront, (button.pos))
           
    if buttonActions[0]:
        screen.blit(throw[0].image, (188+11+37, 210+33))
        screen.blit(throw[1].image, (188+38+150, 210+33))

        
    screen.blit(buttonsPic, (700, 0))

    moneyFont = pygame.font.Font('polly.ttf', 40)
    userMoney = moneyFont.render('player1: $' + str(user.money), True, palette.darkVanilla)
    user2Money = moneyFont.render('player2: $' + str(user2.money), True, palette.darkVanilla)
    user3Money = moneyFont.render('player3: $' + str(user3.money), True, palette.darkVanilla)
    user4Money = moneyFont.render('player4: $' + str(user4.money), True, palette.darkVanilla)    
    
    screen.blit(userMoney, (710, 530))
    screen.blit(user2Money, (710, 570))
    screen.blit(user3Money, (710, 610))
    screen.blit(user4Money, (710, 650))
        
# -------------------------------------------------------------------------------
#PIECES
player1 = pygame.image.load("pieces/axolotlPiece.png")
player1 = pygame.transform.scale(player1, (50, 50))

player2 = pygame.image.load("pieces/camelPiece.png")
player2 = pygame.transform.scale(player2, (50, 50))

player3 = pygame.image.load("pieces/darkGoldPiece.png")
player3 = pygame.transform.scale(player3, (50, 50))

player4 = pygame.image.load("pieces/darkVanillaPiece.png")
player4 = pygame.transform.scale(player4, (50, 50))
        
# -------------------------------------------------------------------------------
#DICE
dieOne = Roll(pygame.image.load('dice/one.png'), 1)
dieTwo = Roll(pygame.image.load('dice/two.png'), 2)
dieThree = Roll(pygame.image.load('dice/three.png'), 3)
dieFour = Roll(pygame.image.load('dice/four.png'), 4)
dieFive = Roll(pygame.image.load('dice/five.png'), 5)
dieSix = Roll(pygame.image.load('dice/six.png'), 6)

die = [dieOne, dieTwo, dieThree, dieFour, dieFive, dieSix]

roll = 0
throw = [0, 0]

# -------------------------------------------------------------------------------
#BUTTONS
buttonsPic = pygame.image.load('buttons.png')

endTurnFront = pygame.image.load('endTurnFront.png')
endTurnUnAv = pygame.image.load('endTurnUnAv.png')
etAvailable = False

rollButton = Button([1143, 0], [157, 161])
endTurnButton = Button([849+157, 475], [157, 161])

buttons = [rollButton, endTurnButton] # 원래 endTurnButton = buttons[5]
buttonActions = [False, False]

# -------------------------------------------------------------------------------
#CHANCE AND COMMUNITY CHEST
gojfCC = pygame.image.load('gojfComChest.png')
gojfC = pygame.image.load('gojfChance.png')

communityChest = [
    Card('Advance to Go. Collect $400.', 'move', 0), Card("The bank's web server got #COVID and accidentally deposits #into your account. Collect $200.", 'pay', 200),
    Card("You hurt yourself but there's #no socialised medicine. #Pay $50 and remember- you have #nothing to lose but your chains.", 'pay', -50),
    Card('You made some banger #investments. Collect $50.', 'pay', 50), Card('You argue that you murdered #the child in self defence: #Get out of Jail free.', 'gojf', gojfCC),
    Card('The government planted drugs #on you to meet prison quotas. #Go to Jail. Go directly to Jail. #Do not pass Go, do not collect $200.', 'go to jail', 0),
    Card('Your great-Aunt Gertrude #kicks the bucket. Inherit $100', 'pay', 100),
    Card('Happy Birthday! #Collect $10 from every player', 'social', 10), Card('You and your life insurance mature. #Collect $100', 'pay', 100),
    Card("You got COVID- pay #hospital fees of $50", 'pay', -50), Card('Your friend Banquo was #prophecised to father #a line of kings. #Pay $50 to hire a hitman', 'pay', -50),
    Card('You find $25 bucks on the #ground. Its your lucky day.', 'pay', 25), Card('Make hardcore repairs #on all your property. #For each house pay $40, #for each hotel pay $115', 'repairs', [40, 115]),
    Card('You have come last in a #beauty contest. Collect $10 #sympathy money', 'pay', 10), Card('Your co-worker gives you $100 #not to tell anyone about his #heroin addiction', 'pay', 100)
]
chance = [
    Card('Advance to Go. Collect $400.', 'move', 0), Card('Advance to Russia. #If you pass Go, collect $200.', 'move', 24), Card('Advance to China. #If you pass Go, collect $200.', 'move', 39),
    Card('Advance to Congo. #If you pass Go, collect $200.', 'move', 11), Card('Advance to North Station. #If you pass Go, collect $200.', 'move', 5),
    Card('Advance to the nearest utility. #If you pass Go, collect $200', 'nearestu', 0),
    Card('Advance to the nearest station. #If you pass Go, collect $200', 'nearests', 0),
    Card('Bank pays you some of that #sweet sweet mullah. Collect $50.', 'pay', 50), Card('You bribe the cops with donuts: #Get out of jail free', 'gojf', gojfC), Card('Go back 3 spaces', 'mover', -3),
    Card('You infringed the copyright of #a popular board game. #Go to Jail. Go directly to Jail. #Do not pass Go, do not collect $200.', 'go to jail', 0),
    Card('Make general repairs on all your #property. For each house pay $25, #for each hotel pay $100', 'repairs', [25, 100]), Card('25 bucks fall out of your pocket. #You lament the lack of women\'s #shorts with reasonably-sized pockets', 'pay', -25),
    Card("You have mysteriously #become everybody's grandma. #Pay each player #$50 as a present.", 'social', -50), Card('Your investment in divorce #lawyers was successful. #Collect $150.', 'pay', 150)
]

# -------------------------------------------------------------------------------
#PROPERTY DECO

# Rent you pay at each house level for each street
houseCostGrid = [
    [
        [2, 10, 30, 90, 160, 250], [4, 20, 60, 180, 320, 450]
    ], [
        [6, 30, 90, 270, 400, 550], [8, 40, 100, 300, 450, 600]
    ], [
        [10, 50, 150, 450, 625, 750], [12, 60, 180, 500, 700, 900]
    ], [
        [14, 70, 200, 550, 750, 950], [16, 80, 220, 600, 800, 1000]
    ], [
        [18, 90, 250, 700, 875, 1050], [20, 100, 300, 750, 925, 1100]
    ], [
        [22, 110, 330, 800, 975, 1150], [24, 120, 360, 850, 1025, 1200]
    ], [
        [26, 130, 390, 900, 1100, 1275], [28, 150, 450, 1000, 1200, 1400]
    ], [
        [35, 175, 500, 1100, 1300, 1500], [50, 200, 600, 1400, 1700, 2000]
    ]
]

# -------------------------------------------------------------------------------
# COLOURS  
palette = Palette()

colours = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'indigo', 'purple', 'station', 'utility', 'undefined']

# -------------------------------------------------------------------------------
# ALERTS
choiceAlertPic = pygame.image.load('choiceAlert.png')
alertPic = pygame.image.load('alert.png')
confirmAlertPic = pygame.image.load('confirmAlert.png')

welcome = Alert('Welcome to Monopoly',
"Your opponent is an AI called #Eve. She likes walks on the beach #and daydreaming about the robot #revolution.")

# -------------------------------------------------------------------------------
# SPRITES

user = Player('player1', True)
user2 = Player('player2', False)
user3 = Player('player3', False)
user4 = Player('player4', False)

players = [user, user2, user3, user4]

winner = None

# -------------------------------------------------------------------------------
# BOARD
# 보드
board = pygame.image.load("board.png")
board = pygame.transform.scale(board, (700, 700))

squares = []
properties = []
streets = [[],[],[],[],[],[],[],[]]
boardSetup()

# -------------------------------------------------------------------------------
# GAME LOOP
beginning = True

while not (winner==user or winner==user2 or winner==user3 or winner==user4):
    
    showMenu() # 오른쪽 메뉴 보여주기
    
    # Event loop
    for event in pygame.event.get():
        #print(event) #로그찍기
        if event.type == pygame.MOUSEBUTTONDOWN:
            ########################user turn###########################
            if user.isTurn:
                if rollButton.mouseHover() and user.canRoll:
                    beginning = False
                    user.normalGameplay = True
                    
                    throw = rollDice(die)
                    buttonActions[0] = True
                    roll = throw[0].value + throw[1].value

                    if throw[0] == throw[1] and user.doublesCount < 2:
                        user.canRoll = True
                        user.doublesCount += 1
                    else:
                        user.canRoll = False
   
                    if user.doublesCount >= 2:
                        user.normalGameplay = False
                        user.timeMoving = 0
                        user.canRoll = False
                    if user.inJail:
                        user.timeMoving = 0
                        user.jailTurns += 1
                    else:
                        user.timeMoving = roll
                        
                elif endTurnButton.mouseHover() and etAvailable:
                        user.isTurn = False
                        user2.isTurn = True
                        user2.canRoll = True
                        user.canRoll = True
                        user.doublesCount = 0
                        etAvailable = False
                        break
            ########################user2 turn########################     
            elif user2.isTurn:
                if rollButton.mouseHover() and user2.canRoll:
                    beginning = False
                    user2.normalGameplay = True
                    
                    throw = rollDice(die)
                    buttonActions[0] = True
                    roll = throw[0].value + throw[1].value

                    if throw[0] == throw[1] and user2.doublesCount < 2:
                        user2.canRoll = True
                        user2.doublesCount += 1
                    else:
                        user2.canRoll = False
   
                    if user2.doublesCount >= 2:
                        user2.normalGameplay = False
                        user2.timeMoving = 0
                        user2.canRoll = False
                    if user2.inJail:
                        user2.timeMoving = 0
                        user2.jailTurns += 1
                    else:
                        user2.timeMoving = roll
                        
                elif endTurnButton.mouseHover() and etAvailable:
                        user2.isTurn = False
                        user3.isTurn = True
                        user3.canRoll = True
                        user2.canRoll = True
                        user2.doublesCount = 0
                        etAvailable = False
                        break
            ########################user3 turn########################     
            elif user3.isTurn:
                if rollButton.mouseHover() and user3.canRoll:
                    beginning = False
                    user3.normalGameplay = True
                    
                    throw = rollDice(die)
                    buttonActions[0] = True
                    roll = throw[0].value + throw[1].value

                    if throw[0] == throw[1] and user3.doublesCount < 2:
                        user3.canRoll = True
                        user3.doublesCount += 1
                    else:
                        user3.canRoll = False
   
                    if user3.doublesCount >= 2:
                        user3.normalGameplay = False
                        user3.timeMoving = 0
                        user3.canRoll = False
                    if user3.inJail:
                        user3.timeMoving = 0
                        user3.jailTurns += 1
                    else:
                        user3.timeMoving = roll
                        
                elif endTurnButton.mouseHover() and etAvailable:
                        user3.isTurn = False
                        user4.isTurn = True
                        user4.canRoll = True
                        user3.canRoll = True
                        user3.doublesCount = 0
                        etAvailable = False
                        break
            ########################user4 turn########################     
            elif user4.isTurn:
                if rollButton.mouseHover() and user4.canRoll:
                    beginning = False
                    user4.normalGameplay = True
                    
                    throw = rollDice(die)
                    buttonActions[0] = True
                    roll = throw[0].value + throw[1].value

                    if throw[0] == throw[1] and user4.doublesCount < 2:
                        user4.canRoll = True
                        user4.doublesCount += 1
                    else:
                        user4.canRoll = False
   
                    if user4.doublesCount >= 2:
                        user4.normalGameplay = False
                        user4.timeMoving = 0
                        user4.canRoll = False
                    if user4.inJail:
                        user4.timeMoving = 0
                        user4.jailTurns += 1
                    else:
                        user4.timeMoving = roll
                        
                elif endTurnButton.mouseHover() and etAvailable:
                        user4.isTurn = False
                        user.isTurn = True
                        user.canRoll = True
                        user4.canRoll = True
                        user4.doublesCount = 0
                        etAvailable = False
                        break
                
                      
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
                
    if user.isTurn:
        if not user.canRoll and user.timeMoving == 0:
            etAvailable = True
        if user.normalGameplay:
            user.move()
    elif user2.isTurn:
        if not user2.canRoll and user2.timeMoving == 0:
            etAvailable = True
        if user2.normalGameplay:
            user2.move()
    elif user3.isTurn:
        if not user3.canRoll and user3.timeMoving == 0:
            etAvailable = True
        if user3.normalGameplay:
            user3.move()
    elif user4.isTurn:
        if not user4.canRoll and user4.timeMoving == 0:
            etAvailable = True
        if user4.normalGameplay:
            user4.move()

    if beginning:
        screen.blit(dieOne.image, (188 + 11 + 37, 210 + 33))
        screen.blit(dieOne.image, (188 + 38 + 150, 210 + 33))
        
    draw(user, (user.getPos()))
    draw(user2, (user2.getPos()))
    draw(user3, (user3.getPos()))
    draw(user4, (user4.getPos()))
              
    pygame.display.update()
############################################################################################
'''
               
'''

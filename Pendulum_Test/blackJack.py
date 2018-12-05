import random

spades = ['2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS','AS']
hearts = ['2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH','AH']
clubs = ['2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC','AC']
diamonds = ['2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD','AD']

one_deck = spades + hearts + clubs + diamonds

four_decks = one_deck + one_deck + one_deck + one_deck

standard_deck = four_decks[::]

cpu_hand = []
player_hand = []
split_hand = []

split_count = 0
cash = 0
pbet = 0
bet2 = 0
win1 = []
say_shuff = True

def blackjack():
    global cash
    cash = 1000
    shuff = 'no'

    play = input('Shall we play a game? (y/n)\n')
    
    if play == 'y':
        start_game()

    else:
        return print('Game Over. Your final total is $'+str(round(cash)))

        
    while cash > 0 and play == 'y' or play == 'shuffle':
        play = input('Play again? (y/n)\n')

        if play == 'y':
            reset()
            start_game()
            

        elif play == 'shuffle':
            shuffle()

        else:
            break    

    say_shuff = False
    shuffle()
    
    if cash > 0:
        print('Game Over. Your final total is $'+str(round(cash)))

    elif cash <= 0:
        print('Out of money. Better luck next time.')

    return

def start_game():
        global pbet

        pbet = bet()

        for n in range(2):
            cpu_hand.append(standard_deck[random.randint(0,len(standard_deck)-1)])
            standard_deck.remove(cpu_hand[len(cpu_hand)-1])
        
            player_hand.append(standard_deck[random.randint(0,len(standard_deck)-1)])
            standard_deck.remove(player_hand[len(player_hand)-1])

        print('\nDealer up card is ' + str(cpu_hand[0]))
        
        print('\nYour hand is ' + str(player_hand))

        play_hand(player_hand)

def play_hand(hand):
    global pbet
    global cash
    global bet2
    two_hands = 'n'
    player_hand = hand
    hit_count = 0
    dealerdoes = 'i'
    win = 'n'
    end = False

    while True:
        
        if value(player_hand) == 21:
            if split_count == 0:
                print('\n\nBLACKJACK! You win $'+str(round(pbet*1.5))+'\n')
                print('\nCards remaining: ' + str(len(standard_deck)))
                cash += (pbet*1.5)
                reset()
                return
            else:
                print('\nBLACKJACK!')
                win1.append('Blackjack')
                bet2  += (pbet*1.5)
                break
            
        if player_hand[0][0] == player_hand[1][0]:
            two_hands = input('Would you like to split your hand? (y/n)\n')

            if two_hands == 'y' and pbet <= (cash/2):
                split()
                return

            elif two_hands == 'y' and pbet > (cash/2):
                print('You do not have enough money for that.')
                
        action = input('\nWould you like to Hit(h), Stand(s), or Double Down(d)?\n')

        if action == 'add_money':
            amt = input('Amount to add: ')

            add_money(eval(amt))

            action = input('\nWould you like to Hit(h), Stand(s), or Double Down(d)?\n')

        if action == 'd' and pbet <= (cash/2):

                action = 's'
                pbet *= 2

                player_hand.append(standard_deck[random.randint(0,len(standard_deck)-1)])
                standard_deck.remove(player_hand[len(player_hand)-1])

                if value(player_hand) > 21:
                    if split_count == 0:
                        print('\n\nBUST. You lose $'+str(pbet)+'. Better luck next time.\n')
                    else:
                        win1.append('Bust')
                        bet2 -= pbet
                    end = True
                    break
                    
        elif action == 'd' and pbet > (cash/2):
            action = input('You do not have enough money for that. Would you like to Hit(h) or Stand(s)?\n')

        while action == 'h':
            
            player_hand.append(standard_deck[random.randint(0,len(standard_deck)-1)])
            standard_deck.remove(player_hand[len(player_hand)-1])

            if value(player_hand) == 21:
                action = 's'
                break
            
            if value(player_hand) > 21:
                if split_count == 0:
                    print('\n\nBUST. You lose $'+str(pbet)+'. Better luck next time.\n')
                else:
                    win1.append('Bust')
                    bet2 -= pbet
                end = True
                break

            else: print('\nYour hand is now ' + str(player_hand))

            action = input('\nWould you like to Hit(h) or Stand(s)?\n')

        if end == True:
            break

##To make cheater_bot, uncomment and statment below, and cooment out if statement below.
        
        while action == 's': #and value(player_hand) > value(cpu_hand):
            if value(cpu_hand) == 17 and soft(cpu_hand) == False:
                break

            elif value(cpu_hand) > 17:
                break

            else:
                cpu_hand.append(standard_deck[random.randint(0,len(standard_deck)-1)])
                standard_deck.remove(cpu_hand[len(cpu_hand)-1])
                if split_count == 0:
                    print('\nDealer hits')
                else:
                    hit_count += 1
                
        if action == 's' and value(cpu_hand) > 21:
            if split_count == 0:
                print('\nDealer BUST. You win $'+str(pbet)+'.\n')
            else:
                dealerdoes = 'Dealer BUST.'
            win = 'y'
            break

        elif action == 's' and split_count == 0:
            print('\nDealer stands')
            
        if action == 's' and value(player_hand) > value(cpu_hand):
            if split_count == 0:
                print('\n\nYou win $'+str(pbet)+'. Congratulations!\n')
            win = 'y'
            break

        elif action == 's' and value(player_hand) < value(cpu_hand):
            if split_count == 0:
                print('\n\nYou lose $'+str(pbet)+'. Better luck next time.\n')
            break
                
        elif action == 's' and value(player_hand) == value(cpu_hand):
            if split_count == 0:
                print('\n\nPush. You get $'+str(pbet)+' back.\n')
            win1.append('Push')
            break
        
        else:
            print('\n\nYou lose $'+str(pbet)+'. Next time try following directions cucc.\n')
            if split_count != 0:
                win1.append('Cucc')
                bet2 -= pbet
            else:
                print('\nCards remaining: ' + str(len(standard_deck)))
                cash -= (pbet)
                reset()
                return
        
    if dealerdoes == 'i':
        dealerdoes = '\nDealer stands.'

    for e in range(1):
        if len(win1) >= split_count and split_count != 0:
            break
        if win == 'n':
            bet2 -= pbet
            win1.append('Loss')
        elif win == 'y':
            bet2 += pbet
            win1.append('Win')

    if split_count == 0:
        print('\nDealer\'s hand: ' + str(cpu_hand))
        print('\nYour hand: ' + str(player_hand))
        print('\nCards remaining: ' + str(len(standard_deck)))
        cash += bet2
        reset()
        
    elif split_count == 2:
        for i in range(hit_count):
            print('\nDealer hits.')
        print(str(dealerdoes)+'\n')
        for i in range(2):
            print('Hand '+str(i+1)+' result: '+str(win1[i]))
        print('Final result is $'+str(round(bet2)))
        print('\nDealer\'s hand: ' + str(cpu_hand))
        for i in range(2):
            print('Hand '+str(i+1)+': '+str(split_hand[i]))
        print('\nCards remaining: ' + str(len(standard_deck)))
        cash += bet2
        reset()
        
    return
    
def value(hand):
    output = 0
    ace = False
    for card in hand:
        if card[0] == 'J' or card[0] == 'Q' or card[0] == 'K':
            output += 10

        elif card[0] == 'A':
            output += 1
            ace = True

        elif card[:2] == '10':
            output += 10

        elif type(eval(card[0])) == int and card[:2] != '10':
            output += eval(card[0])

    if ace == True and output <= 11:
        output += 10

    return output

def soft(hand):
    ace = False
    for card in hand:
        if card[0] == 'A':
            ace = True
    return ace

def split():
    player_hand_1 = []
    player_hand_2 = []
    two_hands = 'split'
    global split_count
    global pbet
  
    player_hand_2.append(player_hand[1])
    player_hand.remove(player_hand[1])
    player_hand_2.append(standard_deck[random.randint(0,len(standard_deck)-1)])
    standard_deck.remove(player_hand_2[len(player_hand)-1])

    player_hand_1.append(player_hand[0])
    player_hand.remove(player_hand[0])
    player_hand_1.append(standard_deck[random.randint(0,len(standard_deck)-1)])
    standard_deck.remove(player_hand_1[len(player_hand)-1])
    
    split_hand.append(player_hand_1)
    split_hand.append(player_hand_2)                                

    for hand in split_hand:
        
        split_count += 1

        print('\nHand ' + str(split_count) + ' is ' + str(hand))

        play_hand(hand)

    reset()
    return

def shuffle():
    global say_shuff

    standard_deck.clear()

    for card in four_decks:
        standard_deck.append(card)

    random.shuffle(standard_deck)

    if say_shuff == True:
        return print('Deck shuffled.\n')

    else:
        say_shuff = True
        return print('\n')

def bet():
    betnumber = 0
    Int = False
    print('You have $'+str(round(cash)))
    betnumber = input('What would you like to bet?\n')
    while Int == False:
        try:
            if type(eval(betnumber)) == int and eval(betnumber) <= cash and eval(betnumber) > 0:
                Int = True
                bet = int(eval(betnumber))
            elif eval(betnumber) > cash:
                print('Error. You do not have that much money to bet.')
                betnumber = input('What would you like to bet?\n')
            elif eval(betnumber) <= 0:
                print('Error. Nice try, but you have to bet a positive number')
                betnumber = input('What would you like to bet?\n')
            else:
                print('Error. Please enter a whole number amount for your bet.')
                betnumber = input('What would you like to bet?\n')
        except NameError:
            print('Error. Please enter a number for your bet.')
            betnumber = input('What would you like to bet?\n')
        except TypeError:
            print('Error. Please enter a number for your bet.')
            betnumber = input('What would you like to bet?\n')
            
    return bet

def add_money(amt):
    global cash
    cash += amt
    print('$'+str(amt)+' added to your balance.')
    print('\nDealer up card is ' + str(cpu_hand[0]))
    print('\nYour hand is ' + str(player_hand))
    return

def reset():
    global split_count
    global pbet
    global bet2
    global win1
    global say_shuff
    global cpu_hand
    global player_hand
    global split_hand
    
    cpu_hand = []
    player_hand = []
    split_hand = []

    split_count = 0
    pbet = 0
    bet2 = 0
    win1 = []
    say_shuff = True

blackyjack()
####################################################################################################
# File: 	millionaire.py                                                                         #
# A console simulation of a game Who Wants to Be a Millionaire                                     #
# Author: 	Ilya Ilyankou                                                                          #
# Date: 	November 2014                                                                          #
####################################################################################################

import millionairedb
import random
import time
import sys

def lets_wait(phrase, t):
  """ Implements a pause with dots """
  print("\n\n %s" % phrase)
  sys.stdout.flush()
  for i in range(t):
    print("."),
    time.sleep(1)
    sys.stdout.flush()


def intro_question(lvl):
  """ Generates introduction to the new question """
  lvl += 1
  bal = balance[lvl]
  v = [0 for i in range(9)]
  v[0] = "Here is question #%s worth $%s." % (lvl, bal)
  v[1] = "We're going to question #%s for you to win $%s." % (lvl, bal)
  v[2] = "Question #%s for $%s now." % (lvl, bal)
  v[3] = "This is the turn of question #%s that will get you $%s." % (lvl, bal)
  v[4] = "Now it is the turn of question #%s. Win $%s!" % (lvl, bal)
  v[5] = "Want $%s? Let's see how you can cope with question #%s!" % (bal, lvl)
  v[6] = "Let's see how much time it'll take you to answer question #%s and win $%s!" % (lvl, bal)
  v[7] = "Now onto question #%s. It is worth $%s." % (lvl, bal)
  v[8] = "Want go win $%s? Here's question #%s." % (bal, lvl)
  n = int (random.random() * 9)
  return v[n]
  

def ask_question(lvl):
  """ Generates a number and gets the question from the database """
  to_return = "\n " + intro_question(lvl) + "\n "
  to_return += "=" * (len(to_return) - 3) + "\n "
  qnum = int (random.random() * 10)
  
  global q
  q = millionairedb.get_question(lvl, qnum)
  to_return += q[0]
  to_return += "\n A. " + q[1] + "\t\t B. " + q[2]
  to_return += "\n C. " + q[3] + "\t\t D. " + q[4]

  global correct_answer
  correct_answer = q[5]
  return to_return


def check_answer(lvl):
  """ Checks the answer """
  answer = raw_input("\n You: ")
  answer = answer.lower()
  global correct_answer, q, help_friend_avail, help_50_avail, help_audience_avail

  if not (answer in acceptable_answers): # Checking if the input makes sence
    print "\n I don't understand what you mean. Enter the answer letter, 'help' to see available lifelines, or 'finish' to exit the game."
    check_answer(lvl)
  
  elif (answer == "help"): # If 'help' was entered
    print ""
    if (help_50_avail): print " "*5 + help_50
    if (help_friend_avail): print " "*5 + help_friend
    if (help_audience_avail): print " "*5 + help_audience
    if not (help_50_avail or help_friend_avail or help_audience_avail): # If all lifelines were used
      print "\n" + " "*5 + "You have no lifelines available..." 
    check_answer(lvl)

  elif (answer == "friend"):
    if (help_friend_avail == True):
      help_friend_avail = False
      if (random.random() < 0.7): # There is a ~70% chance that friend's guess will be the right one
        lets_wait("Calling your friend", 4)
        print "\n Your friend thinks the correct answer is %s." % correct_answer
        check_answer(lvl)
      else: # In case two answers were eliminated by 50:50
        while True:
          i = int (random.random()*4 + 1)
          if (q[i] != "" and q[i] != correct_answer):
            lets_wait("Calling your friend", 4)
            print "\n Your friend thinks the correct answer is %s." % correct_answer
            check_answer(lvl)
    else:
      print "\n You already used this lifeline. Enter 'help' to see what other lifelines are left."
      check_answer(lvl)
        
  elif (answer == "50"):
    if (help_50_avail == True):
      help_50_avail = False
      w = 0 # To track how many answers have been removed
      while True:
        if w == 2:
          break
        i = int (random.random()*4 + 1)
        if (correct_answer != q[i] and q[i] != ""):

          w += 1
          q[i] = ""

      print "\n We eliminated two incorrect answers. The two remaining are:"
      temp = [" A. ", " B. ", " C. ", " D. "]
      for i in range(1,5):
        if (q[i] != ""):
          print (temp[i-1] + q[i] + "\t\t"),
      print ""
      check_answer(lvl)
      
    else:
      print "\n You already used this lifeline. Enter 'help' to see what other lifelines are left."
      check_answer(lvl)

  elif (answer == "audience"):
    if (help_audience_avail == True):
      help_audience_avail = False
      while True: # Just to
        w = random.random()
        if (w > 0.45): # Just a number for the "majority" of the audience
          w = int (w*100)
          break

      if (random.random() < 0.8):
        audience_answer = correct_answer
      else: # In case some answers were eliminated by 50:50
        while True:
          i = int (random.random()*4 + 1)
          if (q[i] != ""):
            audience_answer = q[i]
            break

      lets_wait("The audience is voting", 4)
      print "\n The majority (%s%%) of the audience think that the correct answer is %s." % (w, audience_answer)
      check_answer(lvl)
      
    else:
      print "\n You already used this lifeline. Enter 'help' to see what other lifelines are left."
      check_answer(lvl)

  elif (answer == "finish"):
    print "\n You chose to finish the game, %s. You won $%s. Congratulations!" % (player, balance[lvl])
    quit()

  elif (answer == "a" or answer == "b" or answer == "c" or answer == "d"):
    if (correct_answer == q[ord(answer)-96]):
      if (lvl == 14):
        print(" ******* CONGRATULATIONS, %s! *************" % player.upper())
        print(" **********  YOU WON $1,000,000! *************")
        print(" You reached the top! This was an excellent game! Once again, congratulations!")
      else:
        print("\n You got it right, %s!\n You now have $%s.\n Let's proceed to question #%s!" % (player, balance[lvl+1], lvl+2))
        print ask_question(lvl+1)
        check_answer(lvl+1)
      
    else:
      print("\n Ups. The answer you chose is incorrect.\n The right answer is %s." % correct_answer)
      print(" Thank you for the game!")

      user_choice = raw_input("\n\n Would you like to to try one more time? (y/n)  ")
      if (user_choice.lower() == "y"):
        help_audience_avail = True
        help_50_avail = True
        help_friend_avail = True
        print ask_question(0)
        check_answer(0)
    


balance = [0, 100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]
level = 0   # Current question number
correct_answer = ""
q = []
acceptable_answers = ["a", "b", "c", "d", "50", "help", "audience", "friend", "finish"]
help_50 = "to use \"50:50\", enter '50'"
help_50_avail = True
help_friend = "to \"Phone a Friend\", enter 'friend'"
help_friend_avail = True
help_audience = "to \"Ask the Audience\", enter 'audience'"
help_audience_avail = True

print " *************************************************"
print " *            // who wants to be a \\\            *"
print " *            ||    MILLIONAIRE    ||            *"
print " *            \\\ who wants to be a //            *"
print " *************************************************\n"

print " Welcome to the show \"Who Wants to Be a Millionaire!\"\n"
player = raw_input(" What is your name? ")

print ("\n Let's start the game, %s! There will be 15 questions\n\
 that are arranged by difficulty. Simplier questions\n\
 go first and are worth less. Every question will have four \n\
 answer choices, of which only one is correct. Answering the hardest,\n\
 15th question, will make you a winner of $1,000,000! \n\n\
 Remember that you have 3 lifelines, each can be used only once:\n\
      %s\n\
      %s\n\
      %s\n\n\
 You can always enter 'help' to get reminded of these options.\n\n\
 So, let's get started!\n"
 % (player, help_50, help_friend, help_audience))

print ask_question(0)
check_answer(0);
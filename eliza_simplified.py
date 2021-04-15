#--------------------------------------------------------------------------------
#  eliza_simplified.py
#
#  a cheezy little Eliza knock-off by Joe Strout <joe@strout.net>
#  with some updates by Jeff Epler <jepler@inetnebr.com>
#  hacked into a module and updated by Jez Higgins <jez@jezuk.co.uk>
#  simplified and Py2/3 compatibility by Amir Zeldes <amir.zeldes@georgetown.edu>
#  last revised: 24 September 2017
#  modified by Ulie Xu <lx59@georgetown.edu>
#--------------------------------------------------------------------------------

import re
import random


#----------------------------------------------------------------------
# translate: take a string, replace any words found in dictionary as key
#  with the corresponding dictionary value
#----------------------------------------------------------------------
def translate(str,dict):
    words = str.lower().split()
    keys = dict.keys()
    words_modified = []
    for word in words:
        if word in keys:
            word = dict[word]
        words_modified.append(word)
    translation = ""
    for word in words_modified:
        translation = translation + " " + word
    return translation.strip()


#----------------------------------------------------------------------
#  respond: take a string, a dictionary of mappings, and find
#    corresponding responses in a list; find a match, and return a randomly
#    chosen response from the corresponding list.
#----------------------------------------------------------------------
def respond(str_in, mappings, reflections):
    # Find a match among patterns
    for pattern in mappings:
        match = re.match(pattern, str_in)
        if match is not None:
            # Found a match ... choose random response
            resp = random.choice(mappings[pattern])

            # Check if the response embeds something from the match (has '%%')
            if "%%" in resp:
                filler = match.group(1)
                translated_filler = translate(filler, reflections)
                resp = re.sub("%%", translated_filler, resp, count=1)

            # Fix munged punctuation at the end
            if resp[-2:] == '?.':
                resp = resp[:-2] + '.'
            if resp[-2:] == '??':
                resp = resp[:-2] + '?'
            return resp

#----------------------------------------------------------------------
# reflections, a translation table used to convert things you say
#    into things the computer says back, e.g. "I am" --> "you are"
#----------------------------------------------------------------------
reflections = {
  "am"   : "are",
  "was"  : "were",
  "i"    : "you",
  "i'd"  : "you would",
  "i've"  : "you have",
  "i'll"  : "you will",
  "my"  : "your",
  "are"  : "am",
  "you've": "I have",
  "you'll": "I will",
  "your"  : "my",
  "yours"  : "mine",
  "you"  : "me",
  "me"  : "you"
}

#----------------------------------------------------------------------
# pats, the main response table.  Each element of the list is a
#  two-element list; the first is a regexp, and the second is a
#  list of possible responses, with group-macros labelled as %%
#----------------------------------------------------------------------
pats = [
  [r'I need (.*)',
  [  r"Why do you need %%?",
    r"Would it really help you to get %%?",
    r"Are you sure you need %%?"]],
  
  [r'Why don\'?t you ([^\?]*)\??',
  [  r"Do you really think I don't %%?",
    r"Perhaps eventually I will %%.",
    r"Do you really want me to %%?"]],
  
  [r'Why can\'?t I ([^\?]*)\??',
  [  r"Do you think you should be able to %%?",
    r"If you could %%, what would you do?",
    r"I don't know -- why can't you %%?",
    "Have you really tried?"]],
  
  [r'I can\'?t (.*)',
  [  r"How do you know you can't %%?",
    r"Perhaps you could %% if you tried.",
    r"What would it take for you to %%?"]],
  
  [r'I am (.*)',
  [  r"Did you come to me because you are %%?",
    r"How long have you been %%?",
    r"How do you feel about being %%?"]],
  
  [r'I\'?m (.*)',
  [  r"How does being %% make you feel?",
    r"Do you enjoy being %%?",
    r"Why do you tell me you're %%?",
    r"Why do you think you're %%?"]],
  
  [r'Are you ([^\?]*)\??',
  [  r"Why does it matter whether I am %%?",
    r"Would you prefer it if I were not %%?",
    r"Perhaps you believe I am %%.",
    r"I may be %% -- what do you think?"]],
  
  [r'What (.*)',
  [  "Why do you ask?",
    "How would an answer to that help you?",
    "What do you think?"]],
  
  [r'How (.*)',
  [  "How do you suppose?",
    "Perhaps you can answer your own question.",
    "What is it you're really asking?"]],
  
  [r'Because (.*)',
  [  "Is that the real reason?",
    "What other reasons come to mind?",
    "Does that reason apply to anything else?",
    r"If %%, what else must be true?"]],
  
  [r'(.*) sorry (.*)',
  [  "There are many times when no apology is needed.",
    "What feelings do you have when you apologize?"]],
  
  [r'Hello(.*)',
  [  "Hello... I'm glad you could drop by today.",
    "Hi there... how are you today?",
    "Hello, how are you feeling today?"]],
  
  [r'I think (.*)',
  [  r"Do you doubt %%?",
    "Do you really think so?",
    r"But you're not sure %%?"]],
  
  [r'(.*) friend (.*)',
  [  "Tell me more about your friends.",
    "When you think of a friend, what comes to mind?",
    "Why don't you tell me about a childhood friend?"]],
  
  [r'Yes',
  [  "You seem quite sure.",
    "OK, but can you elaborate a bit?"]],
  
  [r'(.*) computer(.*)',
  [  "Are you really talking about me?",
    "Does it seem strange to talk to a computer?",
    "How do computers make you feel?",
    "Do you feel threatened by computers?"]],
  
  [r'Is it (.*)',
  [  r"Do you think it is %%?",
    r"Perhaps it's %% -- what do you think?",
    r"If it were %%, what would you do?",
    r"It could well be that %%."]],
  
  [r'It is (.*)',
  [  "You seem very certain.",
    r"If I told you that it probably isn't %%, what would you feel?"]],
  
  [r'Can you ([^\?]*)\??',
  [  r"What makes you think I can't %%?",
    r"If I could %%, then what?",
    r"Why do you ask if I can %%?"]],
  
  [r'Can I ([^\?]*)\??',
  [  r"Perhaps you don't want to %%.",
    r"Do you want to be able to %%?",
    r"If you could %%, would you?"]],
  
  [r'You are (.*)',
  [  r"Why do you think I am %%?",
    r"Does it please you to think that I'm %%?",
    r"Perhaps you would like me to be %%.",
    "Perhaps you're really talking about yourself?"]],
  
  [r'You\'?re (.*)',
  [  r"Why do you say I am %%?",
    r"Why do you think I am %%?",
    "Are we talking about you, or me?"]],
  
  [r'I don\'?t (.*)',
  [  r"Don't you really %%?",
    r"Why don't you %%?",
    r"Do you want to %%?"]],
  
  [r'I feel (.*)',
  [  "Good, tell me more about these feelings.",
    r"Do you often feel %%?",
    r"When do you usually feel %%?",
    r"When you feel %%, what do you do?"]],
  
  [r'I have (.*)',
  [  r"Why do you tell me that you've %%?",
    r"Have you really %%?",
    r"Now that you have %%, what will you do next?"]],
  
  [r'I would (.*)',
  [  r"Could you explain why you would %%?",
    r"Why would you %%?",
    r"Who else knows that you would %%?"]],
  
  [r'Is there (.*)',
  [  r"Do you think there is %%?",
    r"It's likely that there is %%.",
    r"Would you like there to be %%?"]],
  
  [r'My (.*)',
  [  r"I see, your %%.",
    r"Why do you say that your %%?",
    r"When your %%, how do you feel?"]],
  
  [r'You (.*)',
  [  "We should be discussing you, not me.",
    "Why do you say that about me?",
    r"Why do you care whether I %%?"]],
    
  [r'Why (.*)',
  [  r"Why don't you tell me the reason why %%?",
    r"Why do you think %%?" ]],
    
  [r'I want (.*)',
  [  r"What would it mean to you if you got %%?",
    r"Why do you want %%?",
    r"What would you do if you got %%?",
    r"If you got %%, then what would you do?"]],
  
  [r'(.*) (?:mother|mom|mum)(.*)',
  [  "Tell me more about your mother.",
    "What was your relationship with your mother like?",
    "How do you feel about your mother?",
    "Do like like your mother?",
    "Good family relations are important."]],
  
  [r'(.*) (?:father|dad)(.*)',
  [  "Tell me more about your father.",
    "How did your father make you feel?",
    "How do you feel about your father?",
    "Does your relationship with your father relate to your feelings today?",
    "Do you have trouble showing affection with your family?"]],

  [r'(.*) child(.*)',
  [  "Did you have close friends as a child?",
    "What is your favorite childhood memory?",
    "Do you remember any dreams or nightmares from childhood?",
    "Did the other children sometimes tease you?",
    "How do you think your childhood experiences relate to your feelings today?"]],

[r'(.*) friend(.*)',
  [  "Do you have many friends",
    "How do you treat your friends?",
    "Do your friends treat you well?",
    "Do you consider yourself close with the friend?"]],

[r'(.*) ?school(.*)',
  [  "What do you think of school?",
    "How do you like school?",
    "How are you doing in school?",
    "What was your favorate memory from school?",
    "What did you learn in school today?"]],

[r'(.*) (?:argue|argument|conflict)(.*)',
 # ?: is a prefix that makes the grouping not interfere with other numbered groups
  [  "Why did this argument start?",
    "Who do you think is in the wrong?",
    "Who do you think should apologize?",
    "Can you reflect if you did anything wrong?",
    "How do you feel about the conflict now?"]],

[r'(.*) (stress|stressful|stressed out)(.*)',
  [  "Take a deep breath first.",
    "What is causing you the stress?",
    "Maybe you can take a bath tonight.",
    "Maybe you should take a break from your tasks right now and go for a walk.",
    "Let's try finishing our tasks one thing at a time."]],

[r'(.*) difficult(.*)',
  [  "Why is it difficult?",
    "Do you want to talk more about why it's difficult?",
    "Maybe there is an easier approach to it.",
    "Have you asked for help from others?"]],

[r'(.*) (?:fuck|fucking|bitch)(.*)',
  [  "Wow we PG13 here sir/ma'am, mind your language :))",
     "Hey don't say that word again :)",
     "Let's try calming down and not using profanity to express our emotions."]],

  [r'(.*)\?',
  [  "Why do you ask that?",
    "Please consider whether you can answer your own question.",
    "Perhaps the answer lies within yourself?",
    "Why don't you tell me?"]],
  
  [r'quit',
  [  "Thank you for talking with me.",
    "Good-bye.",
    "It's always good to talk it out. Have a good day :)"]],

[r'((good)?bye|see you)',
  [  "Thank you for talking with me.",
    "Good-bye.",
    "It's always good to talk it out. Have a good day :)"]],
  
  [r'(.*)',
  [  "Please tell me more.",
    "Let's change focus a bit... Tell me about your family.",
    "Can you elaborate on that?",
    r"Why do you say that %%?",
    "I see.",
    "Very interesting.",
    r"%%.",
    "I see.  And what does that tell you?",
    "How does that make you feel?",
    "How do you feel when you say that?"]]
  ]



#----------------------------------------------------------------------
#  command_interface
#----------------------------------------------------------------------
print("Therapist\n---------")
print("Talk to the program by typing in plain English, using normal upper-")
print('and lower-case letters and punctuation.  Enter "quit" when done.')
print('='*72)
print("Hello.  How are you feeling today?")
s = ""

# Make an empty dictionary called mappings
mappings = {}
for pattern in pats: # Go through patterns
    find = pattern[0]  # The first item in each pattern is the regex to find
    replacements = pattern[1]  # The second item is itself a list of possible replacements
    mappings[find] = replacements

while s != "quit":
    try:
        s = raw_input(">")
    except NameError:
        s = input(">")
    if len(s) < 1:
        s = "quit"
        print(s)
    s = re.sub(r"[\.!]$", "", s)        # Remove trailing punctuation
    response = respond(s, mappings, reflections)
    print(response)


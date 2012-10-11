import string
import re
import copy
import os
import sys

sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=150))

os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )

def getwordlist(file):
	f = open(file)
	wordlist = []
	for word in f:
		word = word[:-2]
		wordlist.append(word)
	return wordlist

def hashword(wordlist):
	hashed_words = {}
	for lettered_word in wordlist:
		numbered_word = lettered_word
		n = str(0)
		for character in numbered_word:
			if character.isalpha():
				numbered_word = numbered_word.replace(character, n)
			if n in numbered_word:
				n = str(int(n) + 1)
		hashed_words[lettered_word]=numbered_word
	return hashed_words

def letter_match_gen(possible_matches, possible_letters):
	for word in possible_matches:
		n = 0
		current_word_possibilities = []
		while n<len(word):
			if possible_letters[(word[n])]==[]: #for first occurrence of puzzle letter
				for answer in possible_matches[word]:
					if word[n] != answer[n].upper() and answer[n] not in possible_letters[(word[n])]:
						possible_letters[(word[n])].append(answer[n])
			else:
				for answer in possible_matches[word]:
					if word[n] != answer[n].upper() and answer[n] not in current_word_possibilities:
						current_word_possibilities.append(answer[n])
				possible_letters[(word[n])] = list(set(possible_letters[(word[n])]) & set(current_word_possibilities))
			n+=1
	for coded_letter in possible_letters:  #checks to ensure that any possible translation is in a possible word
		n = 0
		while n < len(possible_letters[coded_letter]):
			possible_letter_solution = possible_letters[coded_letter][n]
			for coded_word in possible_matches:
				if coded_letter in coded_word:
					choices = []
					coded_letter_position = coded_word.find(coded_letter)
					for possible_word_solution in possible_matches[coded_word]:
						choices.append(possible_word_solution[coded_letter_position])
					if possible_letter_solution not in choices and possible_letter_solution in possible_letters[coded_letter]:
						possible_letters[coded_letter].remove(possible_letter_solution)
			n+=1	
	return possible_matches, possible_letters

def solution_key_generator(possible_matches, possible_letters, solution_key):
	possible_matches, possible_letters = letter_match_gen(possible_matches, possible_letters)
	for coded_letter in possible_letters:
		if len(possible_letters[coded_letter]) == 1:
			used = possible_letters[coded_letter][0]
			solution_key[coded_letter] = used
			for other_letter in possible_letters:
				if other_letter != coded_letter:
					if used in possible_letters[other_letter]:
						possible_letters[other_letter].remove(used)	
	return possible_matches, possible_letters, solution_key
						
def pruner(possible_matches, possible_letters, solution_key):
	do_again = False
	for word in possible_matches:
		bad_values = []
		for value in possible_matches[word]:
			n=0
			while n < len(word):
				if value[n] not in possible_letters[word[n]]:
					if value not in bad_values:
						bad_values.append(value)
				n+=1
		if bad_values:
			for item in bad_values:
				if item in possible_matches[word]:
					possible_matches[word].remove(item)
			do_again = True
	possible_matches, possible_letters, solution_key = solution_key_generator(possible_matches, possible_letters, solution_key)
	possible_matches, possible_letters = letter_match_gen(possible_matches, possible_letters)
	if do_again:
		return pruner(possible_matches, possible_letters, solution_key)
	else:
		possible_matches, possible_letters, solution_key = solution_key_generator(possible_matches, possible_letters, solution_key)
		return possible_matches, possible_letters, solution_key
	
def wordcheck(word, wordlist):	
	wordset = set(wordlist)
	return word in wordset

def replacer(puzzle, a, b):
	full_puzzle = puzzle.replace(a,b)
	return full_puzzle
	
puzzle1 = "CTNWJC KC, ZWL P LVPSH LVPJ ACSOPSR KYNVPSC PJ ZMQHCS. P HCEL EWFFPSR LVC FCACMJ, ZWL SQ JSYNHJ NYKC QWL."
puzzle2 = "STEQHV THBZQX PQVDV KQNDX AHXYUW VHEEDX VBQXE, SDTXV EDEQYX DXTVDA. SPTVZ AXYID RTGLHK DCYVBV, NQXAV VTIDA. BJKYUW XDUDNV."
puzzle3 = "X ZWZPKPPZKC - FPZKSGO GPFWIP NUG X 'GUXRK JWKCUSK PBSXT' FUZRWRKR UN RPLPZKPPZ MWGER -- WZFTSEWZH X KSGAPO, X ESFA, XZE X BSXWT -- PXFC RKSNNPE WZRWEP KCP IGPLWUSR UZP."

def solver(full_puzzle):
	puzzle = ""
	for char in full_puzzle:
		if char.isalpha() or char == " ":
			puzzle += char
	hashed_database = hashword(wordlist) #creates comprehensive database of words and hashed equivalents
	puzzle.upper()
	definite_letters = []
	solution_key = {}
	#empty_strings = ["" for i in range(len(letters_in_puzzle))]
	puzzle = puzzle.split()
	empty_lists = [[] for i in range(26)]	
	possible_letters = dict(zip(string.ascii_uppercase,empty_lists))				
	hashed_puzzle = hashword(puzzle)
	possible_matches = {}
	for word in hashed_puzzle:
		current_hash = hashed_puzzle[word]
		possible_matches[word] = []
		for key in hashed_database:
			if hashed_database[key]==current_hash:
				possible_matches[word].append(key)
	possible_matches, possible_letters = letter_match_gen(possible_matches, possible_letters)
	possible_matches, possible_letters, solution_key = pruner(possible_matches, possible_letters, solution_key)
	for k,v in solution_key.iteritems():
		full_puzzle = replacer(full_puzzle, k, v)
	full_puzzle = full_puzzle.upper()
	return full_puzzle

wordlist = getwordlist('2of12inf.txt')
print puzzle1
print solver(puzzle1)
print("\r\n")
print puzzle2
print solver(puzzle2)
print("\r\n")
print puzzle3
print solver(puzzle3)
print("\r\n")


#PROBABLY JUNK CODE :(
# 	after_apostrophe = ['t','s','d','m']
# 	for char in puzzle:
# 		if char.isalpha():
# 			solution += str(0)
# 		else: 
# 			solution += char

# 	for word in puzzle: #check if completed word is good
# 		if word.islower():
# 			if not wordcheck(word, wordlist):
# 				return

# 	for word in puzzle:
# 		if "'" in word:  #CONTRACTIONS
# 			if len(word[word.find("'"):]) ==2: #one letter after apostrophe:
# 				pass		
# 			if len(word[word.find("'"):]) == 3: #two letters after apostrophe:
# 				if word[word.find("'") + 1] == word[word.find("'") + 2]:
# 					solution_key[word[word.find("'") + 1]] = 'l'
# 					puzzle = replacer(puzzle, word[word.find("'") + 1], 'l')
# 					definite_letters.append('l')	
# 				else:
# 					solution_key[word[word.find("'") + 2]] = 'e'
# 					puzzle = replacer(puzzle, word[word.find("'") + 2], 'e')
# 					definite_letters.append('e')

# def letter_frequency(wordlist):
# 	alphabet = list(string.letters[:26] + "'")
# 	zeroes = [0 for i in range(27)]
# 	letter_count = dict(zip(alphabet,zeroes))
# 	for word in wordlist:
# 		for char in word[:-1]: #ignores terminal space
# 			letter_count[char] += 1
# 	sorted_letter_count = sorted(letter_count, key = lambda letter: letter_count[letter])
# 	sorted_letter_count.reverse()
# 	return sorted_letter_count
# 	
# def combination_frequency(wordlist):
# 	alphabet_punct = list(string.letters[:26] + " " + "'") #lowercase letters, space, apost
# 	zeroes = [0 for i in range(28)]
# 	second_letters = dict(zip(alphabet_punct,zeroes))
# 	combos = dict(zip(alphabet_punct,[second_letters for i in range(28)]))
# 	for word in wordlist:
# 		for char in range(len(word)-1):  #loops over word stopping before /r
# 			combos[word[char]][word[char+1]] += 1
# 	for first_letter in combos:			
# 		sub_dict = combos[first_letter]
# 		sorted_list = sorted(sub_dict, key = lambda letter: sub_dict[letter])
# 		sorted_list.reverse()
# 		combos[first_letter] = sorted_list
# 	return combos
# 	
# def initial_letters(wordlist):
# 	alphabet = list(string.letters[:26])
# 	zeroes = [0 for i in range(26)]
# 	initial_letters = dict(zip(alphabet,zeroes)) #creates alphabet dictionary
# 	for word in wordlist:
# 		initial_letters[word[0]] +=1
# 	return initial_letters

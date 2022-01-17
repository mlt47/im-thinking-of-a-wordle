import five_letter_words # local file
import string

def get_constraints_from_feedback(guess, feedback):
  """Adds constraints to constraint dict from feedback"""
  # exit early on non valid feedback
  if not feedback or feedback == "0" or \
     any(char not in string.digits + "," for char in feedback):
    return {}

  # handle csv and short-hand input
  constraints = {}
  for position in feedback if "," not in feedback else feedback.split(","):
    if position:
      index = int(position) - 1
      constraints[guess[index]] = index
  return constraints

# initialise values and constraints
shoulds = {}
musts = {}
must_nots = set()
possible_words = five_letter_words.words
finished = False

while not finished:
  # filter words by any recorded constraints
  filtered_words = []
  for word in possible_words:
    if all(letter not in must_nots for letter in word) and \
       all(word[position] == letter for letter, position in musts.items()) and \
       all(letter in word for letter, position in shoulds.items()) and \
       all(word[position] != letter for letter, position in shoulds.items()):
      filtered_words.append(word)
      # further optimisation: shoulds can have more than one position which mean additional constraints
  possible_words = filtered_words
  print(f"Considering {len(possible_words)} words...")

  # count positional letter occurrance for filtered words
  letter_counts = {c: [0, 0, 0, 0, 0] for c in string.ascii_lowercase}
  for word in possible_words:
    for index, letter in enumerate(word):
      letter_counts[letter][index] += 1

  # find max word score form filtered words
  max_word_score = 0
  guess = "?"
  for word in possible_words:
    # caluclate word score heuristic from letter occurance in the corpus
    any_position_count = sum(sum(letter_counts[l]) for l in set(word) if l not in {**shoulds, **musts})
    positional_count = sum(letter_counts[l][i] for i, l in enumerate(word)  if l not in {**shoulds, **musts})  
    word_score = any_position_count + 2*positional_count
    if word_score > max_word_score:
      max_word_score = word_score
      guess = word

  # evaluate guess from wordle feedback
  print(f"Let's try '{guess}'")

  must_positions = input("What are the positions of any green letters? ")
  if must_positions not in {"12345", "done", "correct", "all", "all green"}:
    musts.update(get_constraints_from_feedback(guess, must_positions))

    should_positions = input("What are the positions of any yellow letters? ")
    shoulds.update(get_constraints_from_feedback(guess, should_positions))

    for letter in guess:
      if letter not in shoulds and letter not in musts:
        must_nots.add(letter)
  else:
    finished = True

# success
print("Yay! 🥳")

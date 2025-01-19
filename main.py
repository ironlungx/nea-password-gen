from random import randint
import os
from rich import print as p_print
from rich.prompt import Prompt

class LengthError(Exception):
  pass


def menu(options: list[str], header: str) -> str:
  for i, x in enumerate(options):
    p_print(f"[blue]{i+1}.[/blue] {x}")

  while True:
    try:
      p_print(f'[bold blue]{header}: [/bold blue]', end='')
      choice = int(input(""))
      return options[choice - 1]

    except (ValueError, IndexError):
      p_print('[bold red]Enter a valid number[/bold red]')

def clear():
  os.system('clear' if os.name == 'posix' else 'cls')

def generate_password(length: int) -> str:
  allowed_chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!$%^&*()-_=+'
  while True:
    password = ''
    for x in range(0, length - 1):
      char = allowed_chars[randint(0, len(allowed_chars) - 1)]
      password += char

    if grade_password(password) > 20:
      return password

def grade_password(password: str) -> int:
  row_1 = "qwertyuiop"
  row_2 = "asdfghjkl"
  row_3 = "zxcvbnm"

  keyboard = [
    [x for x in row_1],
    [x for x in row_2],
    [x for x in row_3]
  ]
  allowed_symbols = '!$%^&*()-_=+'

  tmp = password
  score = len(password)

  if len(tmp.strip('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890!$%^&*()-_=+')) > 0:
    raise ValueError()

  hasUpper = False
  hasLower = False
  hasNumber = False
  hasSymbol = False

  # Check if the password has *any* uppercase letters
  # let password = 'wOrd' 
  # This if statement will equate to true in this case
  if any(char.isupper() for char in password):
    score += 5
    hasUpper = True
    # print(f'hasUpper +5 {score}')

  # Check if the password has *any* lowercase letters
  # let password = 'WoRD' 
  # This if statement will equate to true in this case
  if any(char.islower() for char in password):
    score += 5
    hasLower = True
    # print(f'hasLower +5 {score}')

  # Check if the password has *any* numbers 
  # let password = 'This is a str1ng' 
  # This if statement will equate to true in this case
  if any(char.isdigit() for char in password):
    score += 5
    hasNumber = True
    # print(f'hasNumber +5 {score}')


  # Check if the password has *any* of the allowed symbols 
  # let password = 'This is a str1ng!$' 
  # This if statement will equate to true in this case
  if any(char in allowed_symbols for char in password):
    score += 5
    hasSymbol = True
    # print(f'hasSymbols +5 {score}')

  # If all of the conditions are met, then add another 10 points
  if hasNumber and hasLower and hasUpper and hasSymbol:
    score += 10
    # print(f'all the conditions were met  +10{score}')

  if all([x.isupper() for x in password]):
    score -= 5
    # print(f'all upper -5 {score}')

  if all([x.islower() for x in password]):
    score -= 5
    # print(f'all lower -5 {score}')

  if password.isdigit():
    score -= 5
    # print(f'all digits -5 {score}')

  # The passsword only contains the allowed symbols
  # let password = '$!!^'
  
  tmp = password
  if len(tmp.strip(allowed_symbols)) == 0:
    score -= 5

  paswd_split = []
  tmp = password.lower()
  for x in range(2, len(tmp)):
    paswd_split.append(tmp[x-2:x+1])


  for x in paswd_split:
    if x in row_1:
      score -= 5
      # print(f'sequence of letters  -5{x}')
    if x in row_2:
      score -= 5
      # print(f'sequence of letters  -5{x}')
    if x in row_3:
      score -= 5
      # print(f'sequence of letters  -5{x}')

  return score

if __name__ == '__main__':
  try:
    while True:
      # choice = Prompt.ask("What do you want to do?", choices=["Check password", "Generate a password", "About", "Exit"], default="Generate a password", case_sensitive=False)
      choice = menu(["Check password", "Generate a password", "About", "Exit"], "Choose an option")
      if choice == "Exit":
        raise KeyboardInterrupt
      elif choice == "Check password":
        passwd = Prompt.ask("Enter the password")
        if len(passwd) > 28 or len(passwd) < 8:
          p_print("[bold red]Enter a password smaller than 28 and greater than 8[/bold red]")
          continue

        score = grade_password(passwd)
        color = ''
        if score > 20:
          color = 'green'
        elif score < 20 and score > 0: 
          color = 'yellow'
        else:
          color = 'red'

        p_print(f'The score for the password [blue]{passwd}[/blue] is [{color}]{score}[/{color}]')

      elif choice == "Generate a password":
        length = randint(8, 12)
        passwd = generate_password(length)
        print(passwd)

      elif choice == "About":
        ...

  except KeyboardInterrupt:
    print('Bye.....')
    exit(0)

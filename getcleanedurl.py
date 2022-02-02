import time

def getLines(filename: str = '') -> None:
    """Stop running the program using the sys module."""
    lines = []
    with open(filename) as file:
      while line := file.readline():
          newline = line.rstrip()
          if newline != '':
            lines.append(newline)

    lines = list(set(lines))
    return lines

lines1 = getLines("./datas/urls_test1.txt")
time.sleep(1)

lines2 = getLines("./datas/urls_test2.txt")
time.sleep(1)

lines3 = getLines("./datas/urls_test3.txt")
time.sleep(1)

lines4 = getLines("./datas/urls_test4.txt")
time.sleep(1)

lines5 = getLines("./datas/urls_test5.txt")
time.sleep(1)

allines = lines1 + lines2 + lines3 + lines4 + lines5
allines = list(set(allines))

with open("./datas/urls_cleaned.txt", 'w') as f:
  f.write('\n'.join(allines))
  f.close()

print('\nAll done! Urls is now cleaned')
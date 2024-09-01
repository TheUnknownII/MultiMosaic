import random

def generate_log():
  timestamp = random.randrange(1692418213,1695096646,6400)
  level = random.choice(["INFO", "WARNING", "ERROR"])
  message = "This is a log message."
  return "{} {} {}".format(timestamp, level, message)

with open("../log.txt", "w") as f:
  for i in range(100):
    f.write(generate_log() + "\n")
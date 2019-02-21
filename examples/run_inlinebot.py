import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from telegramnews import inlinebot

inlinebot.run()

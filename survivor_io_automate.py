#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  This script is an autoclicker for Survivor.io
  running in BlueStacks on the same machine
"""

# Python native modules
import logging

# Third-party modules
import pyautogui

# Custom modules
from io_battle import Battle
from io_utils import Utils

class SurvivorIO:
  def __init__(self, window_name = "BlueStacks App Player"):
    # Initialize config
    Utils(window_name)
    if not Utils.init_complete:
      raise RuntimeError("Utils class was not initialized!")

    self.Battle = Battle()

  def startTrial(self) -> bool:
    if button := Utils.locateOnScreen("challenge_start_button.png"):
      Utils.clickButton("challenge_start_button.png", button_loc=button)
      return True
    else:
      logging.error("Challenge start window not found!")
      return False

  def runBattle(self) -> bool:
    if self.Battle.runBattle():
      if (button := Utils.locateOnScreen("menu_optional_close.png")) is not None:
        logging.info("Closing optional dialog")
        Utils.clickButton("menu_optional_close.png", button_loc=button)
      return True
    return False


def main():
  game = SurvivorIO()

  while True:
    sep = "==================================="
    print(f"\n{sep}\n"
          "What to do?\n"
          " 1. Start Trial Battle + Run Battle\n"
          " 2. Run Battle\n"
          "\n CTRL+C to exit\n"
          f"{sep}\n")
    
    if (key := input("Input: ")) not in ("1", "2"):
      logging.info("Unknown input")
      continue

    if key == "1":
      if game.startTrial():
        key = "2"

    if key == "2":
      game.runBattle()


if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
  try:
    main()
  except KeyboardInterrupt:
    # Catch Keyboard Interrupts so that terminal is cleared at the end
    pass

  # Clear terminal 
  pyautogui.hotkey("ctrl", "u")

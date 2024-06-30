#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  This script is an autoclicker for Survivor.io
  running in BlueStacks on the same machine
"""

# Python native imports
import logging
from time import sleep

# Third-party imports
import PIL.Image
import keyboard
import PIL
import pyautogui
import pywinauto


class SurvivorIO:
  window_name = "BlueStacks App Player"
  callback_shared: bool | str = False
  image_cache: dict[str, PIL.Image.Image] = {}

  def __init__(self):
    SurvivorIO.region = getWindowRegion(SurvivorIO.window_name)
    SurvivorIO.center = (SurvivorIO.region[0] + SurvivorIO.region[2]/2,
                         SurvivorIO.region[1] + SurvivorIO.region[3]/2)

  @staticmethod
  def _getImage(image: str):
    if image not in SurvivorIO.image_cache:
      logging.info(f"Opening {image} and saving in cache")
      SurvivorIO.image_cache[image] = PIL.Image.open(image)
    return SurvivorIO.image_cache[image]

  def startTrial(self):
    if button := self.locateOnScreen("challenge_start_button.png"):
      pyautogui.leftClick(button)
    else:
      print("Challenge start window not found!")

  def runBattle(self):
    keyboard.on_release(callback_battle)
    SurvivorIO.callback_shared = True

    logging.info("Battle started")

    while SurvivorIO.callback_shared:
      sleep(0.2)
      if SurvivorIO.callback_shared == "skip_automate":
        continue

      if self.locateOnScreen("battle_skill_choice.png"):
        logging.info("Skill choice detected")
        pyautogui.leftClick(SurvivorIO.center)

      if button := self.locateOnScreen("battle_treasure_next.png"):
        logging.info("Treasure detected")
        pyautogui.leftClick(button)

      if button := self.locateOnScreen("battle_success.png"): 
        logging.info("Battle success!")
        pyautogui.leftClick(button)
        break
    
    logging.info("Waiting 8 seconds to return to main menu")
    sleep(8)
    if (center := SurvivorIO.locateOnScreen("menu_optional_close.png")) is not None:
      logging.info("Closing optional dialog")
      pyautogui.leftClick(center)

    keyboard.unhook_all()

  @staticmethod
  def locateOnScreen(image, optional: bool = True) -> tuple | None:
    try:
      return pyautogui.locateCenterOnScreen(image=SurvivorIO._getImage(f"resources/{image}"),
                                            confidence=0.9,
                                            region=SurvivorIO.region)
    except pyautogui.ImageNotFoundException:
      if optional:
        return None
      raise


def callback_battle(keyboard_event: keyboard.KeyboardEvent):
  if keyboard_event.name == "s":
    if SurvivorIO.callback_shared != "skip_automate":
      SurvivorIO.callback_shared = "skip_automate"
      logging.info("Battle Automation disabled")
    else:
      SurvivorIO.callback_shared = True
      logging.info("Battle Automation enabled")

  if keyboard_event.name == "e":
    for image in ("battle_pause.png", "battle_home.png", "battle_quit.png"):
      center = SurvivorIO.locateOnScreen(image, optional=False)
      pyautogui.leftClick(center)
      sleep(1)

    SurvivorIO.callback_shared = False


def getWindowRegion(window_name: str) -> tuple[int, int, int, int]:
    """
    Find and return BlueStacks App Player region

    Returns:
    - region: tuple - tuple of four elements (x, y of top left, width, height of region)
    """
    for window in pywinauto.Desktop(backend="uia").windows():
        if window.window_text() != window_name:
            continue

        logging.info("BlueStacks App Player found!")
        rectangle = window.rectangle()

        return (rectangle.left,
                rectangle.top, 
                rectangle.right - rectangle.left,
                rectangle.bottom - rectangle.top)

    raise RuntimeError("BlueStacks App Player not open")


def main():
  game = SurvivorIO()

  while True:
    print("What to do?\n"
          " 1. Start Trial Battle + Run Battle\n"
          " 2. Run Battle\n"
          "\n CTRL+C to exit")
    
    if (key := input("Input: ")) not in ("1", "2"):
      logging.info("Unknown input")
      continue

    if key == "1":
      game.startTrial()
      key = "2"

    if key == "2":
      game.runBattle()


if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
  main()

  # Clear terminal 
  pyautogui.hotkey("ctrl", "u")

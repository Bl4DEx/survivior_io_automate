# Python native modules
import logging
from time import sleep

# Third-party modules
import keyboard
import pyautogui

# Custom modules
from io_utils import Utils

class Battle:
  callback_shared: bool | str = False

  @staticmethod
  def _locate(image: str) -> tuple[int, int] | None:
    return Utils.locateOnScreen(image=image, sub="battle")

  @staticmethod
  def _clickButton(image: str, button_loc: tuple[int, int] | None):
    Utils.clickButton(image=image, sub="battle", button_loc=button_loc)

  def is_battle_detected(self, timeout: int = 10) -> bool:
    logging.info("Detecting battle for %d seconds", timeout)
    detect_battle_counter = 0
    while True:
      if detect_battle_counter >= timeout:
        logging.error("Battle not detected!")
        return False
      if self._locate("battle_pause.png") or self._locate("battle_pause_background.png"):
        logging.info("Battle detected!")
        return True

      sleep(1)
      detect_battle_counter += 1

  def runBattle(self) -> bool:
    if not self.is_battle_detected():
      return False

    keyboard.on_release(Battle.callback_battle)
    Battle.callback_shared = True

    while Battle.callback_shared:
      sleep(0.2)
      if Battle.callback_shared == "skip_automate":
        continue
      
      if Battle.callback_shared == "exit_battle":
        if self.exitBattle():
          break

      if self._locate("battle_skill_choice.png"):
        logging.info("Skill choice detected")
        pyautogui.leftClick(Utils.window_center)

      if self._locate("battle_treasure.png"):
        logging.info("Treasure detected")
        for sfx in ("start", "finish"):
            image = f"battle_treasure_next_{sfx}.png"
            while (button := self._locate(image)) is None:
                pass
            sleep(0.5)
            Battle._clickButton(image, button_loc=button)

      if button := self._locate("battle_success.png"): 
        logging.info("Battle success!")
        Battle._clickButton("battle_success.png", button_loc=button)
        break

    logging.info("Waiting 10 seconds to return to main menu")
    sleep(10)
    keyboard.unhook_all()
    return True

  def exitBattle(self) -> bool:
    for image in ("battle_pause.png", "battle_home.png", "battle_quit.png"):
        try:
            button = self._locate(image)
        except pyautogui.ImageNotFoundException:
          return False
        Battle._clickButton(image, button)
        sleep(1)
    return True

  @staticmethod
  def callback_battle(keyboard_event: keyboard.KeyboardEvent):
    if keyboard_event.name == "s":
      if Battle.callback_shared != "skip_automate":
        Battle.callback_shared = "skip_automate"
        logging.info("Battle Automation disabled")
      else:
        Battle.callback_shared = True
        logging.info("Battle Automation enabled")

    if keyboard_event.name == "e":
      logging.info("Returning to main window")
      Battle.callback_shared = "exit_battle"




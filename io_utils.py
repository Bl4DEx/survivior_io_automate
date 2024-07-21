# Python native imports
import logging
from time import sleep

# Third-party imports
import PIL.Image
import pyautogui
import pywinauto
from pathlib import Path

class Utils:
  callback_shared: bool | str = False
  image_cache: dict[Path, PIL.Image.Image] = {}
  window_region: tuple[int, int, int, int] = (0, 0, 0, 0)
  window_center: tuple[int, int] = (0, 0)
  init_complete = False

  def __init__(self, window_name: str):
    Utils.window_region = self._getWindowRegion(window_name)
    Utils.window_center = self._findCenter(Utils.window_region)
    Utils.init_complete = True

  @staticmethod
  def _getWindowRegion(window_name: str) -> tuple[int, int, int, int]:
      """
      Find and return window region

      Returns:
      - region: tuple - tuple of four elements (x, y of top left, width, height of region)
      """
      for window in pywinauto.Desktop(backend="uia").windows():
          if window.window_text() != window_name:
              continue

          logging.info("Window '%s' found!", window_name)
          rectangle = window.rectangle()

          return (rectangle.left,
                  rectangle.top, 
                  rectangle.right - rectangle.left,
                  rectangle.bottom - rectangle.top)

      raise RuntimeError("Window '%s' not found!", window_name)

  @staticmethod
  def _findCenter(region: tuple[int, int, int, int]) -> tuple[int, int]:
    return (region[0] + int(region[2]/2),
            region[1] + int(region[3]/2))

  @staticmethod
  def _getImage(sub: str, image: str) -> PIL.Image.Image:
    path = Path(__file__).parent / "resources" / sub / image
    if not path.is_file():
      raise FileNotFoundError(f"{path} not found!")
    if path not in Utils.image_cache:
      logging.debug(f"Opening {path} and saving in cache")
      Utils.image_cache[path] = PIL.Image.open(path)
    return Utils.image_cache[path]

  @staticmethod
  def locateOnScreen(image: str, optional: bool = True, sub: str = "") -> tuple[int, int] | None:
    try:
      return pyautogui.locateCenterOnScreen(image=Utils._getImage(sub=sub, image=image),
                                            confidence=0.9,
                                            region=Utils.window_region)  # type: ignore
    except pyautogui.ImageNotFoundException:
      if optional:
        return None
      raise

  @staticmethod
  def clickButton(image: str, button_loc: tuple[int, int] | None, sub: str = ""):
    while True:
      if button_loc:
        pyautogui.leftClick(button_loc)
      sleep(0.5)
      button_loc = Utils.locateOnScreen(image=image, sub=sub)
      if button_loc is None:
        break

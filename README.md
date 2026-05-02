# Not-So-Classic Game of Snake

A weird little project built around `pyautogui` — a Python library that takes control of your mouse.

Inspired by a [CodeBullet](https://www.youtube.com/@CodeBullet) video where he made a Snake game that eats System32 files (the most critical files in a Windows installation). This is not that. This will **not** touch your System32 files — it just moves desktop icons around to make a janky snake game.

---

## Setup

1. Create a folder on your desktop named exactly:
   ```
   safe_zone_pilkmilk_cursed_game_folder
   ```
2. Place `kat.jpg` inside that folder.
3. Place the folder in the **top-left corner** of your desktop — this is important for the grid origin.
4. Set your desktop path in `cursed_python/.env`:
   ```
   USER_PATH=C:\Users\YourName\Desktop
   ```

---

## Controls

| Key | Action |
|-----|--------|
| `W` `A` `S` `D` | Move |
| `O` | Check current score |
| `P` | Kill-switch — stops everything and cleans up |

**Optional (likely to break things):**

| Key | Action |
|-----|--------|
| `J` | Mouse down (pick up) |
| `K` | Mouse up (drop) |

---

## Adjusting the Grid Size

In `set_grid()`, two variables control how many desktop cells are used:

```python
cols = 19
rows = 9
```

This is the full screen. For a smaller, safer play area, try:

```python
cols = 9
rows = 5
```

Honestly this is your problem so figure out whats the best game size for yourself. Keep it over 1 x 1 and depending on how big your icons are also keep it under 20 by 9 

---

## Warning

This script uses `mouseDown()` and `mouseUp()` from `pyautogui` to drag icons. If your desktop is not cleared, it **will** accidentally move things you did not intend to move. Either clean up your desktop or shrink the grid before running.

If anything goes haywire, press `P`. It will stop execution and attempt a cleanup.


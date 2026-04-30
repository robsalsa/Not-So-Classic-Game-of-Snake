import ctypes
import os
import random
import shutil
import time
from pathlib import Path

import keyboard
import pyautogui
from dotenv import load_dotenv


# Grid settings for desktop traversal.
app_distance_x = 95
app_distance_y = 105
app_starting_line_x = 50
app_starting_line_y = 30

grid = []
snake_body = [(0, 0)]
direction = "Stop"
running = True
setup_complete = False
shutdown_requested = False

apples = []
apple_files = {}
current_score = 0
round_target = 0

FOLDER_START_POS = (0, 0)
START_POS = (0, 0)
folder_pos = FOLDER_START_POS
MASTER_KAT_PATH = Path(__file__).resolve().parent / "apples" / "kat_master.jpg"

# Drag timing tuned so desktop icon drags register consistently.
DRAG_HOLD_DELAY = 0.06
PLACEMENT_DRAG_MOVE_DURATION = 0.175
DRAG_MOVE_DURATION = 0
POST_DROP_DELAY = 0.075
FILE_APPEAR_DELAY = 0.3
BETWEEN_ICON_DELAY = 0.225

load_dotenv(Path(__file__).resolve().parent / ".env")
USER_PATH = os.getenv("USER_PATH")


def get_desktop_path():
    if not USER_PATH:
        return None
    return Path(os.path.expandvars(USER_PATH)).expanduser()


def get_safe_zone_folder():
    desktop = get_desktop_path()
    if not desktop:
        return None
    return desktop / "safe_zone_pilkmilk_cursed_game_folder"


# Tell Windows Explorer a file was created so the desktop icon appears immediately.
_SHCNE_CREATE = 0x00000002
_SHCNE_DELETE = 0x00000004
_SHCNF_PATH = 0x0005


def notify_shell_created(path):
    ctypes.windll.shell32.SHChangeNotify(_SHCNE_CREATE, _SHCNF_PATH, str(path), None)


def notify_shell_deleted(path):
    ctypes.windll.shell32.SHChangeNotify(_SHCNE_DELETE, _SHCNF_PATH, str(path), None)


def wait_for_path(path, timeout=3.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists():
            return True
        time.sleep(0.025)
    return path.exists()


def ensure_master_kat(safe_zone_folder):
    source_kat = safe_zone_folder / "kat.jpg"

    if MASTER_KAT_PATH.exists():
        return True

    if not source_kat.exists():
        source_kat = next(
            (
                file_path
                for file_path in safe_zone_folder.iterdir()
                if file_path.suffix.lower() == ".jpg" and file_path.stem.startswith("kat")
            ),
            None,
        )

    if not source_kat:
        return False

    MASTER_KAT_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(source_kat), str(MASTER_KAT_PATH))
    return True


def hard_kill():
    # Immediate stop with cleanup, then hard exit.
    global running, setup_complete, shutdown_requested, direction
    shutdown_requested = True
    running = False
    setup_complete = False
    direction = "Stop"

    restore_folder_to_origin()
    cleanup_desktop()
    normalize_game_folder()

    keyboard.unhook_all()
    os._exit(0)


def drag_between_cells(source_pos, target_pos):
    if not grid:
        return
    source_x, source_y = grid[source_pos[0]][source_pos[1]]
    target_x, target_y = grid[target_pos[0]][target_pos[1]]

    pyautogui.moveTo(source_x, source_y, duration=DRAG_MOVE_DURATION)
    pyautogui.mouseDown()
    time.sleep(DRAG_HOLD_DELAY)
    pyautogui.moveTo(target_x, target_y, duration=DRAG_MOVE_DURATION)
    pyautogui.mouseUp()
    time.sleep(POST_DROP_DELAY)


def set_grid():
    cols = 19
    rows = 9
    global grid
    grid = []

    for row_index in range(rows):
        row_center = []
        for col_index in range(cols):
            center_x = app_starting_line_x + (col_index * app_distance_x)
            center_y = app_starting_line_y + (row_index * app_distance_y)
            row_center.append((center_x, center_y))
        grid.append(row_center)


def button_comp(event):
    global direction

    # Kill-switch must always work, even during setup lock.
    if event.name == "p":
        hard_kill()
        return

    # Ignore all other keys until setup is complete.
    if not setup_complete:
        return

    if event.name == "w" and direction != "down":
        direction = "up"
    elif event.name == "s" and direction != "up":
        direction = "down"
    elif event.name == "a" and direction != "right":
        direction = "left"
    elif event.name == "d" and direction != "left":
        direction = "right"
    elif event.name == "j":
        pyautogui.mouseDown()
    elif event.name == "k":
        pyautogui.mouseUp()
    elif event.name == "o":
        count_score()


keyboard.on_press(button_comp)


def get_next(pos):
    row, col = pos
    if direction == "up":
        return (row - 1, col)
    if direction == "down":
        return (row + 1, col)
    if direction == "left":
        return (row, col - 1)
    if direction == "right":
        return (row, col + 1)
    return pos


def perform_step():
    global snake_body, current_score, direction

    if shutdown_requested:
        return

    head = snake_body[0]
    next_pos = get_next(head)

    if not (0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0])):
        return

    x, y = grid[next_pos[0]][next_pos[1]]
    pyautogui.moveTo(x, y)
    snake_body[0] = next_pos

    if next_pos in apples:
        apples.remove(next_pos)
        eaten_file = apple_files.pop(next_pos, None)
        if eaten_file and eaten_file.exists():
            eaten_file.unlink()
        current_score += 1
        print(f"score: {current_score}/{round_target}")

        if current_score >= round_target:
            print("Round complete! Resetting score and starting new round.")
            current_score = 0
            direction = "Stop"
            snake_body = [START_POS]
            setting_up_the_apples()


def count_score():
    pyautogui.alert(f"score: {current_score}/{round_target}")


def cleanup_desktop():
    desktop = get_desktop_path()
    if not desktop or not desktop.exists():
        return

    removed = 0
    for file_path in desktop.iterdir():
        if file_path.suffix.lower() == ".jpg" and file_path.stem.startswith("kat"):
            file_path.unlink()
            removed += 1
    print(f"Cleaned up {removed} kat image(s) from desktop")


def normalize_game_folder():
    safe_zone_folder = get_safe_zone_folder()
    if not safe_zone_folder or not safe_zone_folder.is_dir():
        return

    if not ensure_master_kat(safe_zone_folder):
        return

    for file_path in safe_zone_folder.iterdir():
        if file_path.suffix.lower() == ".jpg" and file_path.stem.startswith("kat"):
            file_path.unlink()

    canonical = safe_zone_folder / "kat.jpg"
    shutil.copy2(str(MASTER_KAT_PATH), str(canonical))


def restore_folder_to_origin():
    global folder_pos
    if not grid:
        return
    if folder_pos != FOLDER_START_POS:
        drag_between_cells(folder_pos, FOLDER_START_POS)
        folder_pos = FOLDER_START_POS


def cleanup_folder_copies(safe_zone_folder):
    for file_path in safe_zone_folder.iterdir():
        if file_path.suffix.lower() == ".jpg" and "- Copy" in file_path.stem:
            file_path.unlink()


def build_round_files(safe_zone_folder, image_count):
    if not ensure_master_kat(safe_zone_folder):
        return None, []

    cleanup_folder_copies(safe_zone_folder)

    source_kat = safe_zone_folder / "kat.jpg"
    if not source_kat.exists():
        shutil.copy2(str(MASTER_KAT_PATH), str(source_kat))

    copies = []
    for i in range(max(0, image_count - 1)):
        copy_name = "kat - Copy.jpg" if i == 0 else f"kat - Copy ({i + 1}).jpg"
        copy_path = safe_zone_folder / copy_name
        shutil.copy2(str(MASTER_KAT_PATH), str(copy_path))
        copies.append(copy_path)

    return source_kat, copies


def checking_the_board():
    if not USER_PATH:
        print("USER_PATH is not set in .env")
        return False

    safe_zone_folder = get_safe_zone_folder()
    if not safe_zone_folder:
        return False
    if safe_zone_folder.is_dir():
        print("safe_zone_pilkmilk_cursed_game_folder FOUND!! YIPPE!!!")
        return True

    print(f"safe_zone_pilkmilk_cursed_game_folder not found at: {safe_zone_folder}")
    return False


def setting_up_the_apples():
    global apples, apple_files, setup_complete, folder_pos, round_target, DRAG_MOVE_DURATION
    setup_complete = False

    if shutdown_requested:
        return

    if not USER_PATH:
        print("Theres no path inside of the .env. Fix that please")
        setup_complete = True
        return

    desktop = get_desktop_path()
    safe_zone_folder = get_safe_zone_folder()
    if not desktop or not safe_zone_folder:
        setup_complete = True
        return

    cleanup_desktop()
    normalize_game_folder()

    if not safe_zone_folder.is_dir():
        print("safe_zone_pilkmilk_cursed_game_folder missing on desktop")
        setup_complete = True
        return

    rows = len(grid)
    cols = len(grid[0]) if grid else 0
    if rows == 0 or cols == 0:
        setup_complete = True
        return

    # Strictly less than one quarter of the full grid.
    max_images = max(1, (rows * cols - 1) // 4)
    image_count = random.randint(1, max_images)

    source_kat, copy_files = build_round_files(safe_zone_folder, image_count)
    if not source_kat:
        print("No kat.jpg found in safe_zone_pilkmilk_cursed_game_folder")
        setup_complete = True
        return

    all_positions = [
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if (r, c) != FOLDER_START_POS
    ]

    if len(all_positions) < 2:
        print("Not enough free grid positions")
        setup_complete = True
        return

    files_in_order = [source_kat] + copy_files
    max_placeable = len(all_positions) - 1
    files_in_order = files_in_order[:max_placeable]

    next_folder_pos = random.choice(all_positions)
    placeable_positions = [pos for pos in all_positions if pos != next_folder_pos]
    chosen_positions = random.sample(placeable_positions, len(files_in_order))

    DRAG_MOVE_DURATION = PLACEMENT_DRAG_MOVE_DURATION
    try:
        # Move folder from its current recorded position only once per round.
        if next_folder_pos != folder_pos:
            drag_between_cells(folder_pos, next_folder_pos)
        folder_pos = next_folder_pos

        # Drag out original first, then copies.
        # Each icon is copied and moved fully before the next one is created.
        apples = []
        apple_files = {}
        for idx, kat_file in enumerate(files_in_order):
            dest = desktop / ("kat.jpg" if idx == 0 else f"kat_{idx}.jpg")
            if dest.exists():
                dest.unlink()

            # Move exactly one file out of the folder, notify Explorer immediately,
            # then drag it away before creating the next icon.
            shutil.move(str(kat_file), str(dest))
            notify_shell_deleted(kat_file)
            notify_shell_created(dest)
            if not wait_for_path(dest):
                print(f"Desktop icon did not appear in time: {dest.name}")
                continue
            time.sleep(FILE_APPEAR_DELAY)

            target_pos = chosen_positions[idx]
            # New desktop icons default to origin; always drag from 0,0.
            drag_between_cells(START_POS, target_pos)
            time.sleep(BETWEEN_ICON_DELAY)
            apples.append(target_pos)
            apple_files[target_pos] = dest

        # Purge any kat images that failed to move out — folder must be empty.
        for leftover in safe_zone_folder.iterdir():
            if leftover.suffix.lower() == ".jpg" and leftover.stem.startswith("kat"):
                leftover.unlink()
                notify_shell_deleted(leftover)
                print(f"Purged leftover from folder: {leftover.name}")
    finally:
        DRAG_MOVE_DURATION = 0

    round_target = len(apples)
    start_x, start_y = grid[START_POS[0]][START_POS[1]]
    pyautogui.moveTo(start_x, start_y)
    print(f"Round setup complete. folder at {folder_pos}, apples={round_target}")
    setup_complete = True


if checking_the_board():
    set_grid()
    setting_up_the_apples()
    pyautogui.moveTo(*grid[0][0])

    while running:
        perform_step()
        time.sleep(0.1)

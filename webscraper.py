from main import main, print_grid
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput import keyboard
import time



grid = [[0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [2, 0, 2, 0, 2, 0],
        [0, 0, 0, 1, 0, 0],
        [2, 0, 2, 0, 0, 0],
        [0, 2, 0, 2, 0, 0]]

n = 6

def on_press(key):
    try:
        # Check if the pressed key is 's'
        if key.char == 's':
            # Stop listener
            return False
    except AttributeError:
        pass  # Handle special key event

def quit_driver(browser):
    def on_press(key):
        try:
            if key.char == 'q':  # Press 'q' to quit
                browser.quit()
                return False  # Stop listener
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

def webscraping(input_size):
    # The browser
    browser = webdriver.Chrome()
    browser.get("https://0hh1.com/")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    while True:
        # Start game by clicking the grid size
        try:
            # Use WebDriverWait to wait for the element to be clickable
            grid_size_selector = f'div[data-action="startGame"][data-gridsize="{input_size}"]'
            grid_size_element = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, grid_size_selector))
            )
            grid_size_element.click()
            print(f"Clicked on grid size {input_size}")
        except Exception as e:
            print(f"An error occurred: {e}")
            # Add a delay to see what happens before closing the browser
            time.sleep(2)
            browser.quit()

        # Generate the input grid
        try:
            time.sleep(0.1)
            # Initialize an empty grid
            grid = [[None for _ in range(input_size)] for _ in range(input_size)]
            # The tiles to clikc on later
            tiles = []
            cur_idx = 0
            clicked = []

            # Loop through all possible x, y coordinates
            for x in range(input_size):
                for y in range(input_size):
                    # Construct the ID for the tile at the current coordinates
                    tile_id = f"tile-{x}-{y}"
                    # Wait until the tile element is present
                    WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.ID, tile_id))
                    )
                    # Find the tile element
                    tile_element = browser.find_element(By.ID, tile_id)
                    tiles.append(tile_element)
                    class_name = tile_element.get_attribute('class')
                    # Determine the status of the tile based on its class
                    if 'tile-1' in class_name:
                        grid[y][x] = 1  # Yellow
                        clicked.append(cur_idx)
                    elif 'tile-2' in class_name:
                        grid[y][x] = 2  # Blue
                        clicked.append(cur_idx)
                    else:
                        grid[y][x] = 0  # Empty
                    cur_idx += 1

            # Print the grid for verification
            print_grid(grid)
            

        except Exception as e:
            print(f"An error occurred: {e}")

        # Solve the grid
        main(grid, input_size)

        # Print the solved grid for verification
        print("solved grid: ")
        print_grid(grid)

        # Conver the array into a list it goes down the right
        clicks = []
        for i in range(input_size):
            for j in range(input_size):
                clicks.append(grid[j][i])

        # Finally solve it
        cur_idx = 0
        for tile in tiles:
            if cur_idx not in clicked:
                tile.click()
                if clicks[cur_idx] == 2:
                    tile.click()
            cur_idx += 1

        # TODO handle the 5 games pop up thing
        # quit_driver(browser)
webscraping(6)

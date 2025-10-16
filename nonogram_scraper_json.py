"""
Scraper for Pixelogic 5x5 Nonogram puzzles
Extracts row and column hints from all puzzles on the page
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json

def setup_driver():
    """Set up Chrome driver with headless option"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')  # Use new headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Add user agent to avoid detection
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except:
        # Fallback to basic setup
        driver = webdriver.Chrome(options=options)
    
    return driver

def close_popup(driver):
    """Close the congratulations popup if it appears"""
    try:
        wait = WebDriverWait(driver, 5)
        # Look for "Look around" button or any button to close the popup
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if "Look around" in button.text or "Show stats" in button.text:
                button.click()
                print("Closed popup")
                time.sleep(1)
                return True
    except:
        pass
    return False

def extract_hints(driver):
    """Extract row and column hints from the current puzzle"""
    try:
        # Wait for the loader to appear first
        # print("Waiting for loader...")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "pixelogic-infinite-player-loader"))
        )
        
        # Now wait for the actual player to load inside the loader
        # print("Waiting for player to load inside loader...")
        # time.sleep(1)  # Reduced from 3 to 1
        
        # Get the loader element
        loader_element = driver.find_element(By.TAG_NAME, "pixelogic-infinite-player-loader")
        loader_shadow = driver.execute_script('return arguments[0].shadowRoot', loader_element)
        
        if not loader_shadow:
            print("Loader shadow root is null!")
            return None
        
        # Find the player inside the loader's shadow DOM using CSS selector
        # print("Looking for player inside loader shadow DOM...")
        player_element = loader_shadow.find_element(By.CSS_SELECTOR, "pixelogic-infinite-player")
        
        # Access shadow DOM of the player
        # print("Accessing player shadow DOM...")
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', player_element)
        
        if not shadow_root:
            print("Shadow root is null!")
            return None
        
        # Look for mini-player inside shadow root using CSS selector
        # print("Looking for mini-player...")
        mini_player = shadow_root.find_element(By.CSS_SELECTOR, "mini-player")
        mini_shadow = driver.execute_script('return arguments[0].shadowRoot', mini_player)
        
        if not mini_shadow:
            print("Mini player shadow root is null!")
            return None
        
        # Now find the hints within the shadow DOM
        # print("Looking for row-hints in shadow DOM...")
        row_hints_container = mini_shadow.find_element(By.CLASS_NAME, "row-hints")
        row_hint_elements = row_hints_container.find_elements(By.CLASS_NAME, "hints")
        
        # print(f"Found {len(row_hint_elements)} row hint elements")
        
        row_hints = []
        for hint_elem in row_hint_elements:
            hint_text = hint_elem.text.strip()
            if hint_text:
                hint_numbers = [int(x) for x in hint_text.split() if x.isdigit()]
                row_hints.append(hint_numbers if hint_numbers else [0])
            else:
                row_hints.append([0])
        
        # Extract column hints
        # print("Looking for col-hints in shadow DOM...")
        col_hints_container = mini_shadow.find_element(By.CLASS_NAME, "col-hints")
        col_hint_elements = col_hints_container.find_elements(By.CLASS_NAME, "hints")
        
        # print(f"Found {len(col_hint_elements)} col hint elements")
        
        col_hints = []
        for hint_elem in col_hint_elements:
            hint_text = hint_elem.text.strip()
            if hint_text:
                hint_numbers = [int(x) for x in hint_text.split() if x.isdigit()]
                col_hints.append(hint_numbers if hint_numbers else [0])
            else:
                col_hints.append([0])
        
        # print(f"Successfully extracted: {len(row_hints)} rows, {len(col_hints)} cols")
        
        return {
            'row_hints': row_hints,
            'col_hints': col_hints
        }
    except Exception as e:
        print(f"Error extracting hints: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_puzzle_number(driver):
    """Get the current puzzle number"""
    try:
        # Look for puzzle number in URL or on page
        url = driver.current_url
        if '#' in url:
            return url.split('#')[1]
        return None
    except:
        return None

def scrape_all_puzzles(base_url, max_puzzles=100):
    """
    Scrape all nonogram puzzles from the page
    
    Args:
        base_url: Base URL of the puzzle page
        max_puzzles: Maximum number of puzzles to scrape
    
    Returns:
        Dictionary mapping puzzle numbers to their hints
    """
    driver = setup_driver()
    all_puzzles = {}
    
    try:
        for puzzle_num in range(1, max_puzzles + 1):
            url = f"{base_url}#{puzzle_num}"
            print(f"\nScraping puzzle #{puzzle_num}...")
            
            try:
                driver.get(url)
                time.sleep(1.5)  # Reduced from 4 to 1.5
                
                hints = extract_hints(driver)
                if hints and (hints['row_hints'] or hints['col_hints']):
                    all_puzzles[puzzle_num] = hints
                    print(f"✓ Successfully scraped puzzle #{puzzle_num}")
                else:
                    print(f"✗ Could not extract hints for puzzle #{puzzle_num}")
                    # If we can't find hints, we may have reached the end
                    if puzzle_num > 10:  # Only break after first 10 to account for errors
                        break
            except Exception as e:
                print(f"✗ Error on puzzle #{puzzle_num}: {e}")
                if puzzle_num > 10:
                    break
        
    finally:
        driver.quit()
    
    return all_puzzles

def save_to_file(puzzles, filename='nonogram_puzzles.json'):
    """Save puzzles to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(puzzles, f, indent=2)
    print(f"Saved {len(puzzles)} puzzles to {filename}")

if __name__ == "__main__":
    # Base URL without the puzzle number
    base_url = "https://pixelogic.app/every-5x5-nonogram"
    
    # Scrape puzzles
    print("Starting scraper...")
    puzzles = scrape_all_puzzles(base_url, max_puzzles=3)
    
    # Save results
    save_to_file(puzzles)
    
    # Print sample
    if puzzles:
        first_puzzle = next(iter(puzzles.values()))
        print("\nSample puzzle:")
        print(f"Row hints: {first_puzzle['row_hints']}")
        print(f"Column hints: {first_puzzle['col_hints']}")

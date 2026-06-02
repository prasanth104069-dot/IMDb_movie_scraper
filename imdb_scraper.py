"""
IMDb Movie Rating Scraper
Scrapes Top 250 movies from IMDb using Selenium and saves to CSV.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import pandas as pd
import time
import logging

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def get_driver():
    """Create and return a Chrome WebDriver instance."""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=en-US")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )
    return driver


def scrape_imdb_top250():
    """
    Scrape IMDb Top 250 movies.
    Returns a list of dicts with keys: rank, title, year, rating.
    """
    url = "https://www.imdb.com/chart/top/"
    movies = []

    driver = get_driver()
    try:
        logger.info("Opening IMDb homepage...")
        driver.get("https://www.imdb.com")
        time.sleep(4)

        logger.info("Navigating to Top 250...")
        driver.get(url)
        time.sleep(10)

        # Scroll down to trigger lazy loading
        for i in range(5):
            driver.execute_script("window.scrollBy(0, 800)")
            time.sleep(1)

        # Scroll back to top
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(3)

        # Wait for items to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
            )
        )

        items = driver.find_elements(
            By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item"
        )
        logger.info(f"Found {len(items)} movies")

        for idx, item in enumerate(items, start=1):
            try:
                # ── Title ──────────────────────────────────────────────────
                title_el = item.find_element(
                    By.CSS_SELECTOR, "h3.ipc-title__text"
                )
                raw_title = title_el.text.strip()
                title = raw_title.split(". ", 1)[-1] if ". " in raw_title else raw_title

                # ── Year ───────────────────────────────────────────────────
                try:
                    full_text = item.text
                    lines = full_text.split('\n')
                    year = "N/A"
                    for line in lines:
                        line = line.strip()
                        if len(line) >= 4 and line[:4].isdigit():
                            year = line[:4]
                            break
                except Exception:
                    year = "N/A"

                # ── Rating ─────────────────────────────────────────────────
                try:
                    rating_el = item.find_element(
                        By.CSS_SELECTOR, "span.ipc-rating-star--rating"
                    )
                    rating = rating_el.text.strip()
                except Exception:
                    rating = "N/A"

                movies.append({
                    "rank":   idx,
                    "title":  title,
                    "year":   year,
                    "rating": rating,
                })

                if idx % 50 == 0:
                    logger.info(f"Scraped {idx} / {len(items)}...")

            except Exception as e:
                logger.warning(f"Skipping row {idx}: {e}")

    finally:
        driver.quit()
        logger.info("Browser closed.")

    return movies


def save_to_csv(movies, filename="imdb_top250.csv"):
    """Save movie list to a CSV file."""
    df = pd.DataFrame(movies)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    logger.info(f"Saved {len(df)} movies to '{filename}'")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    movies = scrape_imdb_top250()

    if movies:
        save_to_csv(movies)
        df = pd.DataFrame(movies)
        print("\n--- Preview (first 10 movies) ---")
        print(df.head(10).to_string(index=False))
    else:
        print("No movies found!")
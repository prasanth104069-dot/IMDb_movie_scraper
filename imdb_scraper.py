from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
import pandas as pd
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)


def get_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
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
    url = "https://www.imdb.com/chart/top/"
    movies = []

    driver = get_driver()
    try:
        logger.info("Opening IMDb homepage...")
        driver.get("https://www.imdb.com")
        time.sleep(5)

        logger.info("Navigating to Top 250...")
        driver.get(url)
        time.sleep(12)

        # Scroll to load all movies
        for i in range(8):
            driver.execute_script("window.scrollBy(0, 800)")
            time.sleep(1)

        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(3)

        # Try multiple selectors for movie items
        items = driver.find_elements(
            By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item"
        )
        logger.info(f"Found {len(items)} movies")

        for idx, item in enumerate(items, start=1):
            try:
                # Title — try multiple selectors
                title = "N/A"
                for selector in [
                    "h3.ipc-title__text",
                    "h3",
                    ".ipc-title__text",
                    "a.ipc-title-link-wrapper"
                ]:
                    try:
                        el = item.find_element(By.CSS_SELECTOR, selector)
                        raw = el.text.strip()
                        if raw:
                            title = raw.split(". ", 1)[-1] if ". " in raw else raw
                            break
                    except Exception:
                        continue

                # Year — from text lines
                year = "N/A"
                try:
                    lines = item.text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if len(line) >= 4 and line[:4].isdigit():
                            year = line[:4]
                            break
                except Exception:
                    year = "N/A"

                # Rating — try multiple selectors
                rating = "N/A"
                for selector in [
                    "span.ipc-rating-star--rating",
                    "span[class*='rating']",
                    ".ipc-rating-star--rating"
                ]:
                    try:
                        el = item.find_element(By.CSS_SELECTOR, selector)
                        rating = el.text.strip()
                        if rating:
                            break
                    except Exception:
                        continue

                if title != "N/A":
                    movies.append({
                        "rank": idx,
                        "title": title,
                        "year": year,
                        "rating": rating
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
    df = pd.DataFrame(movies)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    logger.info(f"Saved {len(df)} movies to '{filename}'")


if __name__ == "__main__":
    movies = scrape_imdb_top250()
    if movies:
        save_to_csv(movies)
        df = pd.DataFrame(movies)
        print("\n--- Preview (first 10 movies) ---")
        print(df.head(10).to_string(index=False))
    else:
        print("No movies found!")
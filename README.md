# 🎬 IMDb Movie Rating Scraper

A Python-based automation tool that dynamically scrapes movie data from IMDb using Selenium and Chrome WebDriver. It retrieves movie details like title, release year, and IMDb rating from the **Top 250 Movies** list and saves them to a CSV file.

---

## 📌 Project Description

The **IMDb Movie Rating Scraper** automates browser actions to handle dynamic content loading on IMDb. The extracted data can be used for:
- Movie trend analysis
- Building recommendation engines
- Personal film databases
- Data science and ML projects

---

## ✨ Features

- ✅ **Dynamic Movie Scraping** — Uses Selenium to load IMDb Top 250 page and extract full content
- ✅ **Top Movie Rankings** — Scrapes movie name, year, and IMDb rating
- ✅ **Structured Output** — Saves extracted data to CSV for easy access and analysis
- ✅ **Bot Protection Bypass** — Uses selenium-stealth to avoid IMDb detection
- ✅ **Auto ChromeDriver** — Automatically downloads the correct ChromeDriver version
- ✅ **Expandable** — Easily extendable to scrape individual movie pages for cast, genre, etc.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python | Main scripting language |
| Selenium | Browser automation |
| selenium-stealth | Bypass bot detection |
| webdriver-manager | Auto-download ChromeDriver |
| pandas | Data manipulation and CSV export |
| Chrome WebDriver | Render JavaScript-loaded content |

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/prasanth104069-dot/IMDb_movie_scraper.git
cd IMDb_movie_scraper
```

### 2. Install Required Libraries
```bash
pip install selenium webdriver-manager selenium-stealth pandas
```

---

## ▶️ How to Run

```bash
python imbd_scraper.py
```

Chrome will open automatically, navigate to IMDb, scrape all 250 movies, and close. Results are saved to `imdb_top250.csv`.

---

## 📊 Output

The script generates a CSV file `imdb_top250.csv` with the following columns:

| rank | title | year | rating |
|------|-------|------|--------|
| 1 | The Shawshank Redemption | 1994 | 9.3 |
| 2 | The Godfather | 1972 | 9.2 |
| 3 | The Dark Knight | 2008 | 9.1 |
| 4 | The Godfather Part II | 1974 | 9.0 |
| 5 | 12 Angry Men | 1957 | 9.0 |

---

## 📁 Project Structure

```
IMDb_movie_scraper/
├── imbd_scraper.py       # Main scraper script
├── requirements.txt      # Required libraries
├── imdb_top250.csv       # Output CSV file (auto-generated)
└── README.md             # Project documentation
```

---

## ⚙️ How It Works

1. **Opens Chrome** automatically using Selenium
2. **Visits IMDb homepage** first to avoid bot detection
3. **Navigates to Top 250** movies page
4. **Scrolls the page** to trigger lazy loading of all movies
5. **Extracts** title, year, and rating for each movie
6. **Saves data** to `imdb_top250.csv` using pandas
7. **Closes browser** automatically

---

## 🐛 Troubleshooting

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install selenium webdriver-manager selenium-stealth pandas` |
| `0 movies found` | IMDb blocked request — script visits homepage first to fix this |
| `ChromeDriver error` | Update Chrome browser to latest version |
| `TimeoutException` | Slow internet — increase `time.sleep()` value |
| `Lock file error` | Run `del "%USERPROFILE%\.wdm\.wdm-lock-chromedriver-win64"` |

---

## 🚀 Future Enhancements

- [ ] Schedule daily scraping using Task Scheduler
- [ ] Scrape individual movie pages for cast and genre
- [ ] Add data visualization using matplotlib
- [ ] Build a movie recommendation engine
- [ ] Export to Excel with formatting

---

## 👨‍💻 Author

**Prasanth**
- GitHub: [@prasanth104069-dot](https://github.com/prasanth104069-dot)

---

## 📄 License

This project is for educational and internship purposes only.

---

⭐ If you found this project helpful, please give it a star!

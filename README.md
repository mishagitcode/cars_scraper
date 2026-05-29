# cars_scraper

---

**Table of Contents**
1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Database Description](#database-description)
4. [Spider Description](#spider-description)
5. [How to Run the Project](#how-to-run-the-project)
   - [Prerequisites](#1-prerequisites)
   - [Installation](#2-installation)
   - [Running the Spider](#3-running-the-spider)
   - [Exporting to JSON](#4-exporting-to-json)
6. [Technologies](#technologies)

---

## Project Overview

This project is a Scrapy web scraper that collects BMW approved used car listings from [usedcars.bmw.co.uk](https://usedcars.bmw.co.uk). It scrapes the first 5 pages of cash-payment results, visits each vehicle's detail page, and stores the collected data directly into a SQLite database.

The workflow includes:
1. Scraping listing pages (pages 1–5) to collect car title, model, and link
2. Following each link to the vehicle detail page to collect 8 specification fields
3. Saving all data directly to `bmw_cars.sqlite3` via a pipeline
4. Optionally exporting the database contents to JSON files

---

## Project Structure

```text
cars_scraper/
|-- cars_scraper/                        # Scrapy project package
|   |-- spiders/
|   |   `-- UsedCarsBmwUkSpider.py       # Main spider
|   |-- items.py                         # BmwAdvertItem and BmwSpecItem definitions
|   |-- pipelines.py                     # SQLitePipeline — saves items to SQLite
|   |-- middlewares.py                   # Scrapy middlewares (default)
|   `-- settings.py                      # Scrapy settings (Playwright, pipeline, etc.)
|-- bmw_cars.sqlite3                     # SQLite database (auto-created on first run)
|-- db_to_json.py                        # Export DB contents to adverts.json / specs.json
|-- scrapy.cfg                           # Scrapy deploy configuration
`-- requirements.txt                     # Project dependencies
```

---

## Database Description

The project uses SQLite (`bmw_cars.sqlite3`) with two tables linked by a foreign key:

- **adverts**
  - `id` — primary key
  - `title` — vehicle name, e.g. `"X1 sDrive18d M Sport"`
  - `model` — BMW model range, e.g. `"BMW X1"`
  - `link` — full URL to the vehicle detail page (unique)

- **specs**
  - `id` — primary key
  - `advert_id` — foreign key → `adverts.id` (ON DELETE CASCADE)
  - `spec_1` — Mileage, e.g. `"10,940"`
  - `spec_2` — Registration date, e.g. `"May 2025"`
  - `spec_3` — Engine capacity or electric range, e.g. `"1,995 cc"`
  - `spec_4` — Exterior colour, e.g. `"Black Sapphire metallic paint"`
  - `spec_5` — Fuel type, e.g. `"Diesel"`
  - `spec_6` — Transmission, e.g. `"Automatic"`
  - `spec_7` — Registration plate, e.g. `"WD25KXL"`
  - `spec_8` — Upholstery, e.g. `"M Alcantara Veganza combination Black"`

Relationships:
- One `advert` → one `specs` record

---

## Spider Description

**`UsedCarsBmwUkSpider`** uses Scrapy-Playwright to render JavaScript-heavy pages.

- Visits pages 1–5 of `https://usedcars.bmw.co.uk/result/?payment_type=cash&size=23&source=home`
- Waits for `.uvl-c-advert-overview__title a[href*='quoteref']` before parsing each listing page
- Extracts `title`, `model`, `link` → yields `BmwAdvertItem`
- Follows each link, waits for `.uvl-c-specification-overview__value`, extracts 8 spec values → yields `BmwSpecItem`
- `SQLitePipeline` receives both item types and writes them to the database

---

## How to Run the Project

### 1. Prerequisites

- Python 3.10+
- Git
- Virtual environment tool (`venv`)
- Node.js (required by Playwright)

### 2. Installation

2.1. Clone the repository:

```commandline
git clone https://github.com/mishagitcode/cars_scraper
```

```commandline
cd cars_scraper
```

2.2. Create a virtual environment:

```commandline
python -m venv venv
```

2.3. Activate the virtual environment:

Windows:
```commandline
venv\Scripts\activate
```

macOS/Linux:
```commandline
source venv/bin/activate
```

2.4. Install dependencies:

```commandline
pip install -r requirements.txt
```

2.5. Install Playwright browser:

```commandline
playwright install chromium
```

---

### 3. Running the Spider

```commandline
scrapy crawl UsedCarsBmwUkSpider
```

The spider will create `bmw_cars.sqlite3` automatically and populate both tables.

---

### 4. Exporting to JSON

To export the database contents to `adverts.json` and `specs.json`:

```commandline
python db_to_json.py
```

---

## Technologies

- **Python**: Core programming language
- **Scrapy**: Web scraping framework
- **Scrapy-Playwright**: JavaScript rendering via Playwright (Chromium)
- **SQLite**: Database for storing scraped data
- **Playwright**: Browser automation for JS-rendered pages

---

Developed by [mishagitcode](https://github.com/mishagitcode)

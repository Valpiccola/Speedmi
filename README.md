# Welcome to SpeedMe

## 🚀 Introducing 𝗦𝗽𝗲𝗲𝗱𝗠𝗲: A Powerful Open-Source Website Speed Analysis Tool

Ever wondered how your website could perform better in terms of speed and user experience? Look no further! We are excited to present 𝗦𝗽𝗲𝗲𝗱𝗠𝗲, a comprehensive website speed analyzer that extracts vital performance data from web pages and stores it in a PostgreSQL database for further analysis. 📊

## 🔥 Speedmi Features:

✅ Extracts URLs from a sitemap XML file
✅ Processes each URL using Google PageSpeed Insights API
✅ Collects various performance, accessibility, best practices, and SEO metrics
✅ Saves the metrics to a PostgreSQL database

## 🎓 Getting started:

1️⃣ Create a PostgreSQL database and table
2️⃣ Set up environment variables for your database credentials and Google PageSpeed API Key
3️⃣ Run the script by providing your sitemap URL

### 1: Create a PostgreSQL database and create a dedicated table:

```sql
CREATE TABLE site_speed_scores (
    id SERIAL PRIMARY KEY,
    url VARCHAR(2083) NOT NULL,
    timestamp TIMESTAMP,
    performance_score NUMERIC,
    accessibility_score NUMERIC,
    best_practices_score NUMERIC,
    seo_score NUMERIC,
    first_contentful_paint_score NUMERIC,
    first_meaningful_paint_score NUMERIC,
    largest_contentful_paint_score NUMERIC,
    speed_index_score NUMERIC,
    cumulative_layout_shift_score NUMERIC,
    server_response_time_score NUMERIC,
    is_crawlable_score NUMERIC,
    console_errors_score NUMERIC,
    total_byte_weight_score NUMERIC,
    dom_size_score NUMERIC
);
```

### 2: Set the environment variables for your database credentials and Google PageSpeed API Key.

```shell
export DB_USER=
export DB_PASS=
export DB_HOST=
export DB_PORT=
export DB_NAME=postgres
export GOOGLE_SPEED_API_KEY=
```

### 3: Call the script passing your sitemap URL

```shell
python speedme.py "https://example.com/sitemap.xml"
```

## Upcoming Features

✨ Visualize data with charts and graphs
✨ Schedule automatic scans and monitoring
✨ Integration with other performance analysis tools
✨ Detailed comparison between different scans and metrics

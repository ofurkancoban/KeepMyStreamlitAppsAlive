import streamlit as st
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import pyppeteer
import logging
import asyncio
import pytz

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to visit websites using pyppeteer
async def visit_websites():
    urls = [
        "https://keepmywebappsalive.streamlit.app/",
        "https://xml2csv.streamlit.app/",
        "https://semesterticket.streamlit.app/",
        "https://shifttracker.streamlit.app/",
        "https://pdfwithnotes.streamlit.app/",
        "https://pdfdarkmodeconverter.streamlit.app/"
    ]

    results = []
    try:
        logger.info("Launching browser...")
        browser = await pyppeteer.launch(headless=True, args=['--no-sandbox'])
        page = await browser.newPage()
        logger.info("Browser launched.")

        for url in urls:
            try:
                logger.info(f"Visiting {url}")
                await page.goto(url, {'waitUntil': 'load'})
                await asyncio.sleep(5)  # Wait for the page to load
                results.append((url, "Visited Successfully"))
            except Exception as e:
                results.append((url, f"Error: {e}"))
                logger.error(f"Error visiting {url}: {e}")

        await browser.close()
        logger.info("Browser closed.")
    except Exception as e:
        logger.error(f"Error during the browsing session: {e}")
        results.append(("Error", f"Error: {e}"))

    return results

# Function to start the scheduler
def start_scheduler(loop):
    scheduler = BackgroundScheduler(timezone=pytz.UTC)
    trigger = IntervalTrigger(hours=1, timezone=pytz.UTC)
    scheduler.add_job(lambda: asyncio.run_coroutine_threadsafe(visit_websites(), loop), trigger=trigger)
    scheduler.start()
    logger.info("Scheduler started")

# Streamlit app function
def main(loop):
    st.title("Automated Website Visitor")
    st.write("This app visits specified websites every 12 hours automatically.")

    if st.button("Run Now"):
        results = asyncio.run_coroutine_threadsafe(visit_websites(), loop).result()
        for url, status in results:
            st.write(f"Visited {url} - Status: {status}")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Start the scheduler in the main thread
    start_scheduler(loop)

    # Run the Streamlit app
    main(loop)

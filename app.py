import streamlit as st
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import time
from threading import Thread


# Function to visit websites
def visit_websites():
    urls = ["https://keepmywebappsalive.streamlit.app/",
        "https://xml2csv.streamlit.app/",
        "https://semesterticket.streamlit.app/",
        "https://shifttracker.streamlit.app/",
        "https://pdfwithnotes.streamlit.app/",
        "https://pdfdarkmodeconverter.streamlit.app/"

    ]

    results = []
    for url in urls:
        try:
            response = requests.get(url)
            results.append((url, response.status_code))
        except Exception as e:
            results.append((url, f"Error: {e}"))

    return results


# Function to run the scheduler
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(visit_websites_job, 'interval', hours=12)
    scheduler.start()
    print("Scheduler started")
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


# Wrapper for visit_websites to be used in scheduler
def visit_websites_job():
    results = visit_websites()
    for url, status in results:
        print(f"Visited {url} - Status Code: {status}")


# Streamlit app function
def main():
    st.title("Automated Website Visitor")
    st.write("This app visits specified websites every 24 hours automatically.")

    if st.button("Run Now"):
        results = visit_websites()
        for url, status in results:
            st.write(f"Visited {url} - Status Code: {status}")


if __name__ == "__main__":
    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=start_scheduler)
    scheduler_thread.start()

    # Run the Streamlit app
    main()

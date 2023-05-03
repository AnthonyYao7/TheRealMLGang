from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time
import threading

from typing import List


base_search_url = "https://www.youtube.com/results?search_query={}"

CHROME_PATH = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
CHROMEDRIVER_PATH = "C:\chromedriver\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.binary_location = CHROME_PATH

special_characters = "@#$%^&*_={}|[]\\:\";'<>?,/"


def get_video_link(artist_name: str, video_name: str) -> str:
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)

    search_query = artist_name + " " + video_name
    search_query = search_query.replace(" ", "+")

    search_query = "".join([ch for ch in search_query if ch not in special_characters])

    driver.get(base_search_url.format(search_query))

    try:
        first_video = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a/yt-formatted-string"))
        )
        driver.execute_script("arguments[0].click();", first_video)
        ret = driver.current_url
    except:
        return
    finally:
        driver.quit()

    return ret


def get_video_link_threaded(artist_name: str, video_name: str, track_id: str) -> None:
    link = get_video_link(artist_name, video_name)
    if link is None:
        return

    lock = threading.Lock()
    lock.acquire()

    with open("links.txt", "a") as f:
        f.write(",".join([track_id, '"' + artist_name.replace('"', '') + '"', '"' + video_name.replace('"', '') + '"', link]) + "\n")
    lock.release()


def do_subset(entry_list: List) -> None:
    for entry in entry_list:
        get_video_link_threaded(entry[0], entry[1], entry[2])


def main():
    df = pd.read_csv("../Alan/cleaned_data.csv")

    artists = list(df['artists'])
    track_name = list(df['track_name'])
    track_id = list(df['track_id'])

    a_tn = list(zip(artists, track_name, track_id))

    threads = []

    for i in range(20):
        thread = threading.Thread(target=do_subset, args=(a_tn[i * 500: (i + 1) * 500],))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()

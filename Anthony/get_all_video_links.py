from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse
import pandas as pd
import time

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
    finally:
        driver.quit()
    # first_link_xpath = '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a/yt-formatted-string'
    # first_video = driver.find_element('xpath', first_link_xpath)
    return ret



def main():
    df = pd.read_csv("dataset.csv")
    artist_trackname = df[['artists', 'track_name', 'popularity']].copy()

    artist_trackname.sort_values(by=['popularity'], inplace=True, ascending=False)
    artist_trackname.drop_duplicates(subset="track_name", keep="first", inplace=True)

    artists = list(artist_trackname['artists'])
    track_name = list(artist_trackname['track_name'])

    youtube_urls = []
    done = 453
    count = done
    for artist, track in zip(artists, track_name):
        if done > 0:
            done -= 1
            continue
        if count == 10000:
            break
        youtube_urls.append(get_video_link(artist, track))
        if youtube_urls[-1] is None:
            youtube_urls.pop(-1)
            continue
        print(youtube_urls[-1])
        with open("links.txt", "a") as f:
            f.write(youtube_urls[-1] + "\n")
        count += 1

    artist_trackname['yt_links'] = youtube_urls

    artist_trackname.to_csv("with_links.csv")


if __name__ == "__main__":
    main()

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys

ffox_profile_path = r'C:\Users\beuth\AppData\Roaming\Mozilla\Firefox\Profiles\l4aeu5vs.default-release'

profile = FirefoxProfile(ffox_profile_path)

# Use my personal firefox profile
profile.set_preference('browser.startup.homepage_override.mstone', 'ignore')
profile.set_preference('startup.homepage_welcome_url.additional', '')
profile.set_preference('datareporting.healthreport.uploadEnabled', False)
profile.set_preference('datareporting.policy.dataSubmissionEnabled', False)

firefox_options = webdriver.FirefoxOptions()
firefox_options.profile = profile

# Create the webdriver using the configured profile
driver = webdriver.Firefox(options=firefox_options)

singdata = {} # List to store name of artists
songdata = {} # List to store top 100 songs

years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
for year in years:
    # fo to the appropriate year on billboard.com
    link = f"https://www.billboard.com/charts/hot-100/{year}-12-02/"
    driver.get(link)

    # full class value of the page, contains all song names and singers
    total = driver.find_elements(By.CLASS_NAME, 'o-chart-results-list-row-container')

    songs, artists = [], []
     
    # fetching the top 100 songs
    for piece in total:
        song = piece.find_element(By.CSS_SELECTOR, 'li ul li h3').text
        artist = piece.find_element(By.CSS_SELECTOR, 'li ul li span').text
        songs.append(song)
        artists.append(artist)
        
    singdata[year] = artists
    songdata[year] = songs      
# total exists to keep track of how the mining is going 
total=0
# hot100list is where our data is stored and will be turned into a DF after
hot100list = []
print(songdata.keys())
print(songdata[2011])
driver.get("https://genius.com/Imagine-dragons-believer-lyrics")
for year in songdata.keys():
    songs = songdata[year]
    singers = singdata[year]
    i=0
    for song, singer in zip(songs, singers):
        # Search the Genius.com Searchbar in the top left of the page with our info to find the lyrics
        sgenre = None
        searchbar = driver.find_element(By.XPATH, '//*[@id="sticky-nav"]/div[2]/form/input')
        searchbar.send_keys(f"{singer} {song}")
        searchbar.submit()
        time.sleep(4)
        try:
            # Click the first link under the "Songs" category
            songaction = driver.find_element(By.XPATH, '/html/body/routable-page/ng-outlet/search-results-page/div/div[2]/div[1]/div[2]/search-result-section/div/div[2]/search-result-items/div[1]/search-result-item/div/mini-song-card/a')
            songaction.click()
        except:
            lyrics= None
        try:
            # Lyrics are split in two chunks, collect both
            lyrics_container_1 = driver.find_elements(By.XPATH, '//*[@id="lyrics-root"]/div[2]')
            lyrics_container_2 = driver.find_elements(By.XPATH, '//*[@id="lyrics-root"]/div[5]')
    
            # Extract text content from both containers
            lyrics_1 = ' '.join(line.strip() for line in lyrics_container_1[0].text.splitlines()) if lyrics_container_1 else ''
            lyrics_2 = ' '.join(line.strip() for line in lyrics_container_2[0].text.splitlines()) if lyrics_container_2 else ''
    
            # Concatenate both sets of lyrics
            lyrics = '\n'.join([lyrics_1, lyrics_2]).strip()
    
            # Remove unwanted tags like [Verse]
            j=0
            for j in range(1, 6):
                lyrics = lyrics.replace(f'[Verse {j}]', '').strip()
            lyrics = lyrics.replace('[Pre-Chorus]', '').strip()
            lyrics = lyrics.replace('[Chorus]', '').strip()
            lyrics = lyrics.replace('[Outro]', '').strip()
            lyrics = lyrics.replace('[Buildup]', '').strip()
            lyrics = lyrics.replace('[Guitar Solo]', '').strip()
            lyrics = lyrics.replace('[Refrain]', '').strip()
            lyrics = lyrics.replace('[Bridge]', '').strip()
    
            # Replace newlines with spaces
            lyrics = ' '.join(line + ' ' for line in lyrics.splitlines())
        except:
            lyrics = None
            #=====================Experimental Section Where Genre Finding Would Go==========================#
        # try:
        #     driver.get("https://www.google.com/search?q=calculator&rlz=1C1GCEA_enUS952US952&oq=calculator&gs_lcrp=EgZjaHJvbWUqDwgAEAAYQxixAxiABBiKBTIPCAAQABhDGLEDGIAEGIoFMg0IARAAGIMBGLEDGIAEMgoIAhAAGLEDGIAEMgoIAxAAGLEDGIAEMgoIBBAAGLEDGIAEMg0IBRAAGIMBGLEDGIAEMgoIBhAAGLEDGIAEMgoIBxAAGLEDGIAEMgoICBAAGLEDGIAEMgoICRAAGLEDGIAE0gEIMTM0OGowajeoAgCwAgA&sourceid=chrome&ie=UTF-8")
        #     time.sleep(1)
    
        #     # Clear the search bar to ensure it's empty
        #     googlesearch.clear()

        #     # Entering the search text
        #     googlesearch.send_keys(f"{singer} {songs[i]} lyrics")
    
        #     # Press Enter to submit the search
        #     googlesearch.send_keys(Keys.RETURN
        #     # To prevent captcha being initialized due to bot activity
        #     time.sleep(5)
        #     parent_element = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/music/recording_cluster:skos_genre"]')

        #     # Find the child element containing the genre text
        #     genre_element = parent_element.find_element(By.CSS_SELECTOR, 'span.LrzXr.kno-fv.wHYlTd.z8gr9e a.fl')

        #     # Get the text content of the genre
        #     sgenre = genre_element.text
                    
        # except:
        #     sgenre = None
        sgenre = None
        hot100list.append({'Year': year,'Song': song,'Singer': singer,'Lyrics': lyrics,'Genre': sgenre})
        print(hot100list[total])
        total = total + 1
        i = i+1
        # This page is used as the default since the loop needs to start on a genius lyrics page
        driver.get("https://genius.com/Imagine-dragons-believer-lyrics")

hot100DF = pd.DataFrame(hot100list)
driver.close()
hot100DF.to_csv('Hot100_2010-2023.csv')

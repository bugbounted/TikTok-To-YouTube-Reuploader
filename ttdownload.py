# open SnapTik website,
#      input link into form field
#      enter
#      click download HD video
#      wait for download finish

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options

from random import randint

from time import sleep
from os import listdir,mkdir

# google authentication

from googleapiclient.http import MediaFileUpload
from Google import Create_Service

from os import remove


CLIENT_SECRET_FILE='client_secret.json'
API_NAME='youtube'
API_VERSION='v3'
SCOPES=['https://www.googleapis.com/auth/youtube.upload']


VIDEO_PATH='videos/'

service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)


    
    
prefs = {
    'download.default_directory' : VIDEO_PATH
}


options = Options()

options.add_argument('--headless')
# options.add_argument('--no-sandbox') # # Bypass OS security model
options.add_argument('start-maximized')
options.add_argument('disable-infobars')

# options.add_extension('AdblockPlus.crx') #
DRIVER = webdriver.Chrome(options=options)
print('Fetching webpage...')

DRIVER.implicitly_wait(2)    

snaptik_url = 'https://snaptik.app/en'

# WebdriverWait(driver, 2.5).until(titleIs())

    
# returns title of video


# In backwards order, with highest function requiring the least dependamatoes


def remove_all_videos():
    # remove videos
    print(f'Cleaning up for next meal ({VIDEO_PATH})...')
        
    for video in listdir(VIDEO_PATH):
        remove(f'{VIDEO_PATH}/{video}')
    
    print(f'Scavengar has finished cleaning up \n')

    return print('Videos deleted.')

def return_tiktok_credit(link):
    credit = link.split('https://www.tiktok.com/')[1].split('/')[0]

    return credit

def generate_title(link):
    
    # to credit username & avoid copyright issues + others
    username = return_tiktok_credit(link)    
         
    # giant list file full of clickable SEO titles to use randomint() on to find randomized title 4 variety
    
    with open('comma_seperated_titles','r') as name_list:
    
        title = '{}'.format(name_list.read().split(',\n')[randint(0,10)])

        if '[NAME]' in title:
            title = title.replace('[NAME]', username[1:])
        if '[TRENDORCHALLENGE]' in title:
            title = title.replace('[TRENDORCHALLENGE]', input('Congrats, you have landed on a title that requires input. Enter the trend/ challenge for use in the title! '))
     
        # credits in description
        user_profile = f'https://www.tiktok.com/{username}'
                
        return title, user_profile

def upload_video(link, file_name, publishAt=0):
        
    # title creation
    video_title, credit_profile_link = generate_title(link)        
    
    description= """
        Link to her profile: 
        {}
        
        """.format(credit_profile_link)

    request_body = {
        "snippet": {
        "title": video_title,
        "description": description,
        "tags": [
        ]
        },
        "status": {
        "privacyStatus": "public",
        #  "publishAt": publishAt
        }
    }

    
    mediaFile=MediaFileUpload(f'{VIDEO_PATH}/{file_name}')


    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()
    return 

def download_from_snaptik(link):

    # defines a wait. Revalulate later
    wait = WebDriverWait(DRIVER, 10) 
    
    # goes to snaptik, enters url
    DRIVER.get(snaptik_url)
    load_link_button = DRIVER.find_element(By.NAME,'url')
    load_link_button.send_keys(link + Keys().RETURN)
            
    # examine download button for href. If not loaded, wait until found...
    while True:
        sleep(2.5)

        try:
            dl_button = DRIVER.find_element(By.XPATH, '/html/body/main/section[2]/div/div/article/div[2]/div/a[2]')
            dl_link = dl_button.get_property('href')
            
            DRIVER.get(dl_link)
            break
        except:
            print('Failed to find element, retrying...') 
    
    # dl_button = DRIVER.find_element(By.XPATH, '//a[@title=Download Server 02]')
    
    
    # wait for download to finish, reevaluate later...  
    sleep(10)
    
    print('Scavengar has downloaded the content, moving onto upload process...')

    for f in listdir(VIDEO_PATH):
        upload_video(links, f)
        
        print('Upload complete for video {}'.format(link))
        remove_all_videos()

    
    
    return

def reupload_tiktok_to_yt(link):
    # make sure there's no previous videos in path
    try:
        print('Attempting to clear directory...')
        remove_all_videos()
        print('Cleared directory.')
    except:
        print('Directory already cleared, moving on...')
    
    download_from_snaptik(link)


links = '''https://www.tiktok.com/t/ZTRDvB7Dr/?k=1
https://www.tiktok.com/t/ZTRDvrMEH/?k=1
https://www.tiktok.com/t/ZTRDvPmH3/?k=1
https://www.tiktok.com/t/ZTRDv23kp/?k=1
https://www.tiktok.com/t/ZTRDv5V3q/?k=1
https://www.tiktok.com/t/ZTRDvyc5o/?k=1
https://www.tiktok.com/t/ZTRDvHBeq/?k=1
https://www.tiktok.com/t/ZTRDvUpqB/?k=1
https://www.tiktok.com/t/ZTRDvAfpm/?k=1
https://www.tiktok.com/t/ZTRDvFRTq/?k=1
https://www.tiktok.com/t/ZTRDvYe9n/?k=1
https://www.tiktok.com/t/ZTRDvrBxw/?k=1
https://www.tiktok.com/t/ZTRDvk1SB/?k=1
https://www.tiktok.com/t/ZTRDvAC24/?k=1
https://www.tiktok.com/t/ZTRDvPnbC/?k=1
https://www.tiktok.com/t/ZTRDvPKaW/?k=1
https://www.tiktok.com/t/ZTRDv9FC7/?k=1
https://www.tiktok.com/t/ZTRDvUqbk/?k=1
https://www.tiktok.com/t/ZTRDvm9gb/?k=1'''.split('\n')



for link in links:
    reupload_tiktok_to_yt(link)

print('Last file process attempt complete, Scavengar API has stopped.')

DRIVER.quit()

# iterate through file path & upload videos. Delete dummy file directory after uploading is over & videos


# change default download path
# create remove_all_videos & upload_video_in_path functions
# load adblocker extensions w/ webdriver (chrome.Options()?)
# yt upload functionality
# running selenium on aws instance


# hip hop clips & hip hop channel
# chairs shorts w/ Amazon FBA
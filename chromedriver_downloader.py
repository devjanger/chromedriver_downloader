import requests
import winreg
import zipfile, os
import platform

platform = platform.architecture()[0]
if platform == '64bit':
    platform = 'win64'
else:
    platform = 'win32'

def get_chromedriver_download_url(current_version):
    
    response = requests.get('https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json')

    for version in response.json()['versions'][::-1]:
        try:
            if current_version in version['version']:
                chromedrivers = version['downloads']['chromedriver']
                for chromedriver in chromedrivers:
                    if chromedriver['platform'] == platform:
                        download_url = chromedriver['url']
                        print(f'Downloading chromedriver from "{download_url}"')
                        return download_url

        except Exception as e:
            print(e)
            continue



def get_current_chrome_version():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
    value = winreg.QueryValueEx(key, "version")
    
    return value[0]


def download_chromedriver():
    current_version = get_current_chrome_version().split('.')[0]
    download_url = get_chromedriver_download_url(current_version)


    response = requests.get(download_url)
    with open(f'chromedriver_{platform}.zip', 'wb') as f:
        f.write(response.content)
    

    with zipfile.ZipFile(f'chromedriver_{platform}.zip', 'r') as zip_ref:
        for zipName in zip_ref.namelist():
            if 'chromedriver.exe' in zipName:
                
                readed = zip_ref.open(zipName)
                with open('chromedriver.exe', 'wb') as f:
                    f.write(readed.read())
                readed.close()
                break
    zip_ref.close()

    os.remove(f'chromedriver_{platform}.zip')

    print('Done.')

if __name__ == '__main__':
    download_chromedriver()

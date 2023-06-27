import requests
from bs4 import BeautifulSoup
import time
import os
import warnings
from tqdm import tqdm
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains


warnings.filterwarnings('ignore')
options = Options()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
options.add_argument('user-agent=' + user_agent)
## for background
# options.add_argument("headless")
options.add_argument('--window-size=1920, 1080')
options.add_argument('--no-sandbox')
options.add_argument("--disable-dev-shm-usage")
# options.add_argument('--start-maximized')
# options.add_argument('--start-fullscreen')
options.add_argument('--disable-blink-features=AutomationControlled')

# Save log 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('codeforces.log')
logger.addHandler(file_handler)


class CodeForcesCrawler:
    def __init__(self, save_path):
        self.url = "https://www.codeforces.com/"
        self.mirror_url = "https://mirror.codeforces.com/"
        self.contest_url = self.url + "contest/"

        self.save_path = save_path
        
    def __wait_until_find(self, driver, xpath):
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        return element
            
    def __wait_and_click(self, driver, xpath):
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        button = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", button)

    def get_contest_list(self, driver):
        contest_list = []

        # page_url = self.mirror_url + 'api/contest.status?contestId=' + project + '&count=500' # just 10
        # print("API: " + page_url)

        # response = requests.get(page_url)
        # results = response.json()['result']
        # for result in tqdm(results):
        #     if result['programmingLanguage'] in ['Python 3', 'PyPy 3'] \
        #         and result['problem']['name'] == 'Merge Sort' \
        #         and result['verdict'] in ['OK', 'WRONG_ANSWER']:
        #         id_verdict_map[result['id']] = result['verdict']
        
        return contest_list
    
    def get_problem_list(self, contest):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        
        problem_url = self.contest_url + contest
        driver.get(problem_url)
        time.sleep(1)
        
        problem_list = {}
        problem_xpath = '//*[@id="pageContent"]/div[2]/div[6]/table/tbody'
        
        try:
            pb_list = self.__wait_until_find(driver, problem_xpath)
            children = pb_list.find_elements(By.XPATH, "./child::*")
            cnt = 0
            tmp_list = []
            for elem in children:
                if cnt == 0:
                    cnt += 1
                    continue
                
                tmp_list.append(elem.text.split('\n')[1])
            problem_list[contest] = tmp_list
        except:
            print("Problem Error")
        
        return problem_list
    
        
    def get_submission_url_list(self, driver, contest, language):
        submission_url_list = []
        
        
        
        return submission_url_list
        
    
    def get_submission_list(self, contest, submission_url_list):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        submission_list = {}
        
        # submission_url = self.contest_url + contest + "/submission" + 
        
        # driver.get()
        return submission_list
        # submission_dict = {}
        # failed_dict = {}

        # submission_url = self.url + 'contest/' + project + '/submission/'

        # for id, verdict in tqdm(id_verdict_map.items()):
        #     page_url = submission_url + str(id)
        #     print(page_url)
        #     page = requests.get(page_url)
        #     soup = BeautifulSoup(page.text, "html.parser")
        #     try:
        #         code = soup.find('pre', {'id': 'program-source-text'}).text
        #         submission_dict[id] = [verdict, code]
        #     except:
        #         failed_dict[id] = verdict
        #         # logger.info(page_url)
        
        # if failed_dict:
        #     rest_submission_dict = self.get_submissions(project, failed_dict)
        #     submission_dict.update(rest_submission_dict)
                
        # return submission_dict


    def save(self, dir_path, file_path, data):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        with open(file_path, 'w') as w:
            w.write(data.strip())

    # def save_data(self, contest, submission_dict):
        # for id, (verdict, code) in tqdm(submission_dict.items()):
        #     dir_path = os.path.join(self.save_path, contest, verdict)
        #     file_path = dir_path+'/'+str(id)+'&'+verdict+'&'+'.py'
        #     self.save(dir_path, file_path, code)

    def run_one(self, contest):
        print('Get contest problem list...')
        problem_list = self.get_problem_list(contest)
        print("problem_list: " + str(problem_list))
        # print('Get submissions...')
        # submission_dict = self.get_submissions(project, id_verdict_map)
        # print('Save data...')
        # self.save_data(project, submission_dict)

# def recrawl():
#     urls = open('codeforces.log').read()
#     url_list = urls.split('\n')

#     for page_url in url_list:
#         page_url = 'https://www.codeforces.com/contest/873/submission/167504780'
#         id = page_url.split('/')[-1]

#         page = requests.get(page_url)
#         soup = BeautifulSoup(page.text, "html.parser")
#         code = soup.find('pre', {'id': 'program-source-text'}).text


if __name__ == '__main__':
    language = 'PYTH 3'
    
    save_path = 'codeforceData/'
    
    # Run CodeForcesCrawler with save_path
    cfc = CodeForcesCrawler(save_path)
    
    cfc.run_one('1842')

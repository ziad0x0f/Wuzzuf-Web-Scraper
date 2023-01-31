from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
from selenium.webdriver.common.by import By 

def scraper(search_for , pages, keywords):
	
	job_title = []
	company = []
	location = []
	skills = []
	experience = []
	job_type = []
	salaries = []
	links = []
	open_positions = []

	#create a chrome driver
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options=options)

	
	#start iterating through the pages starting from homepage
	for _ in range(pages):
		#open url with driver
		url = f"https://wuzzuf.net/search/jobs/?q={str(search_for)}&start={str(_)}"
		driver.get(url)

		try:
			job_roles = (list(map(get_text, driver.find_elements(By.XPATH, "//h2[@class='css-m604qf']/a"))))
		except NoSuchElementException:
			print("no jobs found")

		i = 1
		links.clear()

		# search job roles that relate to the given keywords
		for pos in list(map(lambda x: x.lower(), job_roles)):
			if any(key in pos for key in list(map(lambda x: x.lower(), keywords))) :	
				job_title.append(driver.find_element(By.XPATH, f"//div[@class='css-1gatmva e1v1l3u10'][{i}]/div[@class='css-pkv5jc']/div[@class='css-laomuu']/h2[@class='css-m604qf']/a[@class='css-o171kl']").text)
				job_type.append(driver.find_element(By.XPATH,f"//div[@class='css-1gatmva e1v1l3u10'][{i}]/div[@class='css-pkv5jc']/div[@class='css-y4udm8']/div[@class='css-1lh32fc']/a[1]/span").text)				
				company.append(driver.find_element(By.XPATH,f"//div[@class='css-1gatmva e1v1l3u10'][{i}]/div/div[@class='css-laomuu']/div/a").text)
				location.append(driver.find_element(By.XPATH,f"//div[@class='css-1gatmva e1v1l3u10'][{i}]/div/div[@class='css-laomuu']/div/span").text)
				
				try:
					experience.append(driver.find_element(By.XPATH,f"//div[@class='css-1gatmva e1v1l3u10'][{i}]/div[@class='css-pkv5jc']/div[@class='css-y4udm8']/div[2]/span[1]").text)
				except:
					experience.append("· 0 Yrs of Exp")

				links.append(driver.find_element(By.XPATH, f"//div[@class='css-1gatmva e1v1l3u10'][{i}]/div[@class='css-pkv5jc']/div[@class='css-laomuu']/h2[@class='css-m604qf']/a[@class='css-o171kl']").get_attribute("href"))
		
			i+=1	
	
		#extract job details(salary, open positions, skills)
		for _ in range(len(links)):
			driver.get(links[_])
			time.sleep(2)
			salaries.append(driver.find_element(By.XPATH, "//div[4]/span[@class='css-47jx3m']/span").text)
			open_positions.append(get_number(driver.find_element(By.XPATH, "//div[@class='css-bjn8wh']/div[@class='css-104dl8g']/div[@class='css-1wb134k']/span[@class='css-ixb653']/span").text))
			
			# append list of skills per job
			content = [driver.find_element(By.XPATH,f"//a[@class='css-g65o95'][{i+1}]/span[@class='css-6to1q']/span[@class='css-tt12j1 e12tgh591']/span[@class='css-158icaa']").text for i in range(len(driver.find_elements(By.XPATH,"//div[@class='css-s2o0yh']/a")))]
			skills.append(content)
	
	#return  pandas data frame
	data = {
	"job title":job_title, 
	"company": company,
	"location": location,
	"experience": experience,
	"salaries":salaries,
	"skills":skills,
	"job type": job_type,
	"open postions":open_positions
	}
	df = pd.DataFrame(data)

	return df
	
# get text property from list elements
def get_text(elem):
	return elem.text

def get_number(txt):
	for s in txt.split():
		if s.isdigit():
			return int(s)


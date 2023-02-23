from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import re
from selenium.webdriver.common.by import By
from difflib import SequenceMatcher


def scraper(search_for, pages, keywords):

	job_title = []
	job_id = []
	company = []
	location = []
	skills = []
	experience = []
	job_type = []
	salaries = []
	links = []
	open_positions = []

	# create a chrome driver
	driver = webdriver.Edge()

	# start iterating through the pages starting from homepage
	for pg_no in range(pages):

		# open url with driver
		url = f"https://wuzzuf.net/search/jobs/?q={str(search_for)}&start={str(pg_no)}"
		driver.get(url)

		try:
			job_roles = (list(map(get_text, driver
                        .find_elements(By.XPATH, "//h2[@class='css-m604qf']/a"))))
		except NoSuchElementException:
			print("no jobs found")

		
		links.clear()

		# search job roles that relate to the given keywords
		for i, job in enumerate(list(map(lambda x: x.lower(), job_roles))):
			if any(is_string_similar(job, key, 0.6) for key in list(map(lambda x: x.lower(), keywords))):

				job_title.append(driver
								.find_element(By.XPATH, f"//div[@class='css-1gatmva e1v1l3u10'][{i+1}]/div[@class='css-pkv5jc']/div[@class='css-laomuu']/h2[@class='css-m604qf']/a[@class='css-o171kl']")
								.text)
				job_type.append(driver
								.find_element(By.XPATH, f"//div[@class='css-1gatmva e1v1l3u10'][{i+1}]/div[@class='css-pkv5jc']/div[@class='css-y4udm8']/div[@class='css-1lh32fc']/a[1]/span").text)
				company.append(driver
								.find_element(By.XPATH, f"//div[@class='css-1gatmva e1v1l3u10'][{i+1}]/div/div[@class='css-laomuu']/div/a").text)
				location.append(driver
								.find_element(By.XPATH, f"//div[@class='css-1gatmva e1v1l3u10'][{i+1}]/div/div[@class='css-laomuu']/div/span")
								.text)

				try:
					experience.append(driver.find_element(
					By.XPATH, f"//div[@class='css-1gatmva e1v1l3u10'][{i+1}]/div[@class='css-pkv5jc']/div[@class='css-y4udm8']/div[2]/span[1]").text)
				except:
					experience.append("· 0 Yrs of Exp")

				links.append(driver.find_element(
					By.XPATH, f"//div[@class='css-1gatmva e1v1l3u10'][{i+1}]/div[@class='css-pkv5jc']/div[@class='css-laomuu']/h2[@class='css-m604qf']/a[@class='css-o171kl']").get_attribute("href"))

				

		# extract job details(job_id, salary, open positions, skills)
		for id, link in enumerate(links):

			driver.get(link)
			time.sleep(2)

			job_id.append(str(pg_no+1) + str(id))
			salaries.append(driver.find_element(
				By.XPATH, "//div[4]/span[@class='css-47jx3m']/span").text)
			open_positions.append(int(re.findall("\d+", driver.find_element(By.XPATH,
			                      "//div[@class='css-bjn8wh']/div[@class='css-104dl8g']/div[@class='css-1wb134k']/span").text)[0]))

			# append list of skills per job
			content = [driver.find_element(By.XPATH, f"//a[@class='css-g65o95'][{i+1}]/span[@class='css-6to1q']/span[@class='css-tt12j1 e12tgh591']/span[@class='css-158icaa']").text 
			for i in range(len(driver.find_elements(By.XPATH, "//div[@class='css-s2o0yh']/a")))]
			skills.append(content)

	# return  pandas data frame
	data = {
            "job_id": job_id,
            "job_title": job_title,
            "company": company,
            "location": location,
            "experience": experience,
            "salaries": salaries,
            "skills": skills,
            "job_type": job_type,
            "open_postions": open_positions
			}

	return pd.DataFrame(data).explode("skills", ignore_index=True).rename(columns={"skills": "skill"})

# get text property from list elements
def get_text(elem):
	return elem.text

# check if two strings are similar within a certain degree of similarity
def is_string_similar(s1: str, s2: str, threshold: float = 0.8):
   return SequenceMatcher(a=s1.lower(), b=s2.lower()).ratio() >= threshold


# # uncomment this block if you want to run the script directly
# if __name__ == "__main__":

# 	search_for = "data"
# 	pages = 10
# 	keywords = ["data analyst", "data engineer"]
# 	df = scraper(search_for, pages, keywords)
# 	print(df)

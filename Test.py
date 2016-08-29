__author__ = 'Ashish Kumar'
#import all the inbuilt modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import unittest, time, os

targetBrowser = "Chrome"


class MoatSearchTest(unittest.TestCase):


    def setUp(self):
        if targetBrowser == "Chrome":
            self.driver = webdriver.Chrome()
        elif targetBrowser == "Firefox":
            self.driver = webdriver.Firefox()
        print "Target Browser is ", targetBrowser
        #add implicit wait of 30 seconds
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.moat.com/"


    def tearDown(self):
        self.driver.quit()

    def test_001_verifyTryTheseRandomness(self, iteration=5):
        '''********************************************************************************************
            Objective:	Verify that the "Try These" links are random and that they work.
            No of loops:  5
        ********************************************************************************************'''
        try:
            print('test_001: Verify that the "Try These" links are random and that they work.')
            driver = self.driver
            #Open "http://www.moat.com/"
            driver.get(self.base_url)
            oldLinksName = []
            newLinksName = []
            #provision of iteration to repeat the test multiple times
            for i in range(iteration):
                print "Iteration "+str(i+1)+" started:"
                #iterate to find the 3 "Try These" links' and verify each link by launching them and comparing the link name in new page
                for x in range(3):
                    tryTheseElement = driver.find_element_by_xpath('//*[@id="search-bar"]/div/div[1]/span/a['+str(x+1)+']')
                    if tryTheseElement is not None:
                        oldLinksName.append(tryTheseElement.get_attribute('text'))
                        tryTheseElement.click()
                    else:
                        raise Exception("Couldn't find element for \"try these\" link 1")

                    if driver.find_element_by_id("data_header").text == oldLinksName[x]:
                        print "try link "+str(x+1)+" works"
                    else:
                        driver.find_element_by_id("data_header").text
                        raise Exception("try link "+str(x+1)+" is broken")

                    #go back to previous page
                    driver.back()
                print "the first page Try these links are: ",oldLinksName
                #refresh the page to get new set of "try these" links
                driver.refresh()
                #iterate to find the 3 new "Try These" links and verify each link by launching them and comparing the link name in new page
                for x in range(3):
                    tryTheseElement=driver.find_element_by_xpath('//*[@id="search-bar"]/div/div[1]/span/a['+str(x+1)+']')
                    if tryTheseElement is not None:
                        newLinksName.append(tryTheseElement.get_attribute('text'))
                        print newLinksName
                        tryTheseElement.click()
                    else:
                        raise Exception("Couldn't find element for \"try these\" link 1")

                    if driver.find_element_by_id("data_header").text == newLinksName[x]:
                        print "try new link "+str(x+1)+" works"
                    else:
                        driver.find_element_by_id("data_header").text
                        raise Exception("try new link "+str(x+1)+" is broken")
                    #go back to previous page
                    driver.back()
                print "the refreshed page Try these links are: ",newLinksName
                #compare the names of 3 "try these" links from new and old page to verify they are random
                if [True for x in oldLinksName for y in newLinksName if x == y]:
                    raise Exception("links are not random")
                oldLinksName = newLinksName[:]
                newLinksName = []
                print "Iteration "+str(i+1)+" passed"
            print "Pass"

        except Exception, e:
            driver.get_screenshot_as_file(os.getcwd()+'/Failure_test_001_verifyTryTheseRandomness.png')
            print "Fail"
            print e


    def test_002_verifyRecentlySeenAdslessThan30min(self,iteration=5):
        '''********************************************************************************************
            Objective:	Verify that the "Recently Seen Ads" are no more than half an hour old.
            No of loops:  5
        ********************************************************************************************'''
        try:
            print('test_002: Verify that the "Recently Seen Ads" are no more than half an hour old.')
            driver = self.driver
            #Open "http://www.moat.com/"
            driver.get(self.base_url)
            #provision of iteration to repeat the test multiple times
            for i in range(iteration):
                print "Iteration "+str(i+1)+" started:"
                #iterate over Recently seen adds and verify if mentioned times are less than or equal to 30 mins
                for j in driver.find_elements_by_class_name("featured-agencies"):
                    if 'min' in j.text:
                        #only strings with min/mins are used for comparision, as other values are in seconds which is
                        # already less than 30 mins
                        if int(j.text.strip().split('min')[0]) > 30:

                            raise Exception(j.text+" is an ad more than 30 mins old")
                    print j.text
                #refresh the page for next iteration
                driver.refresh()
                print "Iteration "+str(i+1)+" passed"
            print "Pass"

        except Exception, e:
            driver.get_screenshot_as_file(os.getcwd()+'/Failure_test_002_verifyRecentlySeenAdslessThan30min.png')
            print "Fail"
            print e


    def test_003_verifyAdCount(self, iteration=5):
        '''********************************************************************************************
            Objective: Verify the ad count on the search result page is correct, even if there are
                        multiple pages in the results set.
            No of loops:  5
        ********************************************************************************************'''
        try:
            print('test_003: Verify the ad count on the search result page is correct, even if there are multiple pages in the results set.')
            driver = self.driver
            for i in range(iteration):
                print "Iteration "+str(i+1)+" started:"
                #Open "http://www.moat.com/"
                driver.get(self.base_url)
                #Click on the first "Try these" link
                driver.find_element_by_xpath('//*[@id="search-bar"]/div/div[1]/span/a[1]').click()
                time.sleep(5)
                #store the reported count by Moat Search for that particular search item
                reportedCount = int(driver.find_element_by_class_name("creative-count").text.strip().split('creatives')[0].replace(",",""))
                print "reported count by website :", reportedCount
                #keep on clicking "Load More" till it can be found
                while True:
                    try:
                        print "Clicking on Load More...."
                        driver.find_element_by_id("paginate-button").click()
                        time.sleep(5)
                        #Scroll to end of page to debug failure if any inorder to be captured in screenshot
                        endText = driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/h2')
                        driver.execute_script("return arguments[0].scrollIntoView();", endText)
                        #explicit wait till the "Load More" is visible
                        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, 'paginate-button')))
                    except Exception, e:
                        #if Load More is not seen it will raise exception , indicating there are no more pages to load
                        break
                #count the ad banners in the page
                adCount = len(driver.find_elements_by_class_name("img-holder"))
                #subtract one from ad count if there is any ad that was highlighted while calculating
                if driver.find_elements_by_css_selector(".td-info.seen"):
                    adCount = adCount - 1
                print "count of ad images in the page: ",adCount
                #comapre the reported ad count by website and actual ad banners
                if not (reportedCount == adCount):
                    raise Exception("The count didn't match")
                print "Iteration "+str(i+1)+" passed"

            print "Pass"

        except Exception, e:
            driver.get_screenshot_as_file(os.getcwd()+'/Failure_test_003_verifyAdCount.png')
            print "Fail"
            print e


    def test_004_verifyShareAdFeature(self, iteration=5):
        '''********************************************************************************************
            Objective: Verify the "Share this Ad" feature
            No of loops:  5
        ********************************************************************************************'''
        try:
            print('test_004: Verify the "Share this Ad" feature')
            driver = self.driver
            #provision of iteration to repeat the test multiple times
            for i in range(iteration):
                print "Iteration "+str(i+1)+"started:"
                #Open "http://www.moat.com/"
                driver.get(self.base_url)
                #Click on first "Try these" link
                driver.find_element_by_xpath('//*[@id="search-bar"]/div/div[1]/span/a[1]').click()
                time.sleep(5)
                #Click on one 1st occurence of the ad banners from result page
                driver.find_element_by_class_name("img-holder").click()
                time.sleep(1)
                #store the active date for the ad
                oldDatesActive = driver.find_element_by_css_selector(".td-info.seen").text
                print "Dates Active for the selected advertisement before sharing: ",oldDatesActive
                #Click on the Creative button to expose the shareable link for the ad
                driver.find_element_by_xpath('//*[@id="popup-template"]/div/div[1]/div[2]/table/tbody/tr[5]/td[2]/div/a').click()
                #Read the value of the input box
                sharedLink= driver.find_element_by_xpath('//*[@id="popup-template"]/div/div[1]/div[2]/table/tbody/tr[5]/td[2]/div/div/input').get_attribute('value')
                #open the shared link
                driver.get("http://"+sharedLink)
                time.sleep(5)
                #store the active date of the higlighted banner
                newDatesActive = driver.find_element_by_css_selector(".td-info.seen").text
                print "Dates Active for the selected advertisement after sharing: ", newDatesActive
                #compare the active date of both banner to verify the shared ad and result ad are same
                if not oldDatesActive == newDatesActive:
                    raise Exception("Shared Ad is different from selected ad")
                print "Iteration "+str(i+1)+" passed"
            print "Pass"

        except Exception, e:
            driver.get_screenshot_as_file(os.getcwd()+'/Failure_test_004_verifyShareAdFeature.png')
            print "Fail"
            print "Reason for failure:",e


if __name__ == "__main__":
    unittest.main()
from RPA.Browser.Selenium import Selenium
from main.excel_reader import Excel
# from selenium.webdriver.common.keys import Key
from selenium.webdriver.common.by import By
# from selenium.common.exceptions import NoSuchElementException,TimeoutException
from main.constants import *

sel = Selenium(auto_close=False)

class BrowserOpen:
    def __init__(self) -> None:
        pass
    @staticmethod
    def open_browser():
        sel.open_available_browser(url)
        sel.maximize_browser_window()
    

    @staticmethod
    def search_bar():
        excel_data = Excel.read_excel()
        for row in excel_data:
            sel.input_text(search_path,row['Movie'])
            # sel.press_keys(Keys.ENTER)
            sel.press_keys(None,'\ue007' )  #\ue007
            sel.click_element(movie_path)
            # sel.click_element(exact_results)
            try:
                sel.click_element(exact_results)
            except Exception as e:
                print(f"Exception: {e}")
                # print(f"No locator found for exact results for movie: {row['Movie']}")
                # TV Movie locator instead
                sel.click_element(tv_movie_path)
                # sel.wait_until_element_is_enabled(exact_results)
                sel.click_element(exact_results)

            li_count = sel.get_element_count(movie_list)
            # print(f"Number of li elements inside the unordered list: {li_count}")

            latest_release_date = None
            latest_movie_element = None
            
            for i in range(1, li_count + 1):
                date_xpath = f'//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[{i}]/div[2]/div/ul[1]'
                date_element = sel.find_element(date_xpath)
                release_date = date_element.text.strip()  # Extract the release date text
                # Parse the release date and compare it with the latest release date found so far
                if release_date:
                    if latest_release_date is None or release_date > latest_release_date:
                        latest_release_date = release_date
                        latest_movie_element = date_element
                
            if latest_movie_element:
                latest_movie_element.click()
                # print(f"Clicked on the movie with the latest release date: {latest_release_date}")
                print("For", row['Movie'])
                print("Release data, latest_release_date")

            #for rating
                rating_xpath = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[1]/span[1]'
                try:
                    rating_element = sel.find_element(rating_xpath)
                    rating = sel.get_text(rating_element)
                except:
                    rating = 'N/A'
                print("IMDb rating for is", rating)

                #for popularity
                # popularity_xpath= '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/div[1]/div/div[3]/a/span/div/div[2]/div[1]'
                popularity_xpath = '//div[@data-testid="hero-rating-bar__popularity__score"]'
                try:
                    popular_element = sel.find_element(popularity_xpath)
                    popularity = sel.get_text(popular_element)
                except:
                    popularity = 'N/A'
                print("The popularity score is", popularity)


                #storyline
                # if Index is not None:
                #     try:
                #         storyline_xpath= sel.scroll_element_into_view(f'//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[{Index}]/div[2]/div/div/div/div')
                #         sel.wait_until_element_is_visible(storyline_xpath, timeout=10)
                #         text = sel.get_text(storyline_xpath)
                #         print("Text from the specified XPath:", text)
                #     except:
                #         print("Not found.")
                






                # # Find storyline sections and wait for them to load
                # for section_index in range(1, 8):  # Assuming there are 7 sections
                #     section_xpath = f'//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[{section_index}]'
                #     try:
                #         storyline_span_xpath = '//span[normalize-space()="Storyline"]'
                #         storyline_element = sel.find_element(storyline_span_xpath)
                #         sel.scroll_element_into_view(storyline_element)
                #         sel.wait_until_element_is_visible(storyline_element)
                #         print("Storyline section is loaded.")
                #     except NoSuchElementException:
                #         print("Storyline section not found.")
                #     except TimeoutException:
                #         print("Timeout occurred while waiting for storyline section to load.")
                
                
            #     review_xpath = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div/div[2]/ul/li[2]/a'
            #     expander_xpath = '//*[@class="expander-icon-wrapper spoiler-warning__control"]'
            #     review_container_xpath = '//*[@class="review-container"]'
            #     try:
            #         review_element = sel.find_element(review_xpath)
            #         sel.click_element(review_element)
            #         expander_elements = sel.find_elements(expander_xpath)
            #         for expander_element in expander_elements:
            #             sel.click_element(expander_element)
            #             review_container_elements = sel.find_elements(review_container_xpath)
            #             num_containers = len(review_container_elements)
            #             print(f"Number of review containers found: {num_containers}")
            #             num_to_print = min(5, num_containers)
            #             for i in range(num_to_print):
            #                 container_text = sel.get_text(review_container_elements[i])
            #                 print(f"Review Container {i + 1} Text: {container_text}")
            #     except NoSuchElementException:
            #         print("No reviews found.")
                
          




                




                #reviews
                review_xpath = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div/div[2]/ul/li[2]/a'
                expander_xpath = '//*[@class="expander-icon-wrapper spoiler-warning__control"]'
                review_container_xpath = '//*[@class="review-container"]'

                try:
                    review_element = sel.find_element(review_xpath)
                    review = sel.click_element(review_element)
                    expander_elements = sel.find_elements(expander_xpath)
                    for expander_element in expander_elements:
                        sel.click_element(expander_element)
                        review_container_elements = sel.find_elements(review_container_xpath)
                        num_containers = len(review_container_elements)
                        print(f"Number of review containers found: {num_containers}")
                        num_to_print = min(5, num_containers)
                        for i in range(num_to_print):
                            container_text = sel.get_text(review_container_elements[i])
                            print(f"Review Container {i + 1} Text: {container_text}")
                except:
                    review = 'N/A'
            else:
                print("No movies found.")
                


                # try:
                #     storyline_element = sel.find_element('//*[@class="sc-f5ef05d0-0 gutvDK"]')
                #     # storyline_element = sel.find_element("//div[@class='ipc-html-content ipc-html-content--base sc-3a5dddb9-1 dWpySj']")
                #     sel.scroll_element_into_view(storyline_element)
                #     sel.wait_until_element_is_visible(storyline_element)
                #     print("Storyline section is loaded.")
                # except NoSuchElementException:
                #     print("Storyline section not found.")
                # except TimeoutException:
                #     print("Timeout occurred while waiting for storyline section to load.")



                # #for genre
                # # XPath of the element to list its content
                # genre_xpath = '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[4]/div[2]/ul[2]/li[2]/div'
                # try:
                #     genre_element = sel.find_element(genre_xpath)
                #     genre_content = sel.get_text(genre_element)
                #     genre_lines = genre_content.split('\n')
                #     for line in genre_lines:
                #         print(line.strip())  # Strip any leading/trailing whitespaces
                # except Exception as e:
                #     print("Error:", e)


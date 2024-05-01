from RPA.Browser.Selenium import Selenium
from main.excel_reader import Excel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from main.constants import *
from main.connect_database import Database

sel = Selenium(auto_close=False)
db=Database()
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
        db.create_table()
                           
        for row in excel_data:
            ratings_list = []
            review_titles = []
            review_descriptions = []
            review_data = None
            review_data_1 = None
            review_data_2 = None
            review_data_3 = None
            review_data_4 = None
            review_data_5 = None
            Movie_name = None
            genres_string = None
            data_found= True
            


            sel.input_text(search_path,row['Movie'])
            sel.press_keys(None,'\ue007' )  #\ue007
            # sel.click_element("//button[@id='suggestion-search-button']")
            sel.click_element(movie_path)
            Movie_name = row['Movie']
            try:
                sel.click_element(exact_results)
                data_found = True

            except Exception as e:
                print(f"Exception: {e}")
                # print(f"No locator found for exact results for movie: {row['Movie']}")
                # TV Movie locator instead
                try:
                    sel.click_element(tv_movie_path)
                    sel.click_element(exact_results)
                    data_found = True

                except:
                    data_found = False
                    print("Not found movie", Movie_name)
                

            
            li_count = sel.get_element_count(movie_list)
            latest_release_date = None
            latest_movie_element = None
            
            for i in range(1, li_count + 1):
                date_xpath = f'//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[{i}]/div[2]/div/ul[1]'
                date_element = sel.find_element(date_xpath)
                release_date = date_element.text.strip()  # Extract the release date text
                if release_date:
                    if latest_release_date is None or release_date > latest_release_date:
                        latest_release_date = release_date
                        latest_movie_element = date_element
                    
            if latest_movie_element:
                latest_movie_element.click()
                # print(f"Clicked on the movie with the latest release date: {latest_release_date}")
                print(Movie_name)
                print(f"Release data :{latest_release_date}")
                date = latest_release_date
                print(date)
                sel.scroll_element_into_view("//span[normalize-space()='Storyline']")
                sel.wait_until_page_contains_element("//a[normalize-space()='Plot summary']",timeout=100)

                #for rating
                rating_xpath = '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[1]/span[1]'
                try:
                    rating_element = sel.find_element(rating_xpath)
                    rating = sel.get_text(rating_element)
                except:
                    rating = 'N/A'
                print("IMDb rating for is", rating)

                #for popularity
                popularity_xpath = '//div[@data-testid="hero-rating-bar__popularity__score"]'
                try:
                    popular_element = sel.find_element(popularity_xpath)
                    popularity = sel.get_text(popular_element)
                except:
                    popularity = 'N/A'
                print("The popularity score is", popularity)

                
                # storyline=None
                storyline_xpath = "//div[@data-testid='storyline-plot-summary']"
                try:
                    storyline= sel.get_text(storyline_xpath)
                except:
                    storyline='N/A'
                print("Storyline:",storyline)
                    
                #genre
                genre_xpath = "//li[@data-testid='storyline-genres']//ul[@role='presentation']//li"
                sel.scroll_element_into_view(genre_xpath)
                sel.wait_until_element_is_visible(genre_xpath)
                genre_elements = sel.find_elements(genre_xpath)
                genres = [sel.get_text(genre_element).strip() for genre_element in genre_elements]
                genres_string = ", ".join(genres)
                print("Genres:", genres_string)


                #review
                review_xpath = "//a[normalize-space()='User reviews']"
                try:
                    sel.scroll_element_into_view(review_xpath)
                    sel.click_element(review_xpath)
                        
                    dropdown_xpath = "//select[@name='sort']"
                    sel.scroll_element_into_view(dropdown_xpath)
                    sel.wait_until_element_is_visible(dropdown_xpath)
                    dropdown_element = sel.find_element(dropdown_xpath)
                    dropdown = Select(dropdown_element)
                    options = dropdown.options
                    last_option = options[-1].text
                    dropdown.select_by_visible_text(last_option)

                    sel.wait_until_element_is_visible('//a[@class="title"]')

                    title_elements = sel.find_elements('//a[@class="title"]')[:5]
                    review_titles = []
                    for i, element in enumerate(title_elements, start=1):
                        text_content = sel.get_text(element)
                        review_titles.append(f"Title {i}: {text_content}")

                    rating_elements = sel.find_elements('//span[@class="rating-other-user-rating"]')[:5]
                    ratings_list = []
                    for i, rating_element in enumerate(rating_elements, start=1):
                        rating_review = sel.get_text(rating_element)
                        ratings_list.append(f"Rating {i}: {rating_review}")

                    #expand all
                    expander_xpath = '//*[@class="expander-icon-wrapper spoiler-warning__control"]'
                    try:
                        expander_elements = sel.find_elements(expander_xpath)
                        for expander_element in expander_elements:
                            sel.click_element(expander_element)
                    except: 
                        pass

                    review_container_xpath = "//div[@class='text show-more__control']"
                    review_descriptions = []
                    try:
                        review_container_elements = sel.find_elements(review_container_xpath)
                        num_containers = len(review_container_elements)
                        print(f"Number of review containers found: {num_containers}")
                        num_to_print = min(5, num_containers)
                        for i in range(num_to_print):
                            description_text = sel.get_text(review_container_elements[i])
                            review_descriptions.append(f"Review Description {i + 1}: {description_text}")
                    except:
                        review_descriptions = ["N/A"] * 5
                        print("No review containers found.")

                    # Print reviews as strings
                    if len(review_titles) == 0:  # If no reviews found, insert placeholders
                        review_titles = ["N/A"] * 5
                        ratings_list = ["N/A"] * 5
                        review_descriptions = ["N/A"] * 5

                    for i in range(5):
                        if i < len(review_titles):
                            review_data = f"Review {i+1}: {review_titles[i]} | {ratings_list[i]} | {review_descriptions[i]}"
                        else:
                            review_data = f"Review {i+1}: N/A | N/A | N/A"
                        print(review_data)

                    review_data_1 = f"{review_titles[0]} | {ratings_list[0]} | {review_descriptions[0]}" if review_titles else None
                    review_data_2 = f"{review_titles[1]} | {ratings_list[1]} | {review_descriptions[1]}" if len(review_titles) > 1 else None
                    review_data_3 = f"{review_titles[2]} | {ratings_list[2]} | {review_descriptions[2]}" if len(review_titles) > 2 else None
                    review_data_4 = f"{review_titles[3]} | {ratings_list[3]} | {review_descriptions[3]}" if len(review_titles) > 3 else None
                    review_data_5 = f"{review_titles[4]} | {ratings_list[4]} | {review_descriptions[4]}" if len(review_titles) > 4 else None

                except:
                    print("No review.")
            
            else:
                print("No movies found.")
            
        
            if data_found is True:
                db.insert_data(Movie=Movie_name,
                           Imdb_rating=rating,
                           Popularity= popularity,
                           Storyline = storyline,
                           Genre= genres_string,
                           Review_1 = review_data_1,
                           Review_2 = review_data_2,
                           Review_3 = review_data_3,
                           Review_4 = review_data_4,
                           Review_5 = review_data_5,
                           status= "Success")

            if data_found is False:
                print("No data found for", Movie_name)
                db.insert_data(Movie=Movie_name,
                   Imdb_rating='N/A',
                   Popularity='N/A',
                   Storyline='N/A',
                   Genre='N/A',
                   Review_1='N/A',
                   Review_2='N/A',
                   Review_3='N/A',
                   Review_4='N/A',
                   Review_5='N/A',
                   status="No element found")


            
    def close_browser():
        sel.close_browser()
        pass
      
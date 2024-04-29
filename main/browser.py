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
            sel.input_text(search_path,row['Movie'])
            sel.press_keys(None,'\ue007' )  #\ue007
            # sel.click_element("//button[@id='suggestion-search-button']")
            sel.click_element(movie_path)
            Movie_name = row['Movie']
            try:
                sel.click_element(exact_results)
            except Exception as e:
                print(f"Exception: {e}")
                # print(f"No locator found for exact results for movie: {row['Movie']}")
                # TV Movie locator instead
                sel.click_element(tv_movie_path)
                sel.click_element(exact_results)

            li_count = sel.get_element_count(movie_list)
            # print(f"Number of li elements inside the unordered list: {li_count}")

            latest_release_date = None
            latest_movie_element = None

            
            for i in range(1, li_count + 1):
                date_xpath = f'//*[@id="__next"]/main/div[2]/div[3]/section/div/div[1]/section[2]/div[2]/ul/li[{i}]/div[2]/div/ul[1]'
                date_element = sel.find_element(date_xpath)
                release_date = date_element.text.strip()  # Extract the release date text
                # Find the release date and compare it with the latest release date found so far
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
                genre_xpath = "//li[@data-testid='storyline-genres']//ul[@role='presentation']"
                sel.scroll_element_into_view(genre_xpath)
                sel.wait_until_element_is_visible(genre_xpath)
                genre_elements = sel.find_elements(genre_xpath)
                genres = [genre.strip() for genre_element in genre_elements for genre in sel.get_text(genre_element).split(",")]
                print("Genres:", genres)

                # genre_xpath = "//li[@data-testid='storyline-genres']//ul[@role='presentation']"
                # sel.scroll_element_into_view(genre_xpath)
                # sel.wait_until_element_is_visible(genre_xpath)
                # genre_elements = sel.find_elements(genre_xpath)
                # genre_texts = []
                # for genre_element in genre_elements:
                #     genre_texts.append(sel.get_text(genre_element))
                # genres = ", ".join(genre_texts)
                # print("Genres:", genres)


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
                    #title of the review
                    # title_elements = sel.find_elements('//a[@class="title"]')[:5]
                    # for i, element in enumerate(title_elements, start=1):
                    #     text_content = sel.get_text(element)
                    #     print(f"Review {i}: {text_content}")

                    title_elements = sel.find_elements('//a[@class="title"]')[:5]
                    review_titles = []
                    for i, element in enumerate(title_elements, start=1):
                        text_content = sel.get_text(element)
                        review_titles.append(f"Review {i}: {text_content}")
                    print(review_titles)



                    #review rating
                    # rating_elements = sel.find_elements('//span[@class="rating-other-user-rating"]')[:5]
                    # for i, rating_element in enumerate(rating_elements, start=1):
                    #     rating_review = sel.get_text(rating_element)
                    #     print(f"Rating {i}: {rating_review}")

                    rating_elements = sel.find_elements('//span[@class="rating-other-user-rating"]')[:5]
                    ratings_list = []
                    for i, rating_element in enumerate(rating_elements, start=1):
                        rating_review = sel.get_text(rating_element)
                        ratings_list.append(f"Rating {i}: {rating_review}")
                    print(ratings_list)

                    #expand all
                    expander_xpath = '//*[@class="expander-icon-wrapper spoiler-warning__control"]'
                    try:
                        expander_elements = sel.find_elements(expander_xpath)
                        for expander_element in expander_elements:
                            sel.click_element(expander_element)
                    except: 
                        pass

                    #description
                    # #description
                    # review_container_xpath = "//div[@class='text show-more__control']"
                    # try:
                    #     review_container_elements = sel.find_elements(review_container_xpath)
                    #     num_containers = len(review_container_elements)
                    #     print(f"Number of review containers found: {num_containers}")
                    #     review_descriptions = []  # Initialize a list to store review descriptions
                    #     num_to_print = min(5, num_containers)
                    #     for i in range(num_to_print):
                    #         description_text = sel.get_text(review_container_elements[i])
                    #         review_descriptions.append(description_text)  # Append description to the list
                    # except:
                    #     review_descriptions = []  # Handle the case when no review containers are found
                    #     print("No review containers found.")
                    # print("Review Descriptions:", review_descriptions)  # Print the list of review descriptions





                    review_container_xpath = "//div[@class='text show-more__control']"
                    try:
                        review_container_elements = sel.find_elements(review_container_xpath)
                        num_containers = len(review_container_elements)
                        print(f"Number of review containers found: {num_containers}")
                        num_to_print = min(5, num_containers)
                        for i in range(num_to_print):
                            description_text = sel.get_text(review_container_elements[i])
                            print(f"Review Description {i + 1}: {description_text}")

                    except:
                        description_text = None
                        print("No review containers found.")
                except:
                    review='N/A'
                    print("No reviews.")
            else:
                print("No movies found.")

            
            # print(type(Movie_name))
            # print(type(rating))
            # print(type(popularity))
            # print(type(storyline))
            # print(type(genres))
            # print(type(ratings_list))
            # print(type(review_titles))
            # print(type(description_text))

            db.insert_data(Movie=Movie_name,
                           Imdb_rating=rating,
                           Popularity= popularity,
                           Storyline = storyline,
                           Genre= genres,
                           Review_rating = ratings_list,
                           Review_titles = review_titles,
                           Review_description = description_text,
                           status="Success")
        else:
            print(f"No movies found with the name",Movie_name)
            db.insert_data(Movie=None,
                           Imdb_rating=None,
                           Popularity= None,
                           Storyline = None,
                           Genre= None,
                           Review_rating = None,
                           Review_titles = None,
                           Review_description = None,
                           status="No element found")

            
    def close_browser():
        sel.close_browser()
        pass
      

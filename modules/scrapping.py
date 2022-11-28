from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def build_result_dict_and_append_to_array(search_results):
    """Builds a list containing dictionaries based on the obtained searched results 

    :param search_results: search results previously fetched
    :type search_results: ???

    :return: Array containing all results as dicts with correct formatting
    :rtype: list
    """
    origin_array = []
    for result in search_results:
        fetched_result_data = result.text.split('\n')
        #Remove Mas vendido or Oferta del dia from title
        if (fetched_result_data[0] in ["MÁS VENDIDO", "OFERTA DEL DÍA"]):
            fetched_result_data.pop(0)
        
        result_title = fetched_result_data[0]
        result_price = f"${fetched_result_data[3]}"
        result_extras = fetched_result_data[4:]

        #Removes llega gratis mañana from extras to save it as a boolean value
        if ("Llega gratis mañana" in result_extras):
            result_extras.remove("Llega gratis mañana")
            result_arrives_tmrw = "SI"
        else:
            result_arrives_tmrw = "NO"

        result_data_dict = dict(
            TITLE= result_title,
            PRICE= result_price,
            EXTRAS= result_extras,
            FREE_SHPPNG_TMRW= result_arrives_tmrw
        )
        origin_array.append(result_data_dict)

    return origin_array

def search_items(term):
    """Searches for items in amazon and returns the results

    :return: Array containing all results as dicts with correct formatting
    :rtype: list
    """
    PATH = '/Users/agustinfranchetti/Workspace/meli-scrapper-backend/drivers/chromedriver'
    #To run withouth opening the browser    
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--headless")
    driver = webdriver.Chrome(PATH, options=chromeOptions);

    driver.get('https://mercadolibre.com.ar/')

    print('-------TITLE-------')
    print(driver.title)
    
    search = driver.find_element("name", 'as_word')
    search.send_keys(term)

    # # TODO: -> Wait for request?
    # search_suggestions = driver.find_elements('xpath', "//*[starts-with(@id, 'cb1-opt1')]")

    # print('----SUGGESTIONS START----')
    # for suggestion in search_suggestions:
    #     print(suggestion.text)
    # print('-----SUGGESTIONS END-----')

    # time.sleep(1)

    search.send_keys(Keys.RETURN)

    #TODO: -> Wait for redirect

    # RAW RESULTS AS DICT
    search_results = driver.find_elements('xpath',"//*[starts-with(@class, 'ui-search-result__wrapper')]")

    results_array = build_result_dict_and_append_to_array(search_results)

    driver.quit()
    print('⚡️DONE⚡️')
    return results_array
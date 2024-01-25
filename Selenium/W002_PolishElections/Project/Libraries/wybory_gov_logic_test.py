from wybory_gov import WyboryGov
import wybory_gov_logic







wybory_gov_logic.save_data_from_all_districts()

url = "https://wybory.gov.pl/sejmsenat2023/pl/sejm/wynik/okr/2"
url_elecion = r"https://wybory.gov.pl/sejmsenat2023/pl/sejm/wynik/pl"
webdriver_path = r"C:\Program Files (x86)\chromedriver.exe"
wybory_gov_instance = WyboryGov()
# Open url
wybory_gov_instance.open_url(url_elecion, webdriver_path)

# pd_results = wybory_gov_instance.get_votes_results_divided_by_committee()

# pd_winers = wybory_gov_instance.get_district_winners()
# pd_winers2 = wybory_gov_instance.unify_committe_names(pd_winers.copy())

try:
    pd_votes = wybory_gov_instance.get_electoral_districts_links()
except Exception as error_message:
    print(str(error_message))
print("Check")

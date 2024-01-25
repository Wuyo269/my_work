import pandas as pd
import datetime
import  os

dt1 = "19.03.2024 19:05"
dt2 = "26.03.2024 10:05"

dt1 =  datetime.datetime.strptime(dt1, "%d.%m.%Y %H:%M")
dt2 =  datetime.datetime.strptime(dt2, "%d.%m.%Y %H:%M")


url = r"https://www.kiwi.com/pl/search/results/malaga-hiszpania/katowice-polska,krakow-polska/2024-02-05_2024-02-20"
url2 = r"https://www.kiwi.com/pl/search/results/malaga-hiszpania/katowice-polska,krakow-polska/2024-02-05_2024-02-20/no-return?stopNumber=0%7Etrue"

one_way = "no-return"
direct_fly = "?stopNumber=0%7Etrue"
url3 =f"https://www.kiwi.com/pl/search/results/malaga-hiszpania/katowice-polska,krakow-polska/2024-02-05_2024-02-20/{one_way}{direct_fly}"

#Build kiwi url based on proivided criteria
def build_kiwi_url(airport_start = "", airport_end = "",datetime_start = "", datetime_end = "", b_one_way =True, b_direct_fly = True):
    #DEBUG
    #dt1 = "19.03.2024 19:05"
    #dt2 = "26.03.2024 10:05"
    #datetime_start = datetime.datetime.strptime(dt1, "%d.%m.%Y %H:%M")
    #datetime_end = datetime.datetime.strptime(dt2, "%d.%m.%Y %H:%M")

    #One way or return
    if b_one_way:
        one_way = "no-return"
    else:
        one_way = ""

    #direct fly or multiple airports
    if b_direct_fly:
        direct_fly = "?stopNumber=0%7Etrue"
    else:
        direct_fly = ""

    #Date range
    date_range = f"{datetime_start:%Y}-{datetime_start:%m}-{datetime_start:%d}_{datetime_end:%Y}-{datetime_end:%m}-{datetime_end:%d}"

    #Create final url
    url = f"https://www.kiwi.com/pl/search/results/{airport_start}/{airport_end}/{date_range}/{one_way}{direct_fly}"

    return url

#dictionary of cities presented on kiwiw website
#kiwi_dict["malaga"] = "malaga-hiszpania"
def build_kiwi_dict():
    kiwi_dict = {}
    kiwi_dict["malaga"] = "malaga-hiszpania"
    kiwi_dict["katowice"] = "katowice-polska"
    kiwi_dict["krakow"] = "krakow-polska"
    return  kiwi_dict

#Calculate how many nights are between dates
def midnights(dt1, dt2):
    dt1 = datetime.datetime.strptime(dt1, "%d.%m.%Y %H:%M")
    dt2 = datetime.datetime.strptime(dt2, "%d.%m.%Y %H:%M")
    dt1 = dt1.replace(hour=0, minute=0, second=0, microsecond=0)
    dt2 = dt2.replace(hour=0, minute=0, second=0, microsecond=0)
    return (dt2 - dt1).days

#Calculate how many days are between dates
def wholedays(dt1, dt2):
    #DEBUG
    #dt1 = "13.03.2024 17:20"
    #dt2 = "20.03.2024 21:45"
    dt1 = datetime.datetime.strptime(dt1, "%d.%m.%Y %H:%M")
    dt2 = datetime.datetime.strptime(dt2, "%d.%m.%Y %H:%M")

    #If start date start after 10 do not count it
    if dt1.hour > 10:
        dt1 = dt1.replace(day=dt1.day+1)
    # If end date is after 18 do not count it
    if dt2.hour > 18:
        dt2 = dt2.replace(day=dt2.day+1)

    dt1 = dt1.replace(hour=0, minute=0, second=0, microsecond=0)
    dt2 = dt2.replace(hour=0, minute=0, second=0, microsecond=0)
    return (dt2 - dt1).days

#Apend data to excel
def append_to_excel(fpath, df):
    #If excel exist read sheet as DataTable
    if (os.path.exists(fpath)):
        df_current=pd.read_excel(fpath)
    #If excel does not exist create new DataTable
    else :
        df_current=pd.DataFrame()

    df_concat=pd.concat([df,df_current])
    df_concat.to_excel(fpath,index=False)

#Create combination af all flies from the dataframes
def create_fly_combinations(in_excel_departure, in_excel_arrival):
    #Read input excels
    df_departure = pd.read_excel(in_excel_departure)
    df_arrival = pd.read_excel(in_excel_arrival)

    #Rename columns in arrival
    df_arrival.rename(columns={"departure_datetime": "arrival_datetime", "departure_price": "arrival_price",
                        "departure_company":"arrival_company","departure_airport_in":"arrival_airport_in",
                        "departure_airport_out":"arrival_airport_out"}, inplace=True)

    #Create every combination based on two dataframes
    df_departure.merge(df_arrival, how='cross')
    df_departure['key'] = 1
    df_arrival['key'] = 1
    df_fly_combination = pd.merge(df_departure, df_arrival, on='key').drop('key', axis=1)

    return df_fly_combination

#Add additional columns with calculations
def transform_fly_combinations(df_fly_combination):
    # Total price for both flies
    df_fly_combination["total_price"] = df_fly_combination["departure_price"].astype("int") + df_fly_combination[
        "arrival_price"].astype("int")
    # Convert datetime strings to datetime variables
    pd.to_datetime(df_fly_combination['departure_datetime'])
    pd.to_datetime(df_fly_combination['arrival_datetime'])
    # Count how many days are in trip
    df_fly_combination["days"] = df_fly_combination.apply(
        lambda x: wholedays(x["departure_datetime"], x["arrival_datetime"]), axis=1)
    # Count how many nights are in trip
    df_fly_combination["nights"] = df_fly_combination.apply(
        lambda x: midnights(x["departure_datetime"], x["arrival_datetime"]), axis=1)
    # Check if the start airport and end airport are the same
    df_fly_combination["same_airport"] = df_fly_combination["departure_airport_in"] == df_fly_combination[
        "arrival_airport_out"]
    # Check if there is more nights than days
    df_fly_combination["days_night_difference"] = df_fly_combination["days"] - df_fly_combination["nights"]

    return  df_fly_combination


excel_name = "output_flies_polska.xlsx"
excel_name2 = "output_flies_malaga.xlsx"
out_excel_results = "vacacjones.xlsx"


df_fly_combination = create_fly_combinations(in_excel_departure=excel_name, in_excel_arrival=excel_name2)

df_fly_combination = transform_fly_combinations(df_fly_combination)

# Same results to excel
append_to_excel(out_excel_results, df_fly_combination)




print("S")
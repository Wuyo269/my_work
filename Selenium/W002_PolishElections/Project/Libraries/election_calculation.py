import  pandas as pd




file_path = r"C:\Users\mwojcik\OneDrive - Sopra Steria\Desktop\SopraSteria\Python\Selenium\W002_PolishElections\Project\Data\Test\Okręg wyborczy nr 3.xlsx"

df_Dhondt = pd.read_excel(file_path, sheet_name="df_person_results")
in_mandates_in_district = 14

#Sum votes number
df_Dhondt_sum = df_Dhondt.groupby(['committee_name'])['votes_number'].sum()



#Sort by Votes number
df_Dhondt.sort_values(by=["votes_number"], ascending=False, inplace=True)
#Limit df to number of mandates in district
df_Dhondt = df_Dhondt.head(in_mandates_in_district)
#Group by Party Name
df_Dhondt = df_Dhondt.groupby(['party_name'])['party_name'].count()

print("")
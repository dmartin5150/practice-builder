from components.GenertatedPractice import Generated_Practice
import pandas as pd
import numpy as np
import os
from util.utilities import reformat_ascension_name


data1 = pd.read_csv('data1.csv')
data2 = pd.read_csv('data2.csv')
data3 = pd.read_csv('data3.csv')
data4 = pd.read_csv('data4.csv')
data5 = pd.read_csv('data5.csv')
originial_list = pd.read_csv('ASMCA Surgeon List - ASMCA Surgeon List - 24 Months.csv')
headers = originial_list.iloc[1]
originial_list  = pd.DataFrame(originial_list.values[2:], columns=headers)
# case_volumes = originial_list[['Surgeon','Surgeon Case Volume']].rename(columns={'Surgeon': 'Ascension_Name'})
case_volumes = originial_list[['Surgeon','Surgeon Case Volume']].rename(columns={'Surgeon': 'Ascension_Name'})
# print('case_volumes', case_volumes)
final_data = pd.concat(
            (data1, data2), ignore_index=True, axis=0)
final_data = pd.concat(
            (final_data, data3), ignore_index=True, axis=0)
final_data = pd.concat(
            (final_data, data4), ignore_index=True, axis=0)
final_data = pd.concat(
            (final_data, data5), ignore_index=True, axis=0)
print(final_data.columns)
case_volumes['Ascension_Name'] = case_volumes['Ascension_Name'].apply(lambda x: reformat_ascension_name(x) )
final_data = final_data.merge(case_volumes, left_on='Ascension_Name', right_on='Ascension_Name',how='right')

# print(data_with_case_volumes.columns)
final_data['Clinic_Name'].fillna(final_data['Ascension_Name'] +"'S CLINIC", inplace=True)
final_data['Clinic_Name'] = final_data['Clinic_Name'].apply(lambda x:x.strip().upper())
final_data['Ascension_Name'] = final_data['Ascension_Name'].apply(lambda x:x.strip().upper())
print('test2')



def update_clinic_list(practice, clinic_list):
    new_list = []
    for clinic in clinic_list:
        if clinic not in practice.new_clinics:
            new_list.append(clinic)
    return new_list



practice_list = []
matched_clinics = []
working_clinic_list = final_data['Clinic_Name'].unique()
i=1 
while len(working_clinic_list) > 0:
    cur_clinic = working_clinic_list[0]
    practice = Generated_Practice(f'{cur_clinic} Practice',final_data)
    cur_clinic = working_clinic_list[0]
    # print(cur_clinic)
    practice.generate_practice_data(cur_clinic)
    practice_list.append(practice)
    matched_clinics.append(practice.new_clinics)
    working_clinic_list = update_clinic_list(practice, working_clinic_list)
    # print(len(working_clinic_list))
    i=i+1




def write_practice_clinics_excel_worksheet(writer,practice_list, full_dataframe, worksheet_name='clinics') :
    columns = ['Clinic_Name', 'Address', 'City', 'State', 'Zip', 'Phone', 'Practice_Link']
    all_data = pd.DataFrame(columns=['Practice_Name','Clinic_Name', 'Address', 'City', 'State', 'Zip', 'Phone', 'Practice_Link'])
    blank_row = pd.DataFrame(columns=['Practice_Name','Clinic_Name', 'Address', 'City', 'State', 'Zip', 'Phone', 'Practice_Link'])
    current_practice_name = pd.DataFrame(columns=['Practice_Name','Clinic_Name', 'Address', 'City', 'State', 'Zip', 'Phone', 'Practice_Link'])
    blank_row.loc[0,0] = ''
    print(final_data.columns)
    for practice in practice_list:
        current_practice_name.loc[0,0]=practice.name
        all_data = pd.concat((all_data, current_practice_name),ignore_index=True, axis=0)
        clinic_dataframe = full_dataframe[full_dataframe['Clinic_Name'].isin(practice.new_clinics)][columns].drop_duplicates()
        all_data = pd.concat((all_data, clinic_dataframe),ignore_index=True, axis=0)
        all_data = pd.concat((all_data, blank_row),ignore_index=True, axis=0)
    print(all_data.shape[0])
    try: 
        all_data.to_excel(writer,sheet_name=worksheet_name, index=False)
    except:
        print ('Error')

def write_practice_clinics_surgeons_excel_worksheet(writer,practice_list, full_dataframe, worksheet_name='surgeons') :
    columns = ['Clinic_Name','Ascension_Name', 'Specialty','Surgeon Case Volume', 'Webmd_Link']
    all_data = pd.DataFrame(columns= columns)
    blank_row = pd.DataFrame(columns=columns)
    current_clinic_name = pd.DataFrame(columns=columns)
    current_practice_name = pd.DataFrame(columns=columns)
    blank_row.loc[0,0] = ''
    print(final_data.columns)
    for practice in practice_list:
        clinic_names = full_dataframe[full_dataframe['Clinic_Name'].isin(practice.new_clinics)]['Clinic_Name'].unique().tolist()
        current_practice_name.loc[0,0]= 'Practice: ' + practice.name
        all_data = pd.concat((all_data, current_practice_name),ignore_index=True, axis=0)
        for clinic_name in clinic_names:
            current_clinic_name.loc[0,0]='Clinic: ' + clinic_name
            surgeons = full_dataframe[full_dataframe['Clinic_Name']== clinic_name][columns].drop_duplicates()
            surgeons['Clinic_Name'] = ''
            all_data = pd.concat((all_data, current_clinic_name),ignore_index=True, axis=0)
            all_data = pd.concat((all_data, surgeons),ignore_index=True, axis=0)
            all_data = pd.concat((all_data, blank_row),ignore_index=True, axis=0)
    print(all_data.shape[0])
    try: 
        all_data.to_excel(writer,sheet_name=worksheet_name, index=False)
    except:
        print ('Error')


def write_practices_excel(practice_list, filename='SMCA_Practices.xlsx'):
    path = os.getcwd()
    writer = pd.ExcelWriter(os.path.join(path,filename) , engine='xlsxwriter')
    write_practice_clinics_excel_worksheet(writer, practice_list, final_data)
    write_practice_clinics_surgeons_excel_worksheet(writer, practice_list, final_data)
    writer.save()


write_practices_excel(practice_list)
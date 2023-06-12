import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import io
import zipfile
import random
import string
from glob import glob

temp_zip_folder = './temp/'
temp_zip_file = temp_zip_folder + 'data.zip'

if not os.path.isdir('./temp'):
    os.makedirs('./temp/', exist_ok=True)

def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

def store_data(file, temp_data_directory, temporary_location=temp_zip_file):
    
    #st.warning('Loading data from zip.')

    #with open(temp_data_directory, 'wb') as out:
    with open(temporary_location, 'wb') as out:
        out.write(file.getbuffer())
    
    #if is_zip_oversized(temporary_location):
    #    st.warning('Oversized zip file.')
    #    # clear_data_storage(temporary_location)
    #    return False

    with zipfile.ZipFile(temporary_location) as zip_ref:        
        zip_ref.extractall(temp_data_directory + '/')
        st.success('The file is uploaded')
        
    # clear_data_storage(temp_zip_folder)

    return True

# from sklearn.metrics import (accuracy_score, auc, f1_score, precision_score, recall_score,
#                             mean_absolute_error, mean_squared_error, r2_score)
st.set_option('deprecation.showfileUploaderEncoding', False)

# funtions
def relative_time(t_diff):
    days, seconds = t_diff.days, t_diff.seconds
    if days > 0:
        return f"{days}d"
    else:
        hours = t_diff.seconds // 3600
        minutes = t_diff.seconds // 60
        if hours >0 : #hour
            return f"{hours}h"
        elif minutes >0:
            return f"{minutes}m"
        else:
            return f"{seconds}s"

def get_leaderboard_dataframe(csv_file = 'leaderboardLASC.csv', greater_is_better = True):
    df_leaderboard = pd.read_csv('leaderboardLASC.csv', header = None)
    print(df_leaderboard)
    df_leaderboard.columns = ['Segmenter Name', 'Baseline or Follow-up', 'Score (cm^3 difference)', 'Segmentation Tool', 'Submission Time']
    #df_leaderboard['counter'] = 1
    #df_leaderboard = df_leaderboard.groupby('Segmenter Name').agg({"Score (cm^3 difference)": "min",
    #                                                        "counter": "count",
    #                                                        "Submission Time": "max"})
    df_leaderboard = df_leaderboard.sort_values("Score (cm^3 difference)", ascending = not greater_is_better)
    df_leaderboard = df_leaderboard.reset_index()
    #df_leaderboard.columns = ['Segmenter Name','Score (cm^3 difference)', 'Entries', 'Last']
    #df_leaderboard['Last'] = df_leaderboard['Last'].map(lambda x: relative_time(datetime.now() - datetime.strptime(x, "%Y%m%d_%H%M%S")))
    return df_leaderboard

def app():
    # Title
    st.title("Lymph Atar Segmentation Challenge Leaderboard")

    # Username Input
    username = st.text_input("Username", max_chars= 20,)
    username = username.replace(",","") # for storing csv purpose
    #st.header(f"Hi {username} !!!")

    # Check if master data has been registered:
    master_files = os.listdir('master')

    image_type = st.radio(
    "Which images was used for the segmentation:",
    ('Baseline', 'Follow-up'))

    segmentation_tool = st.text_input("Segmentation tool:",  max_chars= 20,)
    #if ("via_project_9Dec2020_15h40m_Les_ground_truth.json" not in master_files):
    #    st.text("Admin please insert ground truth data")
    #else:

    score = st.text_input("Total volume of the 14 lesions (cm^3):",  max_chars= 20,)
    greater_is_better = False# if metric_type in ["MAE", "MSE"] else True # CHANGE HERE AS YOU WANT
    #global temp_data_directory
    #temp_data_directory = f'./data/{get_random_string(15)}/'
    #os.makedirs(temp_data_directory, exist_ok=True)
    #uploaded_file = st.file_uploader("Upload Submission Segmentation File (supported formats: .nii, nii.gz, .nrrd)", 
    #                                 type=['nii', 'gz', 'nrrd', 'zip'])
    
    #groud_truth_file = 'master/tb_ground_truth.json'
    if st.button("SUBMIT"):
        #if uploaded_file is None:
        #    st.text("UPLOAD FIRST")
        #else:
            #print(uploaded_file.name)
            #store_data(uploaded_file, temp_data_directory)
            ## save submission
            ##print(uploaded_file)
            #path_to_file = os.path.join(temp_data_directory, 
            #                            uploaded_file.name.replace('.zip',''))
            ##print(path_to_file)
            ##file_bytes = np.asarray(bytearray(uploaded_file.read()))
            ##print(file_bytes.shape)
            #image_seg = sitk.ReadImage(path_to_file)# sitk.ReadImage(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
            ##print(image_seg)
            #
            #label_map = sitk.LabelImageToLabelMap(image1=image_seg)# calculate score
            #label_map_float = sitk.Cast(label_map, sitk.sitkInt16)
            #
            #label_stats = sitk.LabelShapeStatisticsImageFilter()
            #label_stats.Execute(image1=label_map_float)
            #number_of_labels = label_stats.GetNumberOfLabels()
            #
            ##print(number_of_labels)
            #merged_label_map=sitk.RelabelComponent(label_map_float)
            # 
            ##label_stats_ps = sitk.LabelShapeStatisticsImageFilter()
            ##label_stats_ps.Execute(image1=merged_label_map)
            ##physical_size = label_stats_ps.GetPhysicalSize(1)#

            #if number_of_labels == 15:
            #    merged_label_map = sitk.BinaryThreshold(merged_label_map, lowerThreshold=2)
            #label_stats_ps = sitk.LabelShapeStatisticsImageFilter()
            #label_stats_ps.Execute(image1=merged_label_map)
            #physical_size = label_stats_ps.GetPhysicalSize(1)
            #
            ##print(physical_size)
            ##dice_scores_user = dicescoring.dice_list(groud_truth_file, uploaded_file)
            #
            #score = abs(physical_size*10e-3 - 113.30)
            #st.text(f"YOUR score was: {score}")
            ## save score
        score = abs(float(score) - 113.30)
        datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open("leaderboardLASC.csv", "a+") as leaderboard_csv:
            leaderboard_csv.write(f"{username}, {image_type},{score},{segmentation_tool},{datetime_now}\n")
            'Segmenter Name', 'Baseline or Follow-up', 'Score (cm^3 difference)', 'Segmentation Tool', 'Submission Time'

        # Showing Leaderboard
        st.header("Leaderboard")
        if os.stat("leaderboardLASC.csv").st_size == 0:
            st.text("NO SUBMISSION YET")
        else:
            df_leaderboard = get_leaderboard_dataframe(csv_file = 'leaderboardLASC.csv', greater_is_better = greater_is_better)
            hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            df_leaderboard['index']+=1
            df_leaderboard.rename(columns={"index": "Place"}, inplace=True)
            df_leaderboard['Place']=[i+1 for i in range(len(df_leaderboard['Place']))]
            st.table(df_leaderboard)
            

    # To register master data
    if username == 'lasc_admin_siim21': # CHANGE HERE AS YOU WANT
        change_master_key = st.checkbox('Change Ground Truth File')

        if change_master_key:

            # Master Data Frame
            uploaded_file_master = st.file_uploader("Upload Ground Truth File", type='json')
            if uploaded_file_master is not None:
                stringio = io.StringIO(uploaded_file_master.getvalue().decode("utf-8"))
    #            f_uploaded_submission_master = open(stringio)
    #            json_uploaded_submission_master = json.load(f_uploaded_submission_master)
                json_uploaded_submission_master = json.load(stringio)
                datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open('master/lasc_ground_truth.json', 'w') as outfile:
                    json.dump(json_uploaded_submission_master, outfile)
            
    

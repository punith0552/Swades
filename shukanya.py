import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

city=input("""Enter your city :  Vatasavai
| Jaggayyapeta     
| Veerullapadu     
| Gampalagudem     
| A. Konduru       
| Bapulapadu       
| Agiripalli       
| G. Konduru       
| Kanchikacharla   
| Chandarlapadu    
| Ibrahimpatnam    
| Vijayawada Urban 
| Vijayawada Rural 
| Gannavaram       
| Ungunturu        
| Penamaluru       
| Thotavalluru     
| Pamidimukkala """)

def SSY():
    # Load the dataset
    file_path = 'SSY.xlsx'
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    
    # Fill missing values with 0
    df.fillna(0, inplace=True)
    
    # Calculate the agricultural worker percentage for each city
    df['Total population of girls'] = df['0-6 age Rural Girls population '] + df['0-6 age Urban Girls population '] 
    df['Total 0-6 rural girls population']=df['Age Group rural 0–6'] - df['0-6 age Rural Boys population ']
    df['Total 0-6 urban girls population']=df['Age Group Urban 0–6'] - df['0-6 age Urban Boys population ']
    
    # Calculate the agricultural worker percentage for both male and female workers
    df['0-6 age Rural Girls population percentage'] = df['Total 0-6 rural girls population'] / df['Total population of girls']
    df['0-6 age Urban Girls population percentage'] = df['Total 0-6 urban girls population'] / df['Total population of girls']
    
    # Select relevant features (0-6 age Rural Girls population percentage and 0-6 age Urban Girls population percentage)
    X = df[['0-6 age Rural Girls population percentage', '0-6 age Urban Girls population percentage']].values
    
    # Apply KMeans clustering with 3 clusters (you can modify this based on the data)
    kmeans = KMeans(n_clusters=3, random_state=0)
    df['Cluster'] = kmeans.fit_predict(X)
    
    
    # Find cities where agricultural workers are a significant percentage of total workers
    recommended_cities = []
    
    for index, row in df.iterrows():
        # If agricultural male or female workers are more than 50% of total workers, consider recommending the KVP scheme
        if row['0-6 age Rural Girls population percentage'] > 0.50 or row['0-6 age Urban Girls population percentage'] > 0.50:
            recommended_cities.append({
                'City/Village Name': row['City/Village Name'],
                '0-6 age Rural Girls population percentage': row['0-6 age Rural Girls population percentage'],
                '0-6 age Urban Girls population percentage': row['0-6 age Urban Girls population percentage']
            })
    
    # Convert recommended cities into a DataFrame for easy viewing
    recommended_df = pd.DataFrame(recommended_cities)
    
    # Display cities eligible for KVP
    # print("Cities recommended for SSY Scheme based on agricultural worker percentage:")
    # print(recommended_df)
    # Calculate overall thresholds for agricultural male and female percentages
    ruralgirls_threshold = df['0-6 age Rural Girls population percentage'].mean()  # Mean for all rows in '0-6 age Rural Girls population percentage'
    urbangirls_threshold = df['0-6 age Urban Girls population percentage'].mean()  # Mean for all rows in '0-6 age Urban Girls population percentage'
    
    # Compare each row's percentage with the respective threshold and filter cities
    above_threshold_rural_girls = []
    above_threshold_urban_girls = []
    
    for index, row in df.iterrows():
        if row['0-6 age Rural Girls population percentage'] > ruralgirls_threshold:
            above_threshold_rural_girls.append({
                'City/Village Name': row['City/Village Name'],
                '0-6 age Rural Girls population percentage': row['0-6 age Rural Girls population percentage']
            })
        elif row['0-6 age Urban Girls population percentage'] > urbangirls_threshold:
            above_threshold_urban_girls.append({
                'City/Village Name': row['City/Village Name'],
                '0-6 age Urban Girls population percentage': row['0-6 age Urban Girls population percentage']
            })
    
    # Convert the filtered cities to a DataFrame
    above_threshold_df_ruralgirls = pd.DataFrame(above_threshold_rural_girls)
    above_threshold_df_urbangirls = pd.DataFrame(above_threshold_urban_girls)
    
    
    # Display cities exceeding the respective thresholds
    print("Cities where rural or urban percentages exceed their respective thresholds:")
    print("Cities percentages exceed their respective thresholds:")
    # print(above_threshold_df_ruralgirls)
    # print('') 
    return above_threshold_df_urbangirls['City/Village Name']




def KVP():
    # Load the dataset
    import pandas as pd
    from sklearn.cluster import KMeans
    
    file_path = 'KVP.xlsx'
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    
    # Fill missing values with 0
    df.fillna(0, inplace=True)
    
    # Calculate the agricultural worker percentage for each city
    df['Total Workers'] = df['Cultivators Male Workers'] + df['Cultivators Female Workers'] + df['Agricultural Labours Male Workers'] + df['Agricultural Labours Female Workers']
    df['Total Male Workers'] = df['Cultivators Male Workers'] + df['Agricultural Labours Male Workers']
    df['Total Female Workers'] = df['Cultivators Female Workers'] + df['Agricultural Labours Female Workers']
    
    # Calculate the agricultural worker percentage for both male and female workers
    df['Agricultural Male Percentage'] = df['Total Male Workers'] / df['Total Workers']
    df['Agricultural Female Percentage'] = df['Total Female Workers'] / df['Total Workers']
    
    # Select relevant features (Agricultural Male Percentage and Agricultural Female Percentage)
    X = df[['Agricultural Male Percentage', 'Agricultural Female Percentage']].values
    
    # Apply KMeans clustering with 3 clusters (you can modify this based on the data)
    kmeans = KMeans(n_clusters=3, random_state=0)
    df['Cluster'] = kmeans.fit_predict(X)
    
    
    # Find cities where agricultural workers are a significant percentage of total workers
    recommended_cities = []
    
    for index, row in df.iterrows():
        # If agricultural male or female workers are more than 50% of total workers, consider recommending the KVP scheme
        if row['Agricultural Male Percentage'] > 0.50:
            recommended_cities.append({
                'City/Village Name': row['City/Village Name']
            })
    
    # Convert recommended cities into a DataFrame for easy viewing
    recommended_df = pd.DataFrame(recommended_cities)
    
    # Calculate overall thresholds for agricultural male and female percentages
    male_threshold = df['Agricultural Male Percentage'].mean()  # Mean for all rows in 'Agricultural Male Percentage'
    female_threshold = df['Agricultural Female Percentage'].mean()  # Mean for all rows in 'Agricultural Female Percentage'
    
    # Compare each row's percentage with the respective threshold and filter cities
    above_threshold_agri_male = []
    above_threshold_agri_female = []
    
    for index, row in df.iterrows():
        if row['Agricultural Female Percentage'] > male_threshold:
            above_threshold_agri_male.append({
                'City/Village Name for Male agri Workers': row['City/Village Name']
            })
        elif row['Agricultural Female Percentage'] > female_threshold:
            above_threshold_agri_female.append({
                'City/Village Name for Female agri workers': row['City/Village Name']
            })
    
    above_threshold_df_male = pd.DataFrame(above_threshold_agri_male)
    above_threshold_df_female = pd.DataFrame(above_threshold_agri_female)
    
    # print(above_threshold_df_male)
    return above_threshold_df_female




def mahila():
    import pandas as pd
    from sklearn.cluster import KMeans
    
    # Load the dataset
    file_path = 'Female dataset .xlsx'  # Replace with the actual file path
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    
    # Fill missing values with 0
    df.fillna(0, inplace=True)
    
    # Calculate percentages for rural and urban female populations
    df['Total Population']=df['Rural population']+df['Urban population']
    df['Female Rural Population']=df['Rural population']-df['Rural Male Population']
    df['Rural Female Percentage'] = df['Female Rural Population']/df['Total Population']
    
    # Select relevant features (Rural and Urban Female Percentages)
    X = df['Rural Female Percentage'].values
    X=X.reshape(-1,1)
    
    # Apply KMeans clustering with 3 clusters (adjust clusters based on the data)
    kmeans = KMeans(n_clusters=3, random_state=0)
    df['Cluster'] = kmeans.fit_predict(X)
    
    # Recommend MSSC scheme for cities/villages where rural or urban female population is significant
    recommended_cities = []
    
    for index, row in df.iterrows():
        # If Rural or Urban Female Percentage is more than 50%, recommend MSSC scheme
        if row['Rural Female Percentage'] > 0.5:
            recommended_cities.append({
                'City/Village Name': row['City/Village Name']
            })
    
    # Convert recommended cities into a DataFrame for easy viewing
    recommended_df = pd.DataFrame(recommended_cities)
    
    print("Cities recommended for MSSC based on significant Female Population:")
    # print(recommended_df)
    
    # Calculate overall thresholds for rural and urban female percentages
    rural_threshold = df['Rural Female Percentage'].mean()  # Mean of rural female percentages
    # Compare each row's percentage with the respective threshold and filter cities
    above_threshold_cities_rural = []
    
    for index, row in df.iterrows():
        if row['Rural Female Percentage'] > rural_threshold:
            above_threshold_cities_rural.append({
                'City/Village Name': row['City/Village Name'],
                'Rural Female Percentage': row['Rural Female Percentage']
            })
    
    # Convert the filtered cities into DataFrames
    above_threshold_df_rural = pd.DataFrame(above_threshold_cities_rural)
    return above_threshold_df_rural['City/Village Name']




#print(KVP())
# print(SSY())
# print(mahila())
if city in list(KVP()):
    print(" Kishan, ")
if city in list(SSY()):
    print(" Sukanya, ")
if city in list(mahila()):
    print(" Mahila, ")

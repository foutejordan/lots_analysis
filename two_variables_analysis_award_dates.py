from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

categories = {
    77: 'Agriculture et espaces verts',
32: 'Appareils radio, télévision, communication, télécommunication',
31: 'Appareils, équipements, consommables électriques et d’éclairage',
92: 'Arts, spectacle, divertissements, sport',
98: 'Autres services communautaires, sociaux et personnels',
41: 'Eau collectée et purifiée',
80: 'Education et formation',
9: 'Energie, gaz, fluides et services connexes',
90: 'Environnement, eau, assainissement, propreté',
35: 'Equipement de sécurité, lutte contre l’incendie, police et défense',
34: 'Equipement de transport et produits auxiliaires pour le transport',
43: 'Equipement minier et carrières, matériel de construction',
38: 'Equipements de laboratoire, d’optique et de précision',
79: 'Etudes, conseil, services aux entreprises',
14: 'Exploitation minière et minerais',
22: 'Imprimés et produits connexes',
37: 'Instruments de musique, articles de sport, jeux, artisanat, arts',
48: 'Logiciels et systèmes d’information',
16: 'Machines agricoles',
42: 'Machines industrielles',
30: 'Machines, matériel et fourniture informatique et de bureau',
44: 'Matériaux et structures de construction, produits pour la construction',
33: 'Matériels médicaux, pharmaceutiques, produits de soins personnels',
39: 'Meubles, aménagements, électroménager, produits de nettoyage',
3: 'Produits agricoles, élevage, pêche, sylviculture et connexes',
15: 'Produits alimentaires, boissons, tabac et produits connexes',
24: 'Produits chimiques',
19: 'Produits cuir et textiles, plastique, caoutchouc',
55: 'Service d’hébergement et de restauration',
63: 'Services d’appui dans les transports, services des agences de voyage',
71: 'Services d’architecture, de construction, d’ingénierie et d’inspection',
75: 'Services de l’administration publique, défense, sécurité sociale',
73: 'Services de R&D, services de conseil connexes',
50: 'Services de réparation et d’entretien',
85: 'Services de santé et d’action sociale',
72: 'Services de technologies de l’information, conseil, développement de logiciels, internet et appui',
60: 'Services de transport (à l’exclusion du transport des déchets)',
64: 'Services des postes et télécommunications',
51: 'Services d’installation',
66: 'Services financiers et d’assurance',
70: 'Services immobiliers',
65: 'Services publics',
76: 'Services relatifs à l’industrie du pétrole et du gaz',
45: 'Travaux de construction, BTP',
18: 'Vêtements, articles chaussants, bagages et accessoires'
}

var_cat = ['typeOfContract', 'cpv']

file_path = 'data/Lots.csv'

# Read the CSV file into a pandas DataFrame
df_Lots = pd.read_csv(file_path, parse_dates=['awardDate'], low_memory=False)

def point_biserial_correlation(df, category_column, numeric_column):
    # Convert category_column to binary (0s and 1s)
    binary_column = (df[category_column] == df[category_column].mode().iloc[0]).astype(int)
    
    # Compute Pearson correlation coefficient between binary_column and numeric_column
    correlation = df[[binary_column.name, numeric_column]].corr().iloc[0, 1]
    
    return correlation

def filter_dates(df_lots_copy):
    df_lots_copy['awardDate'] = pd.to_datetime(df_lots_copy['awardDate'])
    start_date = datetime(2009, 1, 1)
    end_date = datetime.today()
    df_lots_out = df_lots_copy[(df_lots_copy['awardDate'] >= start_date) & (df_lots_copy['awardDate'] <= end_date)]
    return df_lots_out

# # Filter dates between 2009 and today
start_date = datetime(2009, 1, 1)
end_date = datetime.today()

df_Lots = df_Lots[(df_Lots['awardDate'] >= start_date) & (df_Lots['awardDate'] <= end_date)]

def draw_quantitatives_by_date(df_Lots_copy):

    variables = ['awardPrice', 'lotsNumber', 'numberTenders',
                            'correctionsNb', 'numberTendersSme', 'publicityDuration']

    awardDates = pd.to_datetime(df_Lots_copy['awardDate'])

    ''' Du début à la fin des dates (unité = mois) '''

    # Filter data up to today's date
    df_Lots_filtered = df_Lots_copy[awardDates <= pd.Timestamp.now()]

    months = awardDates.dt.to_period('M')

    #Handles wrong values from lotsNumber
    df_Lots_filtered['lotsNumber'] = pd.to_numeric(df_Lots_filtered['lotsNumber'], errors='coerce')

    for variable in variables:

        monthly_distribution = df_Lots_filtered.groupby(months)[variable].std().dropna()

        point_biserial_corr = point_biserial_correlation(df_Lots_filtered, 'awardDate', variable)

        # Write the correlation coefficient to a file
        with open('figs/two_variables_award_dates/'+variable+'_and_date_point_biserial_correlation.txt', 'w') as file:
            file.write(f"Point Biserial Correlation: {point_biserial_corr}")

        plt.figure(figsize=(15, 6))
        monthly_distribution.plot(marker='o', linestyle='-', color='b')
        plt.title('Distribution of '+variable+' Over Time')
        plt.xlabel('Time')
        plt.ylabel(variable)

        # Format the x-axis labels as Year-Month
        plt.xticks(monthly_distribution.index.strftime('%Y'), rotation=45, ha='right')

        plt.grid(True)
        plt.savefig('figs/two_variables_award_dates/'+variable+'_by_award_dates.png')
        #plt.show()

def draw_quantitatives_by_date_cyclic_over_year(df_Lots_copy):
    
    variables = ['numberTendersSme', 'publicityDuration']
        
    # # Read the CSV file into a pandas DataFrame, explicitly specifying the 'awardDate' column as datetime
    # df_Lots_copy = pd.read_csv(file_path, parse_dates=['awardDate'], low_memory=False)

    awardDates = df_Lots_copy['awardDate']

    # Filter data up to today's date
    df_Lots_filtered_2 = df_Lots_copy[awardDates <= pd.Timestamp.now()]

    for var in variables:

        # Create a new column for the month of the year
        df_Lots_filtered_2['MonthOfYear'] = df_Lots_filtered_2['awardDate'].dt.month

        # Group by month of the year and calculate the average of numberTenders
        avg_number_tenders_per_month = df_Lots_filtered_2.groupby('MonthOfYear')[var].std()

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(avg_number_tenders_per_month.index, avg_number_tenders_per_month.values, marker='o', linestyle='-', color='b')
        plt.title('Average Distribution of '+var+' Over a Year')
        plt.xlabel('Months of the Year')
        plt.ylabel('Average '+var)
        plt.grid(True)
        plt.savefig('figs/two_variables_award_dates/'+var+'_by_award_dates_cyclic.png')
        #plt.show()

def draw_qualitatives_by_date(df_Lots):

    # Assuming df_Lots has columns 'awardDate', 'cpv', and 'category'

    # Convert 'awardDate' to datetime if not already
    df_Lots['awardDate'] = pd.to_datetime(df_Lots['awardDate'])

    # Filter out rows with non-numeric first two characters in 'cpv'
    df_Lots = df_Lots[df_Lots['cpv'].astype(str).str[:2].str.isnumeric()]

    # Convert 'cpv' to int after filtering
    df_Lots['cpv_category'] = df_Lots['cpv'].astype(str).str[:2].astype(int)

    # Map the first two digits to the corresponding categories
    df_Lots['category'] = df_Lots['cpv_category'].map(categories)

    # Drop rows where 'category' is not mapped
    df_Lots = df_Lots.dropna(subset=['category'])

    plt.figure(figsize=(12, 8))

    # Count occurrences for each category on each date
    df_counts = df_Lots.groupby(['awardDate', 'category']).size().reset_index(name='count')

    # Use Seaborn's lineplot to plot multiple lines for each category
    sns.lineplot(x='awardDate', y='count', hue='category', data=df_counts)

    plt.title('Usage of Categories Over Time')
    plt.xlabel('Time')
    plt.ylabel('Category Count/Percentage')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    #plt.show()

def draw_typeOfContracts_by_date(df_Lots):

    # Assuming df_Lots has columns 'awardDate', 'cpv', and 'category'

    # Convert 'awardDate' to datetime if not already
    df_Lots['awardDate'] = pd.to_datetime(df_Lots['awardDate'])

    plt.figure(figsize=(12, 8))

    # Count occurrences for each category on each date
    df_counts = df_Lots.groupby(['awardDate', 'typeOfContract']).size().reset_index(name='count')

    # Use Seaborn's lineplot to plot multiple lines for each category
    sns.lineplot(x='awardDate', y='count', hue='typeOfContract', data=df_counts)

    plt.title('Usage of Categories Over Time')
    plt.xlabel('Time')
    plt.ylabel('Category Count/Percentage')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    #plt.show()

def draw_typeOfContracts_by_date_over_year(df_Lots):

    # Assuming df_Lots has columns 'awardDate', 'cpv', and 'category'

    # Convert 'awardDate' to datetime if not already
    df_Lots['awardDate'] = pd.to_datetime(df_Lots['awardDate'])

    plt.figure(figsize=(12, 8))

    # Extract month from 'awardDate'
    df_Lots['month'] = df_Lots['awardDate'].dt.month

    # Count occurrences for each typeOfContract in each month
    df_counts = df_Lots.groupby(['month', 'typeOfContract']).size().reset_index(name='count')

    # Calculate the average count for each typeOfContract in each month
    df_avg_counts = df_counts.groupby('typeOfContract')['count'].std().reset_index(name='average_count')

    # Merge the average counts back to the original dataframe
    df_counts = pd.merge(df_counts, df_avg_counts, on='typeOfContract')

    # Normalize the count by the average to get percentage
    df_counts['percentage'] = (df_counts['count'] / df_counts['average_count']) * 100

    # Use Seaborn's lineplot to plot multiple lines for each typeOfContract
    sns.lineplot(x='month', y='percentage', hue='typeOfContract', data=df_counts)

    plt.title('Average Distribution of Categories Across a Year')
    plt.xlabel('Month')
    plt.ylabel('Percentage')
    plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.savefig('figs/two_variables_award_dates/typeOfContract_by_award_dates_cyclic.png')
    #plt.show()
    
def execute_file():
    draw_quantitatives_by_date(df_Lots.copy())
    draw_quantitatives_by_date_cyclic_over_year(df_Lots.copy())
    draw_typeOfContracts_by_date_over_year(df_Lots.copy())
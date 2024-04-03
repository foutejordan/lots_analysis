import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import chi2_contingency
from sklearn.preprocessing import LabelEncoder
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

def clean_data(df_lots):
    """ Traitement variable 'accelerated' """

    df_lots = df_lots.drop(columns=['accelerated'])

    # loop to take the 2 first digits of the cpv code
    for i, row in df_lots.iterrows():
        if not pd.isna(row['cpv']):
            df_lots.at[i, 'cpv_name'] = str(row['cpv'])[:2]

    columns = df_lots.columns

    """
       ########################## Traitement des variables catégorielles ######œ##################
    """

    """ Traitement vairable 'cpv_name' """

    df_lots['cpv_name'] = df_lots['cpv_name'].fillna(np.random.choice(['45', '33'], p=[0.6, 0.4]))
    " enlever les lignes ou cpv_name est vide "


    """ Traitement vairable 'contractorSme' """

    for i, row in df_lots.iterrows():
        if not pd.isna(row['contractorSme']):
            df_lots.at[i, 'contractorSme'] = str(row['contractorSme'])[
                0]  # Remplacer les valeurs fausses par la première lettre de la valeur ( N ou Y) ou compter le nombre de N et Y et remplacer par la valeur la plus fréquente

    print("contractorSme",df_lots['contractorSme'].value_counts())

    """ Traitement vairable 'fraEstimated' """

    df_lots['fraEstimated'] = df_lots['fraEstimated'].fillna(
        'No')  # considerer les nan comme gagnant ne faisant pas partie des PME

    """ Traitement variable 'jointProcurement', 'onBehalf', 'multipleCae' """

    label_encoder_jointProcurement = LabelEncoder()
    label_encoder_onBehalf = LabelEncoder()
    label_encoder_multipleCae = LabelEncoder()

    label_encoder_jointProcurement.fit(df_lots.loc[:, 'jointProcurement'])
    label_encoder_onBehalf.fit(df_lots.loc[:, 'onBehalf'])
    label_encoder_multipleCae.fit(df_lots.loc[:, 'multipleCae'])

    df_lots['jointProcurement_encoded'] = label_encoder_jointProcurement.transform(df_lots['jointProcurement'])
    df_lots['onBehalf_encoded'] = label_encoder_onBehalf.transform(df_lots['onBehalf'])
    df_lots['multipleCae_encoded'] = label_encoder_multipleCae.transform(df_lots['multipleCae'])

    # replace impute_col_encoded 2 by NaN
    df_lots['jointProcurement_encoded'] = df_lots['jointProcurement_encoded'].replace(2, np.nan)
    df_lots['onBehalf_encoded'] = df_lots['onBehalf_encoded'].replace(2, np.nan)
    df_lots['multipleCae_encoded'] = df_lots['multipleCae_encoded'].replace(2, np.nan)

    # start imputer
    o_j_imputer = IterativeImputer(max_iter=10, random_state=0)

    o_j_imputer.fit(df_lots.loc[:, ['onBehalf_encoded', 'jointProcurement_encoded', 'multipleCae_encoded']])
    df_lots_imputed = o_j_imputer.transform(
        df_lots.loc[:, ['onBehalf_encoded', 'jointProcurement_encoded', 'multipleCae_encoded']])
    # replace with imputed values
    df_lots.loc[:, ['jointProcurement_encoded']] = df_lots_imputed[:, 1].round()
    df_lots.loc[:, ['onBehalf_encoded']] = df_lots_imputed[:, 0].round()
    df_lots.loc[:, ['multipleCae_encoded']] = df_lots_imputed[:, 2].round()
    # inverse transform
    joint_procurement_imputed = list(
        label_encoder_jointProcurement.inverse_transform(df_lots['jointProcurement_encoded'].round().astype('int')))
    df_lots['jointProcurement'] = joint_procurement_imputed

    on_behalf_imputed = list(
        label_encoder_onBehalf.inverse_transform(df_lots['onBehalf_encoded'].round().astype('int')))
    df_lots['onBehalf'] = on_behalf_imputed

    multiple_cae_imputed = list(
        label_encoder_multipleCae.inverse_transform(df_lots['multipleCae_encoded'].round().astype('int')))
    df_lots['multipleCae'] = multiple_cae_imputed

    """ Traitement vairable 'gpa', 'topType' using also column outOfDirectives """

    label_encoder_gpa = LabelEncoder()
    label_encoder_topType = LabelEncoder()
    label_encoder_outOfDirectives = LabelEncoder()

    label_encoder_gpa.fit(df_lots.loc[:, 'gpa'])
    label_encoder_topType.fit(df_lots.loc[:, 'topType'])
    label_encoder_outOfDirectives.fit(df_lots.loc[:, 'outOfDirectives'])

    df_lots['gpa_encoded'] = label_encoder_gpa.transform(df_lots['gpa'])
    df_lots['topType_encoded'] = label_encoder_topType.transform(df_lots['topType'])
    df_lots['outOfDirectives_encoded'] = label_encoder_outOfDirectives.transform(df_lots['outOfDirectives'])

    # replace impute_col_encoded 2 by NaN
    df_lots['gpa_encoded'] = df_lots['gpa_encoded'].replace(2, np.nan)
    df_lots['topType_encoded'] = df_lots['topType_encoded'].replace(9, np.nan)
    # start imputer

    g_t_imputer = IterativeImputer(max_iter=10, random_state=0)

    g_t_imputer.fit(df_lots.loc[:, ['gpa_encoded', 'topType_encoded', 'outOfDirectives_encoded']])
    df_lots_imputed = g_t_imputer.transform(
        df_lots.loc[:, ['gpa_encoded', 'topType_encoded', 'outOfDirectives_encoded']])
    # replace with imputed values
    df_lots.loc[:, ['gpa_encoded']] = df_lots_imputed[:, 0].round()
    df_lots.loc[:, ['topType_encoded']] = df_lots_imputed[:, 1].round()
    df_lots.loc[:, ['outOfDirectives_encoded']] = df_lots_imputed[:, 2].round()
    # inverse transform

    gpa_imputed = list(label_encoder_gpa.inverse_transform(df_lots['gpa_encoded'].round().astype('int')))
    df_lots['gpa'] = gpa_imputed

    topType_imputed = list(label_encoder_topType.inverse_transform(df_lots['topType_encoded'].round().astype('int')))
    df_lots['topType'] = topType_imputed

    """ Traitement variable 'renewal', 'subContracted' à l'aide de 'typeOfContract', 'fraAgreement' """

    label_encoder_renewal = LabelEncoder()
    label_encoder_subContracted = LabelEncoder()
    label_encoder_typeOfContract = LabelEncoder()
    label_encoder_fraAgreement = LabelEncoder()

    label_encoder_renewal.fit(df_lots.loc[:, 'renewal'])
    label_encoder_subContracted.fit(df_lots.loc[:, 'subContracted'])
    label_encoder_typeOfContract.fit(df_lots.loc[:, 'typeOfContract'])
    label_encoder_fraAgreement.fit(df_lots.loc[:, 'fraAgreement'])

    df_lots['renewal_encoded'] = label_encoder_renewal.transform(df_lots['renewal'])
    df_lots['subContracted_encoded'] = label_encoder_subContracted.transform(df_lots['subContracted'])
    df_lots['typeOfContract_encoded'] = label_encoder_typeOfContract.transform(df_lots['typeOfContract'])
    df_lots['fraAgreement_encoded'] = label_encoder_fraAgreement.transform(df_lots['fraAgreement'])

    df_lots['renewal_encoded'] = df_lots['renewal_encoded'].replace(2, np.nan)
    df_lots['subContracted_encoded'] = df_lots['subContracted_encoded'].replace(2, np.nan)
    # start imputer

    r_s_imputer = IterativeImputer(max_iter=10, random_state=0)

    r_s_imputer.fit(
        df_lots.loc[:, ['renewal_encoded', 'subContracted_encoded', 'typeOfContract_encoded', 'fraAgreement_encoded']])
    df_lots_imputed = r_s_imputer.transform(
        df_lots.loc[:, ['renewal_encoded', 'subContracted_encoded', 'typeOfContract_encoded', 'fraAgreement_encoded']])
    # replace with imputed values
    df_lots.loc[:, ['renewal_encoded']] = df_lots_imputed[:, 0].round()
    df_lots.loc[:, ['subContracted_encoded']] = df_lots_imputed[:, 1].round()
    # inverse transform

    renewal_imputed = list(label_encoder_renewal.inverse_transform(df_lots['renewal_encoded'].round().astype('int')))
    df_lots['renewal'] = renewal_imputed

    subContracted_imputed = list(
        label_encoder_subContracted.inverse_transform(df_lots['subContracted_encoded'].round().astype('int')))
    df_lots['subContracted'] = subContracted_imputed

    """ Traitement variable 'contractorSme' à l'aide de 'typeOfContract' et de 'cpv_name """

    label_encoder_contractorSme = LabelEncoder()
    label_encoder_typeOfContract = LabelEncoder()


    label_encoder_contractorSme.fit(df_lots.loc[:, 'contractorSme'])
    label_encoder_typeOfContract.fit(df_lots.loc[:, 'typeOfContract'])
    # cast cpv_name to int
    df_lots['cpv_name'] = df_lots['cpv_name'].astype(int)

    df_lots['contractorSme_encoded'] = label_encoder_contractorSme.transform(df_lots['contractorSme'])
    df_lots['typeOfContract_encoded'] = label_encoder_typeOfContract.transform(df_lots['typeOfContract'])

    print("contractorSme",df_lots['contractorSme'].value_counts(dropna=False))
    print("typeOfContract",df_lots['contractorSme_encoded'].value_counts(dropna=False))
    df_lots['contractorSme_encoded'] = df_lots['contractorSme_encoded'].replace(2, np.nan)
    # start imputer

    c_t_imputer = IterativeImputer(max_iter=10, random_state=0)

    c_t_imputer.fit(df_lots.loc[:, ['contractorSme_encoded', 'typeOfContract_encoded', 'cpv_name']])
    df_lots_imputed = c_t_imputer.transform(df_lots.loc[:, ['contractorSme_encoded', 'typeOfContract_encoded', 'cpv_name']])
    # replace with imputed values
    df_lots.loc[:, ['contractorSme_encoded']] = df_lots_imputed[:, 0].round()
    # inverse transform

    contractorSme_imputed = list(label_encoder_contractorSme.inverse_transform(df_lots['contractorSme_encoded'].round().astype('int')))
    df_lots['contractorSme'] = contractorSme_imputed


    """
        ###################### Traitement des variables Numériques  ##################
    """
    # Remplacer les outliers par la médiane
    columns_to_process = ['correctionsNb', 'numberTenders', 'numberTendersSme', 'awardEstimatedPrice', 'awardPrice',
                          'contractDuration', 'publicityDuration']
    for column in columns_to_process:
        df_lots[column] = pd.to_numeric(df_lots[column], errors='coerce')
        Q1 = df_lots[column].quantile(0.25)
        Q3 = df_lots[column].quantile(0.75)
        IQR = Q3 - Q1

        outliers_mask = (df_lots[column] < (Q1 - 1.5 * IQR)) | (df_lots[column] > (Q3 + 1.5 * IQR))
        median = df_lots[column].median()
        df_lots.loc[outliers_mask, column] = median
    # end

    for i, row in df_lots.iterrows():
        if pd.isna(row['awardEstimatedPrice']):
            df_lots.at[i, 'awardEstimatedPrice'] = row['awardPrice']
        if pd.isna(row['awardPrice']):
            df_lots.at[i, 'awardPrice'] = row['awardEstimatedPrice']
    # imputer awardEstimatedPrice and awardPrice by using iterative imputer with estimator = RandomForestRegressor

    print("start imputer")
    imputer_award = IterativeImputer(max_iter=10, random_state=0)
    imputer_award.fit(df_lots[['awardEstimatedPrice', 'awardPrice']])

    df_lots_imputed = imputer_award.transform(df_lots[['awardEstimatedPrice', 'awardPrice']])

    for i, column in enumerate(['awardEstimatedPrice', 'awardPrice']):
        nan_indices = df_lots[column].index[df_lots[column].isna()]
        # nan_indices_valid = nan_indices[nan_indices < len(df_lots_imputed[i])]
        df_lots.loc[nan_indices, column] = df_lots_imputed[i][nan_indices]

    df_lots[columns].to_csv('data/Lots_cleaned.csv', index=False)


    return df_lots[columns]


if __name__ == '__main__':
    df_lots = pd.read_csv('../data/Lots.csv', dtype=str)
    df_lots_leaned = clean_data(df_lots)
    print(df_lots_leaned.isna().sum())



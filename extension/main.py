
import pandas as pd

extended_agents = pd.read_csv('../data/extended_agents.csv')

if __name__ == '__main__':
    print("begin read stockEH.csv")
    data1 = pd.read_csv('/home/jordan/Documents/Avignon M2/Semestre 2/Application BI/stockEH.csv')

    print("begin read stockUnit.csv")
    data2 = pd.read_csv('/home/jordan/Documents/Avignon M2/Semestre 2/Application BI/stockUnit.csv') # 3 column extracted

    print("begin read stockE.csv")
    data3 = pd.read_csv('/home/jordan/Documents/Avignon M2/Semestre 2/Application BI/stockE.csv') # 3 column extracted

    data4 = pd.read_csv('/home/jordan/Documents/Avignon M2/Semestre 2/Application BI/stockUL.csv') # 2  column extracted ( sexe unité legale, catégorie d'entreprise: PME, autre)

    print("begin read Agents.csv")
    agents = pd.read_csv('../data/Agents.csv')

    # merge data1 and agents on the 'siret' column

    print("begin merge to historic establishment ")
    result = pd.merge(agents, data1, on='siret', how='left')

    # merge result and data2 on the 'siren' column

    print("begin merge to unit")
    extended_agents = pd.merge(result, data2, on='siren', how='left')

    # merge extended_agents and data3 on the 'siret' column

    print("begin merge to establishment")
    extended_agents = pd.merge(extended_agents, data3, on='siret', how='left')

    # merge extended_agents and data4 on the 'siren' column

    print("begin merge to legal unit")
    extended_agents = pd.merge(extended_agents, data4, on='siren', how='left')

    # save the result to a csv file

    print("begin save")

    extended_agents.to_csv('../data/extended_agents.csv', index=False)
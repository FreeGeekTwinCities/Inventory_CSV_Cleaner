# Overall, this is set up to take a .csv as either an argument or prompt response and save the cleaned version to "completeCSV.csv". 
# The current filter criteria for each row are: 
# 1. Row has visible = no -> remove
# 2. Row has stock = 0 or 'Unlimited' -> remove
# 3. Row is tagged with "Inventory Excluded" -> remove
#     (for other cases where we don't need to track it week to week)

from numpy import true_divide
import pandas as pd
import sys

# if filepath is passed as argument, use that, otherwise prompt for one
if len(sys.argv) == 2:
    filepath = sys.argv[1]
else:
    filepath = input("Please enter filepath of .csv to edit: ")

# add validation about csv filetypes only, maybe? 

# Open csv into dataframe(df) using pandas to manipulate
df = pd.read_csv(filepath, sep=',')

# for each row, transfer the "Visible" status, title, and product page to any null rows below it
copyforward = ('Title','Product Page','Visible')
for i in copyforward:
    df[i] = df[i].fillna(method = 'ffill')

# loop over all rows again, and remove row if visible = no OR stock = 0 or Unlimited
dropList = []
for i in range(0,len(df)):
    # T/F criteria to drop row:
    hidden = df.loc[i,'Visible']=='No'
    out = df.loc[i,'Stock']==0
    unlimited = df.loc[i,'Stock']=='Unlimited'

    # for tag filtering, have to explicitly cast tags as a string since NaN is apparently considered a float? Sorry for the janky workaround. 
    tags = str(df.loc[i,'Tags'])
    tagged = (tags.find("Inventory Excluded") != -1)
   
    #if any criteria are met, add to drop list.  
    if hidden or out or unlimited or tagged:
        dropList.append(i)

    # also check if on sale, replace regular price with sale price
    onSale = df.loc[i,'On Sale'] == 'Yes'
    currentPrice = df.loc[i,'Sale Price']
    if onSale:
        df.loc[i,'Price'] = currentPrice
# using a list to keep track of what to drop was done since trying to drop within the for loop is...no bueno
# I think drop() was changing len(df) and that was making things unhappy
df.drop(index = dropList, inplace = True)

# Sort primary: Product Page, secondary:SKU
df = df.sort_values(by = ['Product Page','SKU'])


# print to new CSV
df.to_csv('completeCSV.csv', columns = ['Product Page', 'Title','SKU','Stock','Price'])
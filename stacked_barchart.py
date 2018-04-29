import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('review_output_relative_big.csv')

#add month and year column
df['month'] = pd.to_datetime(df['review_date']).dt.month
df['year'] = pd.to_datetime(df['review_date']).dt.year

#limit the year of display due to the limit of amount of reviews scraped
df = df[df.year.isin([2015,2016,2017,2018])]

#format the month column for sorting convinience
df['month'] = df['month'].apply(lambda x: format (x,'02'))
df['yyyy-mm'] = df.year.astype(str)+'-'+df.month.astype(str)

#aggregate the count of different review ratings
new_df = df.groupby(['yyyy-mm','review_score'],as_index=False).agg({'review_title':'count'}).rename(columns={'review_title':'count'})

new_df=new_df.sort_values(by='yyyy-mm')
pivot_df = new_df.pivot(index='yyyy-mm', columns='review_score', values='count')

#plot the stacked bar chart
colors = ["#C70039", "#FF5733","#FFC300",'#DAF7A6','#27AE60']
pivot_df.loc[:,[1.0,2.0, 3.0,4.0,5.0]].plot.bar(stacked=True, color=colors, figsize=(10,7))
plt.title('Top of the Rock Observation Deck Review Rating Stacked Bar Chart',fontsize = 15)
plt.show()

#%matplotlib
import csv
import nltk
import pandas as pd
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud


##The code below is used to generate the Low Rating vs High Rating Words Frequency
##
f = open("review_output_relative_big.csv","rt",encoding = "utf-8")
reader = csv.reader(f)
header = next(reader)
##initialize sentiment analyzer

low_rating_reviews = ''
high_rating_reviews = ''

for record in reader:
    #take out the special characters can't be encoded into ascii
    clean_record = [item.encode('ascii','ignore').decode("utf-8") for item in record]
    rating_score = int(clean_record[5])
    if rating_score <= 2:
        low_rating_reviews += str(clean_record[6])
    if rating_score >= 4:
        high_rating_reviews += str(clean_record[6])
f.close()

fig = plt.figure(figsize=(14,5))
plt.title("Top of the Rock Observation Deck Review - Word Frequency",fontsize = 15, y = 0.9)
plt.axis('off')
fig.add_subplot(1,2,1)
world_cloud_low_rating = WordCloud(max_font_size=50).generate(low_rating_reviews)
plt.imshow(world_cloud_low_rating, interpolation="bilinear")
plt.title('Low Rating Words Cloud')
plt.axis('off')

fig.add_subplot(1,2,2)
world_cloud_high_rating = WordCloud(max_font_size=50).generate(high_rating_reviews)
high_rating = plt.imshow(world_cloud_high_rating, interpolation="bilinear")

plt.title('High Rating Words Cloud')
fig.tight_layout()
plt.axis("off")

plt.show()

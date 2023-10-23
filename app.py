from flask import Flask, request, render_template
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    # Get user data and make a df
    if request.method == 'POST':
    
    
        data={
            "Name":['User Req name'],
            "Rating":request.form['rating'],
            "Price Rs":[request.form.get('budget')],
            "RAM Gb":[request.form.get('ram')],
            "ROM Gb":[request.form.get('rom')],
            "Battery Mah":[request.form.get('battery')],
        }
    userDf=pd.DataFrame(data)

    # Read the dataset
    df=pd.read_csv('Mobile_phones_data.csv',encoding= 'unicode_escape')

    # Append the user data to the dataframe
    df=df.append(userDf, ignore_index=True)

    # Create a column which will contain all these features
    def combineFeatures(row):
        return str(row['Price Rs'])+" "+str(row['RAM Gb'])+" "+str(row['ROM Gb'])+str(row['Battery Mah'])+str(row['Color'])
    df["combinedFeatures"]=df.apply(combineFeatures, axis=1)

    # Calculate similarity scores
    cv=CountVectorizer()
    countMatrix=cv.fit_transform(df['combinedFeatures'])
    similar=cosine_similarity(countMatrix)
    similarPhones=list(enumerate(similar[-1]))
    sortedSimilarPhones=sorted(similarPhones, key=lambda x:x[1], reverse=True)

    # Get the top 5 recommended mobile phones
    recommended = []
    
    for phone in sortedSimilarPhones:
        if df.loc[phone[0], 'Name'] != 'User Req name':
            recommended.append({
                'name': df.loc[phone[0], 'Name'],
                'ram': str(df.loc[phone[0], 'RAM Gb']),
                'rom': str(df.loc[phone[0], 'ROM Gb']),
                'budget': df.loc[phone[0], 'Price Rs'],
                'rating': df.loc[phone[0], 'Rating'],
                'battery': str(df.loc[phone[0], 'Battery Mah']),
                'color': str(df.loc[phone[0], 'Color']),
                'selling_price': str(df.loc[phone[0], 'Selling Price']),
            })
            if len(recommended) == 5:
                print(recommended)
                break
    
    return render_template('rec2.html', recommended=recommended)

if __name__ == '__main__':
    app.run(debug=True)

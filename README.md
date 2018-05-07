# fuzzywuzzyStringCorrection-
Function used to correct misspelled values in a dataset


'If only the dataset was clean .....'. That's probably one of the most overheard statements that rattles through my head every time I'm working on a data science project. Or any other project that involves data for that matter. It's no secret! Following the proliferate availability of data storage and it's processing, data geeks like myself have seen some of the most oblivious and inconsistent datasets. 


While aggregating the data we collected from several different sources, my team and I, more often than common, hit a excessively irritating roadblock where we would find inconsistent data entry in string values. For example 'Bruce ' and 'bruce' or 'UC Cal' and 'U.C. Cal'. While these differences seem simple, they're such a hassle to deal with on a large scale. We found ourselves spending 3 or even 4 times the time clean the data, than actually using it to gain something useful. In this article I would like to share an approach I used as a workaround for this time consuming task.


The modules that will be used are 


pandas 

numpy 

fuzzywuzzy 


If you do not have fuzzywuzzy installed, just run 


pip install fuzzywuzzy 


The dataset I will use to demonstrate can be found here.



import pandas as pd 
import numpy as np
import fuzzywuzzy as fw 
After importing the libraries, just read the dataset as follows



df = pd.read_csv('PakistanSuicideAttacks Ver 11 (30-November-2017).csv') 
For the sake of keeping this simple, we'll only be working on one feature. However, the same process can be applied to any other feature with the similar problem. In fact, you should write your own function to deliberately edit the feature exactly the way you want it. Moving on, lets look at the 'City' feature in the dataset and it's unique values. 



cities = df['City'].unique()
cities.sort()
print cities
['ATTOCK' 'Attock ' 'Bajaur Agency' 'Bannu' 'Bhakkar ' 'Buner' 'Chakwal '
 'Chaman' 'Charsadda' 'Charsadda ' 'D. I Khan' 'D.G Khan' 'D.G Khan '
 'D.I Khan' 'D.I Khan ' 'Dara Adam Khel' 'Dara Adam khel' 'Fateh Jang'
 'Ghallanai, Mohmand Agency ' 'Gujrat' 'Hangu' 'Haripur' 'Hayatabad'
 'Islamabad' 'Islamabad ' 'Jacobabad' 'KURRAM AGENCY' 'Karachi' 'Karachi '
 'Karak' 'Khanewal' 'Khuzdar' 'Khyber Agency' 'Khyber Agency ' 'Kohat'
 'Kohat ' 'Kuram Agency ' 'Lahore' 'Lahore ' 'Lakki Marwat' 'Lakki marwat'
 'Lasbela' 'Lower Dir' 'MULTAN' 'Malakand ' 'Mansehra' 'Mardan'
 'Mohmand Agency' 'Mohmand Agency ' 'Mohmand agency'
 'Mosal Kor, Mohmand Agency' 'Multan' 'Muzaffarabad' 'North Waziristan'
 'North waziristan' 'Nowshehra' 'Orakzai Agency' 'Peshawar' 'Peshawar '
 'Pishin' 'Poonch' 'Quetta' 'Quetta ' 'Rawalpindi' 'Sargodha'
 'Sehwan town' 'Shabqadar-Charsadda' 'Shangla ' 'Shikarpur' 'Sialkot'
 'South Waziristan' 'South waziristan' 'Sudhanoti' 'Sukkur' 'Swabi '
 'Swat' 'Swat ' 'Taftan' 'Tangi, Charsadda District' 'Tank' 'Tank '
 'Taunsa' 'Tirah Valley' 'Totalai' 'Upper Dir' 'Wagah' 'Zhob' 'bannu'
 'karachi' 'karachi ' 'lakki marwat' 'peshawar' 'swat']

As you can see 'ATTOCK' and 'Attock ' or 'Charsadda' and 'Charsadda ' are essentially the same but because of minor string misplacements, they're read differently. 


 Before going any further, lets get a count of the unique values, and compare that number along the way. 



len(df['City'].unique())
93
Keep that number in mind, 93! That's 93 different values in one feature. 



df['City'] = df['City'].str.lower()
df['City'] = df['City'].str.strip()
The two above commands will turn all of the values into lowercase and eliminate any whitespace. Lets look at the number of unique values now. 



len(df['City'].unique())
67
Alright, now lets use the power of FuzzyWuzzy to do the rest.




matches = fuzzywuzzy.process.extract('Kuram Agency', cities, limit=10, scorer = fuzzywuzzy.fuzz.token_sort_ratio)

In the above command I've asked fuzzy to extract any string that matches a similarity of 'Kuram Agency'. Let's take a look at the results. 


[('Kuram Agency ', 100),
 ('KURRAM AGENCY', 96),
 ('Bajaur Agency', 72),
 ('Khyber Agency', 72),
 ('Khyber Agency ', 72),
 ('Orakzai Agency', 69),
 ('Mohmand Agency', 62),
 ('Mohmand Agency ', 62),
 ('Mohmand agency', 62),
 ('Mosal Kor, Mohmand Agency', 61)]
The results show two matches with a high score. The scores resemble the probability of a correct match. 



matches = fuzzywuzzy.process.extract('Mohmand Agency', cities, limit=10, scorer = fuzzywuzzy.fuzz.token_sort_ratio)
Looking at another example 'Mohmand Agency', you can see that there are three 100 percent matches. Also, another two matches in which the string at hand is a part of the string. 



Sometimes in cases like these, you need some domain knowledge. Is this a spelling mistake or this correct. In this case, I did the research, Ghallani and Mosal Kor are in Mohmand Agency. Therefore they're correct. 



[('Mohmand Agency', 100),
 ('Mohmand Agency ', 100),
 ('Mohmand agency', 100),
 ('Ghallanai, Mohmand Agency ', 74),
 ('Mosal Kor, Mohmand Agency', 74),
 ('Orakzai Agency', 64),
 ('Kuram Agency ', 62),
 ('Bajaur Agency', 59),
 ('KURRAM AGENCY', 59),
 ('Khyber Agency', 59)]
The point I wanted to make by the last example is that fuzzywuzzy is a tool to help you. With that being said, I wouldn't rely on it completely. Always take a look.



If it's not automated, it's not cool 


That's just one of my opinions for most processes, so I wrote a function to run the previous function for each string of a designated column. Take a look. 



def replaceMatches(df, column, minRatio=90):

    #get a list of the unique strings 

    strings = df[column].unique()

    

    for word in strings:

        matches = fuzzywuzz(word, strings)

        closeMatches = closeMatches = [matches[0] for matches in matches if matches[1] >= minRatio]

        rowsWithMatches = df[column].isin(closeMatches)

        df.loc[rowsWithMatches, column] = word

        

    newCol = df[column].unique()

    newCol.sort()

    return newCol

        

        

def fuzzywuzz(word, strings):

    return fuzzywuzzy.process.extract(word, strings, limit = 10, scorer = fuzzywuzzy.fuzz.token_sort_ratio)



Now if we run it like this. 



uniqueMatches = replaceMatches(df=df, column='City')
and print it 


['attock' 'bajaur agency' 'bannu' 'bhakkar' 'buner' 'chakwal' 'chaman'
 'charsadda' 'd. i khan' 'd.g khan' 'dara adam khel' 'fateh jang'
 'ghallanai, mohmand agency' 'gujrat' 'hangu' 'haripur' 'hayatabad'
 'islamabad' 'jacobabad' 'karachi' 'karak' 'khanewal' 'khuzdar'
 'khyber agency' 'kohat' 'kurram agency' 'lahore' 'lakki marwat' 'lasbela'
 'lower dir' 'malakand' 'mansehra' 'mardan' 'mohmand agency'
 'mosal kor, mohmand agency' 'multan' 'muzaffarabad' 'north waziristan'
 'nowshehra' 'orakzai agency' 'peshawar' 'pishin' 'poonch' 'quetta'
 'rawalpindi' 'sargodha' 'sehwan town' 'shabqadar-charsadda' 'shangla'
 'shikarpur' 'sialkot' 'south waziristan' 'sudhanoti' 'sukkur' 'swabi'
 'swat' 'taftan' 'tangi, charsadda district' 'tank' 'taunsa'
 'tirah valley' 'totalai' 'upper dir' 'wagah' 'zhob']

Get the length too



len(uniqueMatches)
65
So it eliminated another two, which may seem like a low number compared to previous operations. But if you know anything about EDA, you'll know that's crucial.



Hope this helps! 



Github code here!






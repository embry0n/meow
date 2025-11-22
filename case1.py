import pandas as pd

#
#посещение подготовительных курсов повышает результаты экзаменов у абитуриентов из семей,
#где оба родителя не имеют высшего образования.
#

df = pd.read_csv('StudentsPerformance .csv') # Чтение CSV-файла в DataFrame

# уникальное число родителей по образованию
print(df['parental level of education'].value_counts())

# кол-во от 40 до 60 по матану
print(df[(df['math score'] > 40) & (df['math score'] < 60)]['math score'].count())

# кол-во студентов с род без обр и от 40 до 60 по матану
print(df[(df['math score'] > 40) & (df['math score'] < 60) & (df['parental level of education'] == 'some high school')]['math score'].count())
print(df[(df['math score'] > 40) & (df['math score'] < 60) & (df['parental level of education'] == 'some high school')]['math score'].count())

#reading score
print(df[(df['reading score'] > 40) & (df['reading score'] < 60) & (df['parental level of education'] == 'high school')]['reading score'].count())
print(df[(df['reading score'] > 40) & (df['reading score'] < 60) & (df['parental level of education'] == 'some high school')]['reading score'].count())

# writing score
print(df[(df['writing score'] > 40) & (df['writing score'] < 60) & (df['parental level of education'] == 'high school')]['writing score'].count())
print(df[(df['writing score'] > 40) & (df['writing score'] < 60) & (df['parental level of education'] == 'some high school')]['writing score'].count())

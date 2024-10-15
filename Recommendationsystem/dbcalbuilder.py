 # Load the dataset
import pandas as pd
import pymysql
df = pd.read_csv(r"C:/diet_Recommendation (2)/diet_Recommendation/diet/Recommendationsystem/dataset/IndianFoodDatasetXLSFinal (3).csv", encoding='unicode_escape')
con=pymysql.connect(host="localhost",user="root",password="root",database="diet")
menu=df['name']
cal=df['totalCaloriesInCal']
print(menu.head())
print(cal.head())
cur=con.cursor()
for i in range(len(menu)):
    sql="INSERT INTO cal(menu,cal) VALUES (%s,%s)";
    values=(menu[i],cal[i])
    cur.execute(sql,values)
    con.commit()
    


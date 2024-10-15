from django.shortcuts import render
import pymysql

con=pymysql.connect(host="localhost",user="root",password="root",database="diet")

def prediction(request):
    return render(request,"prediction.html")
def analyze(request):
    return render(request,"analyze.html")

def about(request):
    return render(request,"aboutUs.html")
def home(request):
    return render(request,"home.html")

def about_developer(request):
    return render(request,"aboutdevelope.html")

def login(request):
    return render(request,"login.html")

def logout(request):
    return render(request,"login.html")

def register(request):
    return render(request,"register.html")

def doregister(request):
    name=request.POST.get('uname')
    cnumber=request.POST.get('cno')
    email=request.POST.get('email')
    password=request.POST.get('password')
    sql="INSERT INTO userdata(name,contact,email,password) VALUES (%s,%s,%s,%s)";
    values=(name,cnumber,email,password)
    cur=con.cursor()
    cur.execute(sql,values)
    con.commit()
    return render(request,"login.html")

def myprofile(request):
    content={}
    payload=[]
    uid=request.session['uid']
    q1="select * from userdata where uid=%s";
    values=(uid)
    cur=con.cursor()
    cur.execute(q1,values)
    res=cur.fetchall()
    for x in res:
        content={'name':x[0],"contact":x[1],"email":x[2]}
        payload.append(content)
        content={}
    return render(request,"myprofile.html",{'list': {'items':payload}})




def prevpred(request):
    content={}
    payload=[]
    uid=request.session['uid']
    q1="select * from smp where uid=%s";
    values=(uid)
    cur=con.cursor()
    cur.execute(q1,values)
    res=cur.fetchall()
    for x in res:
        content={'n':x[0],"g":x[1],"a":x[2],"c":x[3],'age':x[4],"height":x[5],"weight":x[6],"act":x[7],"bmi":x[8],"cal":x[9],"bmr":x[10],"pred":x[11],"dpred":x[13]}
        payload.append(content)
        content={}
    return render(request,"prevpred.html",{'list': {'items':payload}})

    

def dologin(request):
    sql="select * from userdata";
    cur=con.cursor()
    cur.execute(sql)
    data=cur.fetchall()
    email=request.POST.get('email')
    password=request.POST.get('password')
    name="";    
    uid="";
    isfound="0";
    content={}
    payload=[]
    print(email)
    print(password)
    if(email=="admin" and password=="admin"):
        print("print")
        return render(request,"admindashboard.html")
    else:
        for x in data:
            if(x[2]==email and x[3]==password):
                request.session['uid']=x[4]
                request.session['name']=x[0]
                request.session['contact']=x[1]
                request.session['email']=x[2]
                request.session['pass']=x[3]
                isfound="1"
        if(isfound=="1"):
             return render(request,"home.html")
        else:
             return render(request,"error.html")

def calculate_bmi_and_calories(height, weight, age, gender, activity_level):
    # Calculate BMI
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    bmi = round(bmi, 2)

    # Calculate BMR
    if gender == 'male':
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

    # Calculate calories
    if activity_level == 'sedentary':
        calories = bmr * 1.2
    elif activity_level == 'lightly_active':
        calories = bmr * 1.375
    elif activity_level == 'moderately_active':
        calories = bmr * 1.55
    elif activity_level == 'very_active':
        calories = bmr * 1.725
    else:
        calories = bmr * 1.9

    return {'bmi': bmi}


def bmical(request):
    global height,weight,age,gender,activity_level
    import pandas as pd
    from sklearn.tree import DecisionTreeClassifier

    # Load the dataset
    df = pd.read_csv(r"C:/diet_Recommendation (2)/diet_Recommendation/diet/Recommendationsystem/dataset/IndianFoodDatasetXLSFinal (3).csv", encoding='unicode_escape')


    # Preprocess the dataset
    df.drop(['foodID', 'URL', 'imgURL', 'instructions'], axis=1, inplace=True)
    df.drop_duplicates(inplace=True)
    df.fillna(df.mode().iloc[0], inplace=True)
    if request.method == 'POST':
        try:
            name=request.POST.get("name")
            address=request.POST.get("address")
            contact=request.POST.get("contact")
            height = int(request.POST.get('height'))
            weight = int(request.POST.get('weight'))
            age = int(request.POST.get('age'))
            gender = request.POST.get('gender')
            print(gender)
            activity_level = request.POST.get('activity_level')
        except:
            pass

        
        activity_factor = 1.2
        
       
        if gender == 'm':
            desired_calorie_intake = 2500
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            print(bmr)
        else:
            desired_calorie_intake = 2000
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            print(bmr)

        tdee = bmr * activity_factor
        print("calories",tdee)
        calories_to_burn=tdee-desired_calorie_intake
        calories_to_burn=calories_to_burn * (-1)
        print(calories_to_burn)
        # Convert calories_to_burn to a list or a 2D array-like input
        #calories_to_burn = [[calories_to_burn_1], [calories_to_burn_2], [calories_to_burn_3], [calories_to_burn_4Filter the dataset based on the number of calories to burn
        df_filtered = df[df['totalCaloriesInCal'] <= calories_to_burn]

        # Train the decision tree classifier
        features = df_filtered[[ 'totalCaloriesInCal']]
        target = df_filtered['name']
        dt = DecisionTreeClassifier()
        dt.fit(features, target)
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)


        # Predict the recommended food
        prediction = dt.predict([[calories_to_burn]])
        # Modify the input data for prediction
        #prediction = dt.predict(features)
        print(prediction[0])
        y_pred = dt.predict(X_test)
        from sklearn.metrics import confusion_matrix, classification_report
        cm = confusion_matrix(y_test, y_pred)
        print(cm)
        # Compute precision, recall, and F1-score
        report = classification_report(y_test, y_pred)
        #print('Classification report:')
        #print(report)


        result = calculate_bmi_and_calories(height, weight, age, gender, activity_level)
        content={}
        payload=[]


        bmi = result['bmi']
        pred=prediction[0]
        pred1=y_pred[1]
        pred2=y_pred[2]
        pred3=y_pred[3]
        pred4=y_pred[4]
        pred5=y_pred[5]
        # Convert predictions into strings
        pred = str(pred)
        pred1 = str(pred1)
        pred2 = str(pred2)
        pred3 = str(pred3)
        # Concatenate the predictions with a separator
        separator = ', '  # Choose the separator you want, e.g. comma + space
        pred = separator.join([pred,pred1, pred2, pred3])

        pred4 = str(pred4)
        pred5 = str(pred5)
        # Concatenate the predictions with a separator
        separator = ', '  # Choose the separator you want, e.g. comma + space
        dpred = separator.join([pred4, pred5])
        q1="select * from cal";
        cur=con.cursor()
        cur.execute(q1)
        res=cur.fetchall()
        # Create an empty list to store the payload
        payload = []
        calor = {pred: pred,pred1: pred1,pred2: pred2,pred3: pred3}
        # Iterate through the fetched rows
        for x in res:
            menu = x[1]  
            cal = x[2]
            # Check if the 'menu' value is present in the 'calories_map' dictionary
            if menu in calor:
                # Get the corresponding calorie value from the 'calories_map' dictionary
                cal = x[2]
                # Append the menu and calorie values to the payload list
                payload.append({'menu': menu, 'cal': cal})

        calor2 = {pred4: pred4,pred5: pred5}
        # Create an empty list to store the payload
        lst = []
        # Iterate through the fetched rows
        for x in res:
            menu = x[1]  
            cal = x[2]
            # Check if the 'menu' value is present in the 'calories_map' dictionary
            if menu in calor2:
                # Get the corresponding calorie value from the 'calories_map' dictionary
                cal = x[2]
                # Append the menu and calorie values to the payload list
                lst.append({'menu': menu, 'cal': cal})
                print(lst)
        #pred = separator.join(payload)
        import random
        lst11 = ['Oranges (80 cal))', 'Cherries (60 cal)', 'Kiwi (54 cal)', 'Peaches (50 cal)', 'Apple (60 cal)']  
        random_element = random.choice(lst11)
        lst12 = ['Sprouts (16 cal)', 'Oats (150 cal)', 'FoxNut (200 cal)', 'MixNuts (300 cal)','Yoghurt (59 cal)','Dry Fruits(200 cal)']
        random.shuffle(lst12)  # Shuffle the list in place
        random_element1 = lst12[:3]
        random_element1 = ', '.join(random_element1)
        

        bmr=bmr
        caloriesToBurn= calories_to_burn

        #Pass the bmi and calories values to the template continueext
        context = {'bmi': bmi, 'calories_need': tdee, 'bmr': bmr ,'random_element':random_element,'random_element1':random_element1, 'payload':payload,'lst':lst, 'burn':caloriesToBurn}

        #context = {'bmi': bmi, 'calories_need': tdee, 'bmr': bmr ,'random_element':random_element,'random_element1':random_element1, 'pred':pred,'pred1':pred1,'pred2':pred2,'pred3':pred3,'pred4':pred4,'pred5':pred5, 'burn':caloriesToBurn}
        uid=request.session['uid']
        #,bmi,cal,bmr,pred,uid ,str(height),str(weight),str(bmi),str(tdee),str(bmr),str(pred),str(uid)
        sql="INSERT INTO smp(name,gender,address,contact,age,height,weight,activity,bmi,cal,bmr,pred,uid,dpred) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        values=(str(name),str(gender),str(address),str(contact),str(age),str(height),str(weight),str(activity_level),str(bmi),str(tdee),str(bmr),str(pred),str(uid),str(dpred))
        cur=con.cursor()
        cur.execute(sql,values)
        con.commit()
        
        print(context)
        return render(request, 'analyze.html',context)

    else:
        return render(request, 'login.html')


def admindashboard(request):
    return render(request,"admindashboard.html")

def viewprediction(request):
    content={}
    payload=[]
    q1="select * from smp";
    cur=con.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        content={'n':x[0],"g":x[1],"a":x[2],"c":x[3],'age':x[4],"height":x[5],"weight":x[6],"act":x[7],"bmi":x[8],"cal":x[9],"bmr":x[10],"pred":x[11],"dpred":x[13]}
        payload.append(content)
        content={}
    return render(request,"viewprediction.html",{'list': {'items':payload}})


def viewuser(request):
    content={}
    payload=[]
    q1="select * from userdata";
    cur=con.cursor()
    cur.execute(q1)
    res=cur.fetchall()
    for x in res:
        content={'name':x[0],"contact":x[1],"email":x[2]}
        
        payload.append(content)
        content={}
    return render(request,"viewprofile.html",{'list': {'items':payload}})

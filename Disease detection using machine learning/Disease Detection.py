
# Importing the libraries
from tkinter import *
from tkinter import messagebox
import pyttsx3
import datetime
import speech_recognition as sr
import os            
import webbrowser

import numpy as np
import pandas as pd

print('warming up my vocal cords!')
allData=""
username1=""

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')

def speak(text):
    engine.say(text)
    engine.runAndWait()

#Greeting by the chat bot
def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
    speak("I am your personal assistant and I'll try to help you identify what disease you may have based on your symptoms, but there is no surity of that as it is only prediction. I will also try to recommend some expert doctors for the predicted disease. Please consult the doctor before starting the treatment of the disease. But first we let's start by logging in or by registering.")

#Recognise user's voice and get the input
#def takeCommand():
#    r=sr.Recognizer()
#    with sr.Microphone() as source:
#        print("Listening...")

#        audio=r.listen(source)


#        try:
#            statement=r.recognize_google(audio,language='en-in')
#            print(f"user said:{statement}\n")

#        except Exception as e:
#            speak("Pardon me, please say that again")
#            return "None"
#        return statement



class HyperlinkManager:
      
    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

# Importing the dataset
training_dataset = pd.read_csv('Training.csv')
test_dataset = pd.read_csv('Testing.csv')

# Slicing and Dicing the dataset to separate features from predictions
X = training_dataset.iloc[:, 0:132].values
Y = training_dataset.iloc[:, -1].values

# Dimensionality Reduction for removing redundancies
dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

# Encoding String values to integer constants
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
y = labelencoder.fit_transform(Y)

# Splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Implementing the Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)

# Saving the information of columns
cols= training_dataset.columns
cols= cols[:-1]

# Checking the Important features
importances = classifier.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

#y_pred=classifier.predict(X_test)
#from sklearn.metrics import r2_score
#print(r2_score(y_test,y_pred))

text_representation = tree.export_text(classifier)
print(text_representation)

#Saving the Decision tree as an image file
#from six import StringIO
#from IPython.display import Image
#from sklearn.tree import export_graphviz
#import pydotplus
#dot_data=StringIO()
#export_graphviz(classifier,out_file=dot_data,
#               filled=True,rounded=True,
#               special_characters=True)
#graph=pydotplus.graph_from_dot_data(dot_data.getvalue())
#Image(graph.create_png())

wishMe()

# Implementing the Visual Tree
from sklearn.tree import _tree

# Method to simulate the working of a Chatbot by extracting and formulating questions
def print_disease(node):
        node = node[0]
        val  = node.nonzero()
        disease = labelencoder.inverse_transform(val[0])
        return disease
def recurse(node, depth):
            global val,ans
            global tree_,feature_name,symptoms_present
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                yield name + " ?"

                ans = ans.lower()
                if ans == 'yes':
                    val = 1
                else:
                    val = 0
                if  val <= threshold:
                    yield from recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    yield from recurse(tree_.children_right[node], depth + 1)
            else:
                allData=""
                strData=""
                present_disease = print_disease(tree_.value[node])
                strData="You may have :" +  str(present_disease)
                speak(strData)
               
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                
                red_cols = dimensionality_reduction.columns 
                symptoms_given = red_cols[dimensionality_reduction.loc[present_disease].values[0].nonzero()]
                strData="symptoms present:  " + str(list(symptoms_present))
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')
                strData="symptoms that may appear: "  +  str(list(symptoms_given))
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                confidence_level = (1.0*len(symptoms_present))/len(symptoms_given)
                strData="confidence level is: " + str(confidence_level)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')
                strData='The model suggests:'
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')                  
                row = doctors[doctors['disease'] == present_disease[0]]
                strData='Consult '+ str(row['name'].values)
                QuestionDigonosis.objRef.txtDigonosis.insert(END,str(strData)+'\n')
                speak("We recommend you to visit any doctor nearby. We suggest "+str(row['name'].values)+" specialist doctor for your convenience. The link for the details for the specialist doctor will appear now.")
                hyperlink = HyperlinkManager(QuestionDigonosis.objRef.txtDigonosis)
                strData='Visit '+ str(row['link'].values[0])
                def click1():
                    webbrowser.open_new(str(row['link'].values[0]))
                QuestionDigonosis.objRef.txtDigonosis.insert(INSERT, strData, hyperlink.add(click1))
                allData=QuestionDigonosis.objRef.txtDigonosis.get("1.0",'end-1c')
                file2 = open(username1, "a")
                file2.write("\n"+allData + "\n")
                file2.close()
                yield strData
        
def tree_to_code(tree, feature_names):
        global tree_,feature_name,symptoms_present
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]
        symptoms_present = []

def execute_bot():
    tree_to_code(classifier,cols)

doc_dataset = pd.read_csv('doctors_dataset.csv', names = ['Name', 'Description'])

diseases = dimensionality_reduction.index
diseases = pd.DataFrame(diseases)

doctors = pd.DataFrame()
doctors['name'] = np.nan
doctors['link'] = np.nan
doctors['disease'] = np.nan

doctors['disease'] = diseases['prognosis']

doctors['name'] = doc_dataset['Name']
doctors['link'] = doc_dataset['Description']

record = doctors[doctors['disease'] == 'AIDS']
record['name']
record['link']

class QuestionDigonosis(Frame):
    main_Root=None
    objIter=None
    objRef=None
    def __init__(self,master=None):
        QuestionDigonosis.main_Root=master
        QuestionDigonosis.objRef=self
        super().__init__(master=master)
        master.geometry("900x430")
        master.title("Symptoms identification and disease prediction")
        self["bg"]="Black"
        self.createWidget()
        self.iterObj=None

    def createWidget(self):
        self.lblQuestion=Label(self,text="Question",width=12,bg="Grey")
        self.lblQuestion.grid(row=0,column=0,rowspan=4)

        self.lblDigonosis = Label(self, text="Digonosis",width=12,bg="Grey")
        self.lblDigonosis.grid(row=4, column=0,sticky="n",pady=5)

        self.txtQuestion = Text(self, width=100,height=4)
        self.txtQuestion.grid(row=0, column=1,rowspan=4,columnspan=20)

        self.varDiagonosis=StringVar()
        self.txtDigonosis =Text(self, width=100,height=14)
        self.txtDigonosis.grid(row=4, column=1,columnspan=20,rowspan=20,pady=5)

        self.btnNo=Button(self,text="No",width=12,bg="Yellow", command=self.btnNo_Click)
        self.btnNo.grid(row=25,column=0)
        self.btnYes = Button(self, text="Yes",width=12,bg="Yellow", command=self.btnYes_Click)
        self.btnYes.grid(row=25, column=1,columnspan=20,sticky="e")

        self.btnClear = Button(self, text="Clear",width=12,bg="Yellow", command=self.btnClear_Click)
        self.btnClear.grid(row=27, column=0)
        self.btnStart = Button(self, text="Start",width=12,bg="Yellow", command=self.btnStart_Click)
        self.btnStart.grid(row=27, column=1,columnspan=20,sticky="e")

        self.btnLogOut = Button(self, text="Log Out", width=12, bg="Yellow", command=self.btnLogOut_Click)
        self.btnLogOut.grid(row=27, column=1, columnspan=10, stick="e")
        self.btnQuit=Button(self, text="Quit", width=12, bg="Yellow", command=self.btnQuit_Click2)
        self.btnQuit.grid(row=32,column=1,columnspan=10,sticky="e")
    def btnNo_Click(self):
        global val,ans
        global val,ans
        ans='no'
        str1=QuestionDigonosis.objIter.__next__()
        self.txtQuestion.delete(0.0,END)
        self.txtQuestion.insert(END,str1+"\n")
        
    def btnYes_Click(self):
        global val,ans
        ans='yes'
        self.txtDigonosis.delete(0.0,END)
        str1=QuestionDigonosis.objIter.__next__()

    def btnClear_Click(self):
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
    def btnStart_Click(self):
        execute_bot()
        self.txtDigonosis.delete(0.0,END)
        self.txtQuestion.delete(0.0,END)
        self.txtDigonosis.insert(END,"Please Click on Yes or No for the Above symptoms in Question")                  
        QuestionDigonosis.objIter=recurse(0, 1)
        str1=QuestionDigonosis.objIter.__next__()
        self.txtQuestion.insert(END,str1+"\n")
    def btnQuit_Click2(self):
        speak("Thankyou for making me useful")
        self.destroy()
        root.destroy()
    def btnLogOut_Click(self):
        speak("Logging you out")
        self.destroy()
        HomeFromQuestionDigonosis=HomePage(QuestionDigonosis.main_Root)
        HomeFromQuestionDigonosis.pack()

class HomePage(Frame):
    main_Root = None
    def destroyPackWidget(self, parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        HomePage.main_Root = master
        super().__init__(master=master)
        master.geometry("300x300")
        master.title("Home Page")
        master.configure(bg="Black")
        self.createWidget()

    def createWidget(self):
        self.configure(bg="Black")
        self.lblMsg=Label(self, text="Disease Detection Chatbot", bg="Yellow", width="300", height="2", font=("Calibri", 15))
        self.lblMsg.pack(pady=20)
        self.btnLogin=Button(self, text="Login",bg="Yellow", height="2", width="300", command = self.lblLogin_Click)
        self.btnLogin.pack()
        self.btnRegister=Button(self, text="Register",bg="Yellow", height="2", width="300", command = self.btnRegister_Click)
        self.btnRegister.pack()
        self.btnQuit=Button(self,text="Quit",bg="Yellow",height="2",width="200",command=self.btnQuit_Click)
        self.btnQuit.pack(padx=0,pady=20)

    def lblLogin_Click(self):
        self.destroyPackWidget(HomePage.main_Root)
        frmLogin=Login(HomePage.main_Root)
        frmLogin.pack()
        frmLogin.update()
        speak("You have clicked on the login button. Here, please enter the username and the password that you chose while signing up. If you don't remember the login credentials then click on the back button and register again.")
    def btnRegister_Click(self):
        self.destroyPackWidget(HomePage.main_Root)
        frmSignUp = SignUp(HomePage.main_Root)
        frmSignUp.pack()
        frmSignUp.update()
        speak("You have clicked on the register button. Please enter the username and password that you wish to use to login. If you alreay have an account, then click on the back button and login with those credentials.")
    def btnQuit_Click(self):
        speak("Thankyou for making me useful")
        self.destroyPackWidget(HomePage.main_Root)
        root.destroy()

class Login(Frame):
    main_Root=None
    def destroyPackWidget(self,parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        Login.main_Root=master
        super().__init__(master=master)
        master.title("Login")
        master.geometry("300x300")
        self.createWidget()
    def createWidget(self):
        self.configure(bg="Black")
        self.lblMsg=Label(self, text="Please enter details below to login",bg="yellow")
        self.lblMsg.pack()
        self.username=Label(self, text="Username * ",fg="Yellow",bg="Black")
        self.username.pack()
        self.username_verify = StringVar()
        self.username_login_entry = Entry(self, textvariable=self.username_verify)
        self.username_login_entry.pack()
        self.password=Label(self, text="Password * ",fg="Yellow", bg="Black")
        self.password.pack()
        self.password_verify = StringVar()
        self.password_login_entry = Entry(self, textvariable=self.password_verify, show='*')
        self.password_login_entry.pack()
        self.btnLogin=Button(self, text="Login", width=10, height=1,bg="Yellow", command=self.btnLogin_Click)
        self.btnLogin.pack(pady=15)
        self.btnLoginBack=Button(self,text="Back",width=10, height=1,bg="Yellow", command=self.btnLoginBack_Click)
        self.btnLoginBack.pack()
    def btnLogin_Click(self):
        global username1
        username1 = self.username_login_entry.get()
        password1 = self.password_login_entry.get()

        list_of_files = os.listdir()
        if username1 in list_of_files:
            file1 = open(username1, "r")
            verify = file1.read().splitlines()
            if password1 in verify:
                messagebox.showinfo("Sucess","Login Sucessful")
                self.destroyPackWidget(Login.main_Root)
                frmQuestion = QuestionDigonosis(Login.main_Root)
                frmQuestion.pack()
                frmQuestion.update()
                speak("Now that you have successfully logged in, we can start the disease diagnosis. First click on the start button on the right to start the process. I will ask for a symptom. If you feel that you have that, then click on the yes button on the right. Else click on the no button on the left. To reset the process, click on the clear button below the no button. Finally click on the log out button to go back to the home page and quit button to quit the program.")
            else:
                messagebox.showinfo("Failure", "Login Details are wrong try again")
        else:
            messagebox.showinfo("Failure", "User not found try from another user\n or sign up for new user")
    def btnLoginBack_Click(self):
        self.destroyPackWidget(Login.main_Root)
        HomeFromLogin=HomePage(Login.main_Root)
        HomeFromLogin.pack()

class SignUp(Frame):
    main_Root=None
    def destroyPackWidget(self,parent):
        for e in parent.pack_slaves():
            e.destroy()
    def __init__(self, master=None):
        SignUp.main_Root=master
        master.title("Register")
        super().__init__(master=master)
        master.geometry("300x300")
        self.createWidget()
    def createWidget(self):
        self.configure(bg="Black")
        self.lblMsg=Label(self, text="Please enter details below", bg="yellow")
        self.lblMsg.pack()
        self.username_lable = Label(self, text="Username * ",bg="Black",fg="Yellow")
        self.username_lable.pack()
        self.username = StringVar()
        self.username_entry = Entry(self, textvariable=self.username)
        self.username_entry.pack()

        self.password_lable = Label(self, text="Password * ",bg="Black",fg="Yellow")
        self.password_lable.pack()
        self.password = StringVar()
        self.password_entry = Entry(self, textvariable=self.password, show='*')
        self.password_entry.pack()
        self.btnRegister=Button(self, text="Register", width=10, height=1, bg="Yellow", command=self.register_user)
        self.btnRegister.pack(pady=15)
        self.btnRegisterBack=Button(self, text="Back", width=10,height=1, bg="Yellow", command=self.register_back)
        self.btnRegisterBack.pack()

    def register_user(self):
        global username1
        file = open(self.username_entry.get(), "w")
        file.write(+self.username_entry.get() + "\n")
        file.write(self.password_entry.get()+"\n\n"+"History\n")
        file.close()
        username1=self.username_entry.get()
        self.destroyPackWidget(SignUp.main_Root)
        
        self.lblSucess=Label(root, text="Registration Success", fg="green", font=("calibri", 11))
        self.lblSucess.pack()
        
        self.btnSucess=Button(root, text="Click Here to proceed", command=self.btnSucess_Click, bg="Yellow")
        self.btnSucess.pack(pady=120)
    def btnSucess_Click(self):

        self.destroyPackWidget(SignUp.main_Root)
        frmQuestion = QuestionDigonosis(SignUp.main_Root)
        frmQuestion.pack()
        frmQuestion.update()
        speak("Now that you have successfully registered, we can start the disease diagnosis. First click on the start button on the right to start the process. I will ask for a symptom. If you feel that you have that, then click on the yes button on the right. Else click on the no button on the left. To reset the process, click on the clear button below the no button. Finally click on the log out button to go back to the home page and quit button to quit the program.")

    def register_back(self):
        self.destroyPackWidget(SignUp.main_Root)
        HomeFromRegister=HomePage(SignUp.main_Root)
        HomeFromRegister.pack()

root = Tk()

frmHomePage=HomePage(root)
frmHomePage.pack()
frmHomePage.update()
speak("The home page for the chatbot has been opened. There, click on Log in if you are already a user. Click on register if you have never logged in before. If you does not want to use the chatbot anymore, then click on the Quit button")
root.mainloop()
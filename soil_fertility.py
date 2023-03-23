import streamlit as st
import pickle
import base64
import pandas as pd

st.set_page_config(page_title="Soil fertility",page_icon="🌱")


            
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img = get_img_as_base64("wp3592411.jpg")

page_bg_img = f"""
<style>
.stApp {{
background-image: url('data:image/jpg;base64,{img}');
background-size: cover;
}} 
</style>
"""
           
st.markdown(page_bg_img, unsafe_allow_html=True)


st.title("Soil Fertility Predictor")

N = st.number_input("Enter the value of nitrogen",1.00,500.00)
P = st.number_input("Enter the value of phosphorus",1.00,500.00)
K = st.number_input("Enter the value of potassium",1.00,500.00)
field_size = st.number_input("Enter the area of field (in meter square)",1.00,20000.00)
crop_list = ["Maize","Rice","Sugercane","Coconut"]
crop = st.selectbox("Enter the crop harvested",crop_list)
index = crop_list.index(crop)+1
if index == 4:index = 2
crop_to_be = st.selectbox("Enter the crop to be harvested",crop_list,index=index)



logreg_model = pickle.load(open("logreg_model.pickle","rb"))
naine_model = pickle.load(open("naine_model.pickle","rb"))
random_model = pickle.load(open("random_model.pickle","rb"))
svc_model = pickle.load(open("svc_model.pickle","rb"))


select_model = st.selectbox("Select the model",["None","Logistic regression","Randomforest Classifier","Naive Bayes Classifier","Support Vector Machine Classifier","Create new model"])

if select_model == "Create new model":
    st.file_uploader("Upload the dataset")
    
button_predict = st.button("Submit")

if button_predict:
    if select_model == "Logistic regression":
        model = logreg_model
    if select_model == "Randomforest Classifier":
        model = random_model
    if select_model == "Naive Bayes Classifier":
        model = naine_model
    if select_model == "Support Vector Machine Classifier":
        model = svc_model
    
    if N < 100 or K < 100 or P < 100:
        result = "Non Fertile"
    
    if N < 150 and K < 150 and P < 150 and field_size < 50: 
        result = "Non Fertile"
    
    else:
        result = model.predict([[7.74,0.4,0.01,0.01,N,P,K,0.48,6.4,0.21,4.7,84.3,6.8,8.9,6.72,7.81]])
        if result[0] == 1:
            result = "Fertile"
        if result[0] == 0:
            result = "Non Fertile"
    
    if select_model == "None":
        st.error("Please the select the model",icon="🚨")
    else:
        st.subheader("Result :" )
        st.success(str(result),icon="☑️")
        
        st.dataframe(pd.DataFrame(data={'ML-Algorithm':["Logistic regression","Randomforest Classifier","Naive Bayes Classifier","Support Vector Machine Classifier"],"Test_Accuracy":['93.33','90.00','93.33','0.56']}))
    

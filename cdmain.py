import streamlit as st
import pandas as pd
import numpy as np
import controller.user as usrc
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
from PIL import Image
import cv2
#import numpy as np
import av
#import mediapipe as mp
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


def main():
    st.title("COLD DRINKS INVENTORY MANAGEMENT")
    # usrc.create_table()

    menu = ["None","Staff","Admin"]
    choice = st.selectbox("Mode", menu)
    
    if choice=="Staff":
        st.subheader("Staff")
        with st.sidebar:
            d=st.date_input("Date")
            val=st.slider('confidence threshold',0.00,1.00)
            ch=['📽️video','📊data','🖼️image']
            q=st.radio('View Mode',ch)
            if(q=="📊data"):
                d=usrc.read_()
                op=['None','Excel','CSV']
                t=st.radio('Download Mode',op)
                if(t=="None"):
                    pass
                if t=="Excel":
                    usrc.excel(d)
                    st.write('Data is written successfully to Excel File.')
                if t=="CSV":
                    usrc.csv(d)
                    st.write('Data is written successfully to csv File.')


        if q=="📽️video":
            st.subheader("📽️video")
            webrtc_ctx = webrtc_streamer(
                key="WYH",
                mode=WebRtcMode.SENDRECV,
                rtc_configuration=RTC_CONFIGURATION,
                media_stream_constraints={"video": True, "audio": False},
            )

            store=st.checkbox("store")
            lab=st.checkbox("Show the detected labels")


        if q=="🖼️image":
            st.subheader("🖼️image")
            im=st.file_uploader('upload_image',type=['png','jpg','jpeg'])
            if(im):
                st.image(im)
            if im is not None:
                image = np.array(Image.open(im))  # Open buffer
                image = cv2.resize(image, (640, 640))  # resize image
                ##image_box, counting = load(model, image, confidence_threshold,
                                           #640)  
                #st.image(
                 #   image_box, caption=f"Processed image", use_column_width=True,
                #)
                #C = {k: v for k, v in counting.items() if v > 0}
                #data = pd.DataFrame(C, index=['items'])
                #st.sidebar.table(data)
                #for name, d in C.items():
                 #   usrc.create(time,name, d)*/
        if q=="📊data":
                st.subheader("📊data")
                with st.form("f1",clear_on_submit=True):
                    dtime=st.date_input("time")
                    dname=st.text_input("name")
                    dcount=st.number_input("count",min_value=0,step=1)
                    submit=st.form_submit_button("Submit")
                if(submit):
                    usrc.create_table()
                    usrc.create(dtime,dname,dcount)
                table=usrc.read_()
                st.table(table)
                ctt=usrc.count_()
                st.table(ctt)
                    



    if choice=="Admin":
        pass
    if choice=="None":
        pass

            
main()
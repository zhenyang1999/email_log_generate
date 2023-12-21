import streamlit as st
import pandas as pd
import base64
from io import BytesIO
import os
import re
import streamlit as st


def main():

    st.title("Please Fill In To Generate Email Log :sunglasses:")
    
    st.image('way_to_find_log_file_path.gif', caption='Way to Find Log File Generated Path')
    
    email_log_generated_path = st.text_input("Please Enter Log File Generated Path",r"C:\Users\Zhen Yang\Desktop")
    email_log_generated_path_pattern = re.compile(r'^C:\\')
    
    if email_log_generated_path == '':
        
        selected_keyword = []
        st.warning(":warning: Please Fill In to Continue !!! ")

    elif email_log_generated_path != '' : 

        # Predefined options for the multiselect
        keyword = ["INFO", "DEBUG", "WARN", "ERROR","FATAL","OTHERS"]

        # Multiselect widget
        selected_keyword = st.multiselect("Select Log Levels", keyword,["ERROR"])


        if 'OTHERS' in selected_keyword:

            # Text input widget
            other_keyword = st.text_input("Please Enter Your Keyword : ")

            # Display selected options and custom text
            #st.write("Custom Text Input:", other_keyword)

            selected_keyword.append(str(other_keyword))

            if 'OTHERS' in selected_keyword:
                selected_keyword.remove('OTHERS')

            if '' in selected_keyword:
                selected_keyword.remove('')



    last_line = st.number_input("Please Enter Number of Line to be Checked : ", value=100, placeholder="Type a number...")
    
    if last_line is not None:
        
        last_line = int(last_line)
    
    #st.write("Last Number of Line:", last_line)

    date_options = {
    "Today": 0,
    "Yesterday": 1,
    "2 day ago": 2,
    "3 day ago": 3,
    "1 weeks ago": 7,
    "2 weeks ago": 14,
    "1 month ago": 30}

    #st.title("Date Options Buttons")

    selected_date_key = st.radio("Select Log File Date:", list(date_options.keys()))
    selected_date = date_options[selected_date_key]

    email_subject = st.text_input("Please Enter Email Subject : ","Error in executing XXX Algorithm")
    
    #st.write("Email Subject:", email_subject)

    if st.button("Submit"):
        
        if (email_log_generated_path == '') |  (not bool(selected_keyword)) | (last_line is None ) | (selected_date is None) | (email_subject == ''):
            st.warning(':warning: There is still missing information')
        elif ( not email_log_generated_path_pattern.match(email_log_generated_path) ) :
            st.warning(':warning: Please ensure log file generated path in proper format :' + r'^C:\\XXXX')
        else:
            
            try:
                
                email_log_dir = email_log_generated_path.replace('/', '\\') + "/libEmailLog"
                
                os.mkdir(email_log_dir)

                with open("generated.py") as file:
                    emaillog_py_script = file.read()
                
                with open("run.py") as file:
                    run_py_script = file.read()
                
                with open("run.txt") as file:
                    run_py_bat = file.read()
                
                
                
                f = open(email_log_dir+"/email_log.py", 'w')
                f.write(emaillog_py_script)
                f.close()
                
                g = open(email_log_dir+"/run.py", 'w')
                g.write(run_py_script)
                g.close()
                
                h = open(email_log_dir+"/user_variable.ini",'w')
                h.write("[user_variable]\nselected_keyword = {a}\nselected_date = {b}\nlast_line = {c}\nemail_subject = {d}".format(a = selected_keyword,b = selected_date ,c=last_line,d = email_subject))
                h.close()
                
                i = open(email_log_dir+"/run.bat", 'w')
                i.write(run_py_bat)
                i.close()
                
                j = open(email_log_dir+"/email_cred.json", 'w')
                cred_json_sample = """{"EMAIL_ALERT":{"email_server":"abc@gmail.com",
                "password":"XXXXXXXXXX",
                "server":"smtp.gmail.com",
                "port":777,
                "receiver_list":["xyz@gmail.com","efg@gmail.com"]}}"""
                j.write(cred_json_sample)
                j.close()

                st.success("Congratulate, Email Log has been generated .")
                
                st.success("1. User need to fill in email_cred.json  ")
                st.success("2. User need to ensure run.bat has correct directory ")
                st.success("3. User need to ensure the ETL algorithm has logs/logfile.log and logging.ini ")
                st.success("4. User can run the run.bat to execute Email Log ")
                
            except FileExistsError:
                
                st.warning(":warning: Folder %s already exists" % email_log_generated_path)
                
            except FileNotFoundError:
                
                st.warning(":warning: The system cannot find the path specified:" % email_log_generated_path)
                
    #print(email_log_generated_path,selected_keyword, last_line, email_subject )

if __name__ == "__main__":
    main()
"""
This is a python script that loads a streamlit app on your home local 
browser. It loads a streamlit form to obtain data from job applicants. 
It stores the data as a csv file on local storage and to a mysql database.

It guides against duplicate data to deter multiple application.

FROM AUTHOR:
1. I am Lawal Kolawole.
2. Reach me on 09037740910 or lawalkolawole902@gmail.com
"""

import streamlit as st
import mysql.connector, toml, pandas as pd, time as t
from datetime import datetime
from pathlib import Path

# To dynamically greet based on time.
def tell_time():
    time = datetime.now().strftime("%H:%M:%S")
    timeset = time.split(':')
    if timeset[0] < '12' and timeset[0] >= '00':
        return '🌇 Good morning!'
    elif timeset[0] >= "12" and timeset[0] < "16":
        return "🌞 Good afternoon!"
    elif timeset[0]>='16':
        return "🌆 Good evening!"

# To create session to connect to mysql using connection params.
def mysql_connection():
# Ensure you input the password to your mysql database in the 'details.toml' to avoid complications!!!
        old_path = Path.cwd()
        path = old_path.parent
        new_path  = (path/'secrets'/'details.toml')
        with open(new_path, 'r') as f:
            file = toml.load(f)

        host, username, password = (
        file['connection']['host'],
        file['connection']['username'],
        file['connection']['password']
        )
        mydb = mysql.connector.connect(
        host = host,
        user = username, 
        password = password)

        return (mydb)

# To create mysql database on provided params.
def mysql_create(db: str, table: str):
    try:
        mydb = mysql_connection()
        cursor = mydb.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {db}"
        )
        cursor.execute(f'USE {db}')
        cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {table} (ID INT PRIMARY KEY AUTO_INCREMENT,
                    FIRST_NAME VARCHAR(300) NOT NULL,
                    LAST_NAME VARCHAR(300) NOT NULL,
                    EMAIL VARCHAR(100) NOT NULL,
                    PREFERRED_OFFICE VARCHAR(20),
                    EXPERIENCE INT,
                    EDUCATION VARCHAR(50),
                    GRAD_DATE VARCHAR(50),
                    PREFERRED_STATE VARCHAR(500),
                    EXPECTED_TO_RESUME_WITHIN INT,
                    CAREER_SUMMARY TEXT,
                    DATE VARCHAR(10),
                    TIME VARCHAR(10),
                    UNIQUE(EMAIL))
                    """)
        return
    except mysql.connector.Error as err:
        st.write('Error:', err)

# Main streamlit app to collect data and store in a mysql db.   
def main():
    # Setting page configs
    st.set_page_config(
    page_title = "APPLY HERE",
    page_icon = "🏠",
    layout = 'wide'
    )
    POSITION = [
        'ADMIN',
        'DRIVER',
        'NURSE',
        'DOCTOR',
        'RECEPTIONIST',
        'CLERIC',
        'DENTIST',
        'SURGEON',
        'DATA ANALYST',
        'SOFTWARE DEVELOPER',
        'DATA SCIENTIST'
    ]

    LEVEL_OF_GRADUATION = [
        'PRIMARY SCHOOL',
        'SECONDARY SCHOOL',
        'OND',
        'HND',
        'UNDERGRADUATE',
        'MASTERS',
        'PH.D',
        'ASSOCIATE PROFESSOR',
        'PROFESSOR'
    ]

    LOCATION = [
        'F.C.T',
        'Lagos',
        'Rivers',
        'Cross-River',
        'Oyo',
        'Kano'
    ]
    
    st.title('WELCOME TO XYZ Plc!')
    st.markdown(
        f"""
        {tell_time()}\n
        Kindly enter details as prompted below:
        """)
    st.info('THE SECTIONS MARKED * ARE REQUIRED!')
    try:
        wd = Path.cwd()
        new_path = Path(wd/'updated.csv')
        data_from_path = pd.read_csv(new_path)
        st.session_state['updated_data'] = data_from_path
        del st.session_state['updated_data']['Unnamed: 0']
    except:
        st.session_state['updated_data'] = pd.DataFrame([{
                        'First_name':'',
                        'Last_name':'',
                        'eMail': '',
                        'Office':'',
                        'Experience':'',
                        'Education':'',
                        'Grad_date':'',
                        'State':'',
                        'Expected_Resumption':'',
                        'career_summary':'',
                        'date':'',
                        'time':''
                    
        }])    

    # Creating form to collect data from applicants
    with st.form(key = 'User_Form', clear_on_submit=True, border=True):
        email = st.text_input('ENTER EMAIL HERE *').lower()
        col1, col2 = st.columns(2)
        first_name = col1.text_input('ENTER FIRST NAME HERE *')
        last_name = col2.text_input('ENTER LAST NAME HERE: *')
        office_choice = st.selectbox('SELECT YOUR PREFERRED OFFICE HERE:', options=POSITION, index = None)            
        experience = st.number_input('WORK EXPERIENCE (YEARS): ', min_value= 1, max_value=10, step = 1)
        edu_level = st.selectbox('LEVEL OF EDUCATION: ', options= LEVEL_OF_GRADUATION, index = None)
        date_of_graduation = st.date_input('DATE YOU GRADUATED ')
        location = st.multiselect('SELECT ONE OR MORE OF YOUR PREFERRED STATE HERE: ', options = LOCATION)
        resumption_date = st.number_input('WITHIN HOW MANY WEEKS WILL YOU RESUME UPON SELECTION?\n (MAXIMUM OF 4)', min_value=1, max_value=4, step=1)
        career_summary = st.text_area('TELL US A LITTLE ABOUT YOUR CAREER.', max_chars=500)
        time = datetime.now().strftime('%H:%M:%S')
        date = datetime.now().strftime('%Y-%m-%d')
        
        submit_button = st.form_submit_button('SUBMIT RESPONSE')

        if submit_button:
            # First name, Last name and email is compulsory else form will not submit info.
            if not email or not first_name or not last_name:
                st.warning('Ensure all fields are filled!!!')
                st.stop()
            
            # Stop app on repeated email address.
            elif st.session_state['updated_data']['eMail'].str.contains(email).any():
                st.warning('This email has already been used! Enter a new email address.')
                st.stop()
            # Upon successful submission.
            else:
                new_data = pd.DataFrame([{
                    'First_name':first_name,
                    'Last_name':last_name,
                    'eMail': email,
                    'Office':office_choice,
                    'Experience':experience,
                    'Education':edu_level,
                    'Grad_date':date_of_graduation.strftime('%Y-%m-%d'), # type: ignore
                    'State':", ".join(location),
                    'Expected_Resumption':int(resumption_date),
                    'career_summary':career_summary,
                    'date':date, # type:ignore
                    'time':time
                }])
                
                with st.balloons():
                    t.sleep(1)
                st.success('Your response has been captured! We appreciate your response.')
                with st.expander('SEE WHAT YOU ENTERED BELOW', expanded = False):
                    st.write(new_data)
                
                # Updating data by concatenating new data to old data
                st.session_state['updated_data'] = pd.concat([st.session_state['updated_data'], new_data], ignore_index = True)
                updated_data = pd.DataFrame(st.session_state['updated_data'])
        
                # Saving updated data to disk.
                updated_data.to_csv(new_path)
                
                # Deleting session state to hold new data
                del st.session_state['updated_data']

                # Inserting updated data into MySQL database
                mydb = mysql_connection()
                cursor = mydb.cursor()
                cursor.execute('USE APPLICANTS')
                query = 'INSERT IGNORE INTO APPLICANTS_DETAILS (FIRST_NAME, LAST_NAME, EMAIL, PREFERRED_OFFICE, EXPERIENCE, EDUCATION, GRAD_DATE, PREFERRED_STATE, EXPECTED_TO_RESUME_WITHIN, CAREER_SUMMARY, DATE, TIME) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                try:
                    cursor.execute(query, (first_name, last_name, email, office_choice, experience, edu_level, date_of_graduation.strftime('%Y-%m-%d'), ", ".join(location), int(resumption_date), career_summary, date, time )) # type: ignore 
                    mydb.commit()
                except mysql.connector.Error as err:
                    print('Insert error:', err)
                    return
                finally:
                    mydb.close()
                    return

# Main program.
if __name__ == '__main__':
    mysql_create(
                    db = 'APPLICANTS',
                    table = 'APPLICANTS_DETAILS'
                )

    main()
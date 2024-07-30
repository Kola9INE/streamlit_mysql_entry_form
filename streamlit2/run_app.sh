#!/bin/bash

applicants(){
    echo 'Hello, I will open a streamlit app on your local browser!'
    cd 'TYPE THE PATH TO THE applicants.py FOLDER HERE'
    echo 'Working in '$(pwd)
    streamlit run applicants.py
}
applicants
#!/bin/bash

applicants(){
    echo 'Hello, I will open a streamlit app on your local browser!'
    cd 'C:\Users\Kola PC\Desktop\examples\streamlit2\appl'
    echo 'Working in '$(pwd)
    streamlit run applicants.py
}
applicants
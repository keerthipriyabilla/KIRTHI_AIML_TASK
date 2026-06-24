import streamlit as st
import pandas as pd
import re

from datetime import date, datetime

from database import *
from predict import predict_health

create_table()

st.title("Health Prediction Application")

menu = ["Create", "View", "Update", "Delete"]

choice = st.sidebar.selectbox("Menu", menu)

# ==========================
# CREATE
# ==========================

if choice == "Create":

    fullname = st.text_input("Full Name")

    dob = st.date_input("Date Of Birth")

    email = st.text_input("Email Address")

    glucose = st.number_input(
        "Glucose",
        min_value=0.0,
        format="%.2f"
    )

    haemoglobin = st.number_input(
        "Haemoglobin",
        min_value=0.0,
        format="%.2f"
    )

    cholesterol = st.number_input(
        "Cholesterol",
        min_value=0.0,
        format="%.2f"
    )

if st.button("Predict & Save"):

    email = email.strip()

    st.write("Email Entered:", email)  # Debug

    if fullname.strip() == "":
        st.error("Full Name is required")

    elif dob > date.today():
        st.error("DOB cannot be a future date")

    else:

        remarks = predict_health(
            glucose,
            haemoglobin,
            cholesterol
        )

        add_patient((
            fullname,
            str(dob),
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        ))

        st.success("Patient Saved Successfully")

        st.write("Prediction:", remarks)

# ==========================
# VIEW
# ==========================

elif choice == "View":

    data = get_patients()

    if data:

        df = pd.DataFrame(
            data,
            columns=[
                "ID",
                "Name",
                "DOB",
                "Email",
                "Glucose",
                "Haemoglobin",
                "Cholesterol",
                "Remarks"
            ]
        )

        st.dataframe(df, use_container_width=True)

    else:
        st.info("No records found")

# ==========================
# UPDATE
# ==========================

elif choice == "Update":

    data = get_patients()

    if len(data) == 0:
        st.warning("No records available")
    else:

        ids = [row[0] for row in data]

        selected = st.selectbox(
            "Select Patient ID",
            ids
        )

        record = [r for r in data if r[0] == selected][0]

        fullname = st.text_input(
            "Full Name",
            value=record[1]
        )

        dob = st.date_input(
            "Date Of Birth",
            value=datetime.strptime(
                record[2],
                "%Y-%m-%d"
            ).date()
        )

        email = st.text_input(
            "Email",
            value=record[3]
        )

        glucose = st.number_input(
            "Glucose",
            value=float(record[4])
        )

        haemoglobin = st.number_input(
            "Haemoglobin",
            value=float(record[5])
        )

        cholesterol = st.number_input(
            "Cholesterol",
            value=float(record[6])
        )

        remarks = st.text_area(
            "Remarks",
            value=record[7]
        )

        if st.button("Update Record"):

            update_patient((
                fullname,
                str(dob),
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks,
                selected
            ))

            st.success(
                "Record Updated Successfully"
            )

# ==========================
# DELETE
# ==========================

elif choice == "Delete":

    data = get_patients()

    if len(data) == 0:
        st.warning("No records available")

    else:

        ids = [row[0] for row in data]

        selected = st.selectbox(
            "Select Patient ID",
            ids
        )

        if st.button("Delete Record"):

            delete_patient(selected)

            st.success(
                "Record Deleted Successfully"
            )
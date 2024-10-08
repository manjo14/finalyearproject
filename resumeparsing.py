import PyMupdf
import mysql.connector
import os

def pdf_to_text(pdf_file):
    """Extracts text from a PDF file using PyMuPDF."""
    text = ""
    with fitz.open(pdf_file) as doc:
        for page in doc:
            text += page.get_text()
    return text

def store_text_in_database(text, database_name, table_name):
    """Stores the extracted text in a MySQL database."""
    try:
        mydb = mysql.connector.connect(
            host="your_hostname",
            user="your_username",
            password="your_password",
            database=database_name
        )
        mycursor = mydb.cursor()

        sql = "INSERT INTO " + table_name + " (text) VALUES (%s)"
        val = (text,)
        mycursor.execute(sql, val)

        mydb.commit()
        print("Text stored successfully in the database.")
    except mysql.connector.Error as error:
        print("Error:", error)
    finally:
        mydb.close()

def fetch_text_from_database(database_name, table_name, id):
    """Fetches the stored text from the MySQL database."""
    try:
        mydb = mysql.connector.connect(
            host="your_hostname",
            user="your_username",
            password="your_password",
            database=database_name
        )
        mycursor = mydb.cursor()

        sql = "SELECT text FROM " + table_name + " WHERE id = %s"
        val = (id,)
        mycursor.execute(sql, val)

        result = mycursor.fetchone()
        if result:
            text = result[0]
            print("Fetched text:", text)
        else:
            print("No text found for the given ID.")
    except mysql.connector.Error as error:
        print("Error:", error)
    finally:
        mydb.close()

# Example usage:
pdf_file_path = "path/to/your/pdf_file.pdf"
database_name = "your_database_name"
table_name = "your_table_name"

text = pdf_to_text(pdf_file_path)
store_text_in_database(text, database_name, table_name)

# Fetch text using the ID of the stored record
id_to_fetch = 1  # Replace with the desired ID
fetch_text_from_database(database_name, table_name, id_to_fetch)
import  PyPDF2
import mysql.connector

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

        sql = f"INSERT INTO {table_name} (text) VALUES (%s)"
        val = (text,)
        mycursor.execute(sql, val)

        mydb.commit()
        print("Text stored successfully in the database.")
    except mysql.connector.Error as error:
        print("Error:", error)
    finally:
        mydb.close()

def fetch_text_from_database(database_name, table_name, resume_id):
    """Fetches the stored text from the MySQL database."""
    try:
        mydb = mysql.connector.connect(
            host="your_hostname",
            user="your_username",
            password="your_password",
            database=database_name
        )
        mycursor = mydb.cursor()

        sql = f"SELECT text FROM {table_name} WHERE id = %s"
        val = (resume_id,)
        mycursor.execute(sql, val)

        result = mycursor.fetchone()
        if result:
            return result[0]  # Return the resume text
        else:
            print("No resume found for the given ID.")
            return None
    except mysql.connector.Error as error:
        print("Error:", error)
        return None
    finally:
        mydb.close()

def main():
    # Path to your PDF file
    pdf_file = "path/to/your/file.pdf"  # Update this path
    
    # Database configuration
    database_name = "your_database_name"
    table_name = "your_table_name"
    
    # Step 1: Extract text from the PDF
    extracted_text = pdf_to_text(pdf_file)
    print("Extracted text from PDF.")
    
    # Step 2: Store the extracted text in the database
    store_text_in_database(extracted_text, database_name, table_name)
    
    # Step 3: Fetch the resume from the database (example with id=1)
    resume_id = 1  # Update as needed
    resume_text = fetch_text_from_database(database_name, table_name, resume_id)
    
    if resume_text:
        print("Fetched resume text:\n", resume_text)

if __name__ == "__main__":
    main()

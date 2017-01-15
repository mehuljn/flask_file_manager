Flask Based File Manager
============

Description:

This flask application allows the user to upload files.
The application uses MD5 hashing to determine if the files were uploaded previously if yes 
then it does not do the upload but gives the name of the originally uploaded file.

The app.py needs to have two folders configured 
One for temporary purpose
One for final storage of uploaded files.

Additionally there is also a logic built in which identifies any files present in the final storage folder, which
assists with the determination of duplicates.

How to run the application 

1. Clone the git repo
2. cd flask_file_manager
3. Fix the path of TEMP_UPLOAD_FOLDER and UPLOAD_FOLDER as per your requirement
4. start the app by "python app.py"



#1 Open folder
   cd /muzify

  ---  Linux  --- 
#2 Create vertual enviorment (linux)
   virtualenv env

#3 Activate virtual enviorment (linux)
   . env/bin/activate

  ---  windows  --- 
#2 Create vertual enviorment (windows)
   python -m venv env   

#3 Activate virtual enviorment  (windows)
   env/Scripts/activate 

#4 Download all flask modules (for all Operating System)
   pip install -r requirements.txt

#5 Run the application (for all Operating System)
   flask run 


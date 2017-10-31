#TASK:
#Take all downloaded csvs and create one new csv with course > company > accounts
import os
import csv
import pandas as pd

#This is the path to your Data folder containing all the downloaded csv files
path = "/Users/markhoeber/Desktop/data"

#This is where you want the manipulated data outputted 
out_path ='/Users/markhoeber/Desktop/output/'

#This is where you want the results outputted
report_path="/Users/markhoeber/Desktop/"

#function to parse the email address to get the customer name
def customer_name(csv_input):
    #split email by the @ sign
    second_half = csv_input['email'].split("@")
    #split the string after the @ sign by the period
    customer = second_half[1].split(".")
    #get the first half of the string split by the period
    return pd.Series({'company_name': customer[0]})

#function to add the column to the csv file with the customer name
def add_column():
    #for all the files in the Data folder
    for file in os.listdir(path):
        if file.startswith("."):
            print "Removing" + file
            #return None
        else:
            #adds the file name to the Data directory
            new_path = path + '/' + file
            #Make the New_Data directory if it doesn't exist
            if not os.path.exists(out_path):
                os.makedirs(out_path)

            #reads the csv file in the Data directory
            csv_input = pd.read_csv(new_path)

            #adds the new column called company_name with the parsed customer name
            csv_input['company_name'] = csv_input.iloc[:, 1:].apply(customer_name, axis=1)
            #writes to the the New_Data directory
            csv_input.to_csv(out_path+'new_'+file, index=False)

    #run group_data()
    group_data()
        
#group data by customer
def group_data():

    count = 0
    users = {}
    companies = {}

    #creates empty result
    #result = {}
    #path to the output.csv file
    out_file = os.path.join(report_path, 'output.csv')
    #print "Created "+ out_file
    #for file in the New_Data directory
    for file in os.listdir(out_path):
        #print "In for loop"
        #print file
        #split file name by _
        file_split = file.split("_")
        #get just the course number
        course_num = file_split[2]
        #print "course_num = " + course_num
        #get the date
        course_date_split = file_split[8].split(".")
        course_date = course_date_split[0]
        #print "course_date = " + course_date

        #path to the files in the New_Data directory
        new_path = out_path + '/' + file
        #open the files in the New_Data directory 
        with open(new_path, 'rb') as csvfile:
            #Need to reset results for each file processed
            result = {}
            #open the output.csv file so we can write to it
            with open(out_file, 'a') as out:
                #write the course number and course date to the file for each course
                out.write(course_num + " " + course_date + ', , \n')
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                #skip the first line in each csv to avoid confusion 
                next(csvreader)
                #for each row in the csv file
                for row in csvreader:
                    #if the company name is already found in the list of company names
                    if row[-1] in result:
                        #print "Adding to results = " + row[-1]
                        #Row 3 is the row containing the email
                        #Append the user email to the customer
                        result[row[-1]].append(row[3])
                    else:
                        #if the customer isnt found already, we add it to the list of customers
                        result[row[-1]] = [row[3]]
                #for the customer name and user emails per customer
                for key, value in sorted(result.items()):
                    #write the customer names to the output.csv file  
                    #print "Writing key " + key                  
                    out.write("," + key + ", \n")
                    #for each user email for customer
                    companies[key] = key
                    for elem in value:
                        #print "Writing value " + elem  
                        #write the user emails to the output.csv file under the corresponding customer
                        out.write(", ," + elem + "\n")
                        
                       
                        users[elem] = elem
                        
    print "Unique users"
    print len(users)
    print "Unique companies"
    print len(companies)




def remove_files():
    try:
      out_file = os.path.join(report_path, 'output.csv')
      #print "Removing " + out_file
      os.unlink(out_file)
      #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
      print(e)

    for the_file in os.listdir(out_path):
      file_path = os.path.join(out_path, the_file)
      try:
         if os.path.isfile(file_path):
            #print "Removing " + file_path
            os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
      except Exception as e:
        print(e)

#main function        
def main():
    #run add_column function first
    remove_files();
    add_column();

#run main function
main()





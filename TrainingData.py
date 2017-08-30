#TASK:
#Take all downloaded csvs and create one new csv with course > company > accounts
import os
import csv
import pandas as pd

#This is the path to your Data folder containing all the downloaded csv files
path = "/mnt/c/Users/kurt.bugbee/Desktop/Data"

#This is where you want the manipulated data outputted 
out_path ='/mnt/c/Users/kurt.bugbee/Desktop/New_Data/'

#This is where you want the results outputted
report_path="/mnt/c/Users/kurt.bugbee/Desktop/"

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
    #creates empty result
    result = {}
    #path to the output.csv file
    out_file = os.path.join(report_path, 'output.csv')

    #for file in the New_Data directory
    for file in os.listdir(out_path):
        #split file name by _
        file_split = file.split("_")
        #get just the course number
        course_num = file_split[2]
        #get the date
        course_date_split = file_split[8].split(".")
        course_date = course_date_split[0]

        #path to the files in the New_Data directory
        new_path = out_path + '/' + file
        #open the files in the New_Data directory 
        with open(new_path, 'rb') as csvfile:
            #open the output.csv file so we can write to it
            with open(out_file, 'a') as out:
                #write the course number and course date to the file for each course
                out.write(course_num + " " + course_date + ', , \n')
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                #skip the first line in each csv to avoid confusion 
                next(csvreader)
                #for each row in the csv file
                for row in csvreader:
                    #if the company name is already found in the list of compny names
                    if row[-1] in result:
                        #Row 3 is the row containing the email
                        #Append the user email to the customer
                        result[row[-1]].append(row[3])
                    else:
                        #if the customer isnt found already, we add it to the list of customers
                        result[row[-1]] = [row[3]]
                #for the customer name and user emails per customer
                for key, value in sorted(result.items()):
                    #write the customer names to the output.csv file                    
                    out.write("," + key + ", \n")
                    #for each user email for customer
                    for elem in value:
                        #write the user emails to the output.csv file under the corresponding customer
                        out.write(", ," + elem + "\n")


#main function        
def main():
    #run add_column function first
    add_column();

#run main function
main()





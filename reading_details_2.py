import csv
import os
import tabulate
from datetime import datetime

def ask_user(flight_data):
    option = int(input("1: Book tickets\n2: Search flight\n3: show Booking\n4: Exit\nEnter=> "))

    if(option == 1):
        option2 = int(input("1: To Check Flights Schedule\n2: To Book Flight By flight Name\nEnter=> "))
        if(option2==1):
            data1 = show_flights()
            return [1,data1]
        else:
            book_flight(flight_data[1])
            return [1,0]
        
    elif(option == 2):
        data2 = show_flights()
        return [2,data2]
    
    elif(option == 3):
        show_details_booked()
        return [3,0]
    
    else:
        return [4,0]

def show_flights():
    csv_file = open('Flight_Details.csv','r')
    csv_reader = csv.reader(csv_file)
    d_loc=input("Enter departure location: ")
    e_loc = input("Enter destination: ")
    data = []
    rows = []
    for header in csv_reader:
        head = header[0:6]
        break


    for flight in csv_reader:
        if(flight!=[] and flight[1].lower() == d_loc.lower() and flight[2].lower() == e_loc.lower()):
            data.append(flight[0:6])
            rows.append(flight)
    print(tabulate.tabulate(data, headers = head, tablefmt = "grid"))
    csv_file.close()
    return rows

def book_flight(data):

    flight_name = input("Enter name of flight to be booked: ")
    flight_to_book=[]
    csv_file = open("Flight_Details.csv", "r")
    csv_reader = csv.reader(csv_file)
    head=[]
    for header in csv_reader:
        head = header[0:6]
        break

    for flight in data:
        if(flight!=[] and flight[0].lower() == flight_name.lower()):
            print(tabulate.tabulate([flight[0:6]],headers=head,tablefmt="grid"))
            flight_to_book=flight
            break
        
    confirm=int(input("1.)To confirm the flight\n2.)To select another flight\nEnter=> "))
    if(confirm==1):
        csv_file.seek(0, 0)
        head=[]
        for header in csv_reader:
            head = header[9:13]
            break
        for flight in data:
            if(flight!=[] and flight[0].lower() == flight_name.lower()):
                print(tabulate.tabulate([flight[9:13]],headers=head,tablefmt="grid"))
                break
        
    elif(confirm==2):
        show_flights()
        return
    else:
        print("-----Invalid Option------")

    csv_file.close()

    if(int(input("To continue booking enter 1, else enter 0: "))):
        file=open("attendants.csv","a+")
        csv_app = csv.writer(file)
        name=input("Enter Your Name: ")
        gender=input("Enter Your Gender M/F/O: ")
        age=int(input("Enter Your Age: "))
        address=input("Enter Your Address: ")
        seats_booked = int(input("No. of seats to be booked: "))
        seat_type=input("Enter type of seats to book Business/Economy: ")
        upi_ID = input("Enter UPI ID for payment: ")
        details=[name,gender,age,address]
        details=details+flight_to_book[0:5]+[seats_booked,seat_type,upi_ID]
        csv_app.writerow(details)
        file.close()

        update_seats(flight_name, seat_type, seats_booked)
        print("BOOKING DONE!")

def update_seats(flight_name, seat_type, seats_booked):
    records = []
    
    file = open("Flight_Details.csv", "r")
    reader = csv.reader(file)
    for rec in reader:
        records.append(rec)
    file.close()

    file = open("temp.csv", "w", newline='')
    writer = csv.writer(file)
    for rec in records:
        if(rec!=[] and rec[0].lower() == flight_name.lower()):
            if(seat_type.lower() == 'business'):
                if(int(rec[9]) < seats_booked):
                    print("NOT ENOUGH SEATS!")
                    break
                rec[7] = str(int(rec[7]) + seats_booked)
                rec[8] = str(int(rec[8]) - seats_booked)
                rec[9] = str(int(rec[9]) - seats_booked)

            elif(seat_type.lower() == 'economy'):
                if(int(rec[11]) < seats_booked):
                    print("NOT ENOUGH SEATS")
                    break
                rec[7] = str(int(rec[7]) + seats_booked)
                rec[8] = str(int(rec[8]) - seats_booked)
                rec[11] = str(int(rec[11]) - seats_booked)
    writer.writerows(records)
    file.close()

    os.remove("Flight_Details.csv")
    os.rename("temp.csv", "Flight_Details.csv")

def show_details_booked():
    name = input("Enter your name: ")
    file = open("attendants.csv", "r")
    reader = csv.reader(file)
    for header in reader:
        head = header
        break
    for flight in reader:
        if(len(flight)!=0 and flight[0].lower() == name.lower()):
            print(tabulate.tabulate([flight[0:7]], headers = head[0:7], tablefmt = "grid"))
            print(tabulate.tabulate([flight[7:]], headers = head[7:], tablefmt = "grid"))
            break
    file.close()

def admin_change_details():
    file=open("Flight_Details.csv","r")
    reader = csv.reader(file)
    print(reader)
    flight_found = False

    data=[]

    header=[]
    for row in reader:
        header=row
        data.append(header)
        break

    for row in reader:
        if(data!=[]):
            data.append(row)

    flight_name=input("Enter Flight name=> ")
    dept_loc = input("Enter Departure Location=> ")
    dest_loc = input("Enter Destination Location=> ")

    for i in range(len(data)):
        if(data[i]!=[] and data[i][0].lower()==flight_name.lower() and data[i][1].lower()==dept_loc.lower() and data[i][2].lower()==dest_loc.lower()):
            flight_found=True
            print(tabulate.tabulate([data[i][0:7]],headers=header[0:7],tablefmt="grid"))
            print(tabulate.tabulate([data[i][7:]],headers=header[7:],tablefmt="grid"))

            quest = input("Do You Want To Change flight Details Yes/No=>")
            if(quest.lower()=="yes"):
                flight = data[i]
                # print(flight)
                while (True):
                    print("To Change ")
                    print("1.)Departure Time")
                    print("2.)Business Seat Price")
                    print("3.)Economy Seat Price")
                    print("4.) EXIT")
                    field = int(input("Enter The Field To Change=> "))
                    print()

                    if(field == 1):
                        time = input("Time: ")
                        flight[4]=time
                    elif(field ==2):
                        print("Current=> ",flight[10])
                        business_price = int(input("Enter Business Seats Price: "))
                        flight[10] = business_price
                    elif(field==3):
                            print("Current=> ",flight[12])
                            econmy_price = int(input("Enter Economy Seat Price: "))
                            flight[12] = econmy_price
                    elif(field==4):
                        print("-----------EXIT-----------")
                        break
                    else:
                        print("Wrong Option")
                    data[i]=flight

                    print(tabulate.tabulate([flight[0:7]],headers=header[0:7],tablefmt="grid"))
                    print(tabulate.tabulate([flight[7:]],headers=header[7:],tablefmt="grid"))
                    print()
                    print()
            else:
                print("---------------Exit-------------")
            file.close()

    if(flight_found==False):
        print("---FLIGHT NOT FOUND---")
    else:
        file=open("Flight_Details.csv","w", newline="")
        writer=csv.writer(file)
        writer.writerows(data)

        file.close()

def admin_add_new_flight():
    flight_name = input("Enter flight name: ")
    dep_loc = input("Enter departure location: ")
    des_loc = input("Enter destination: ")
    dep_date = input("Enter departure date in dd-mm-yyyy format: ")
    dep_hr = input("Enter departure hour acc to 24hr clock format: ")
    dep_min = input("Enter departure minute: ")
    dep_time = dep_hr + ":" + dep_min
    duration = input("Enter flight duration in hh:mm format: ")
    total_seats = input("Enter total number of seats: ")
    seats_booked = "0"
    seats_available = total_seats
    business_seats = input("Enter number of business class seats: ")
    business_price = input("Enter price of a business class tiket: ")
    economy_seats = str(int(seats_available) - int(business_seats))
    economy_price = input("Enter price of an economy seat: ")

    flight_rec = [flight_name, dep_loc, des_loc, dep_date, dep_time, duration, total_seats, seats_booked, seats_available, business_seats, business_price, economy_seats, economy_price]

    with open("Flight_Details.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(flight_rec)

def admin_delete_flight():
    name = input("Enter name of flight which is to be deleted: ")
    date = input("Enter departue date of flight which is to be deleted(dd-mm-yyyy forat): ")
    found = 0

    f_orig = open("Flight_Details.csv", "r")
    f_new = open("temp.csv", "w", newline="")
    reader= csv.reader(f_orig)
    writer = csv.writer(f_new)
    
    for flight in reader:
        if(flight[0].lower() == name.lower() and flight[3] == date):
            found = 1
            continue
        else:
            writer.writerow(flight)
    
    if(found == 0):
        print("-----------FLIGHT NOT FOUND!-----------")
        os.remove("temp.csv")
    else:
        os.remove("Flight_Details.csv")
        os.rename("temp.csv", "Flight_Details.csv")
        print("----------FLIGHT DELETED----------")

while (True):
    user = int(input("Enter 1 if you are an admin\nEnter 2 if you are a consumer:\nEnter 3 to EXIT \nEnter=> "))
    if(user == 1):
        employ_id = input("Enter your Employ ID : ")
        file = open('employs_id.csv', "r")
        ids = csv.reader(file)

        for id in ids:
            if id[0].lower() == employ_id.lower():
                print(f"ACCESS GRANTED\nWelcome {id[0]}")
                admin_logsheet_file = open('admin_logsheet.csv','a')
                log_writer = csv.writer(admin_logsheet_file)
                log_writer.writerow([id[0], datetime.now()])

                option = int(input("Enter 1) Change flight details\n2) Add new flight\n3) Delete existing flight\nEnter: "))
                if(option == 1):
                    admin_change_details()
                elif(option == 2):
                    admin_add_new_flight()
                elif(option == 3):
                    admin_delete_flight()
                else:
                    print("----------INVALID INPUT----------")

    elif(user == 2):
        previous_option=[]
        while(True):
            current_option=ask_user(flight_data=previous_option)
            previous_option = current_option
            if(current_option[0]==4):
                print("---------------THANK YOU!!!---------------")
                print("--------------DO VISIT AGAIN--------------")
                break

    elif(user==3):
        print("------EXIT-----")
        break

    else:
        print("Invalid Option")
    


            


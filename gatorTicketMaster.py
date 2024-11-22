import sys
import GatorTicketMasterService


if __name__ == "__main__":
    """
    This is the entry point or main function of the application. It takes checks the argument passed along with the makefile,
    then opens the file with file pointer and iterates over the function calls made in each line. 
    Each line is split to get actual API name being called and to get the arguments for API if required according to Problem Statement, also stripped for whitespaces.
    Finally after executing till the EOF of file or untill Quit() is encountered, it saves the output onto a txt file. 
    """

    gtm = GatorTicketMasterService.GatorTicketMaster() #initialize the ticket service which has all the control functions for each api.
    
    try:
        #check insufficient or bad arguements
        if len(sys.argv) > 2 or len(sys.argv) == 1:
            print("Invalid argument provided to code")

        else:
            fileName = sys.argv[1]
            print("You provided filename: ",fileName)
            print("Starting Application")
            with open(sys.argv[1],'r') as f:
                #open a new file with the name required as per Problem statement
                with open(f"{fileName[:-4]}_output_file.txt",'w') as out:
                    for apiCall in f:
                        apiCall = apiCall.split("(") #get the function from line like, AddSeats(10), splitting on '('
                        api = apiCall[0].lower()

                        #switch case over the function name from the required 10 functions in Problem Statement
                        match api:
                            case "initialize":
                                apiArg = apiCall[1].split(")")[0].strip() #get the initial size of seats heap
                                if not apiArg.isdigit():
                                    #if not a valid integer
                                    out.write("Invalid input. Please provide a valid number of seats")
                                else:
                                    #write output to file
                                    out.write(gtm.initialize(int(apiArg)))
                                
                                out.write("\n")

                            case "available":
                                out.write(gtm.available())
                                out.write("\n")

                            case "reserve":
                                apiCall = apiCall[1].split(")")[0].split(",")
                                apiArg1 = apiCall[0].strip() #userID
                                apiArg2 = apiCall[1].strip() #priority
                                if(apiArg1.isdigit == False or apiArg2.isdigit == False):
                                    #check for valid integer
                                    out.write("Invalid Input. Please provide a valid UserID or userPriority")
                                else:
                                    out.write(gtm.reserve(int(apiArg1), int(apiArg2)))
                                
                                out.write("\n")

                            case "cancel":
                                apiCall = apiCall[1].split(")")[0].split(",")
                                apiArg1 = apiCall[0].strip() #seatID
                                apiArg2 = apiCall[1].strip() #userID
                                if(apiArg1.isdigit == False or apiArg2.isdigit == False):
                                    out.write("Invalid Input. Please provide a valid userID or seatID")
                                    out.write("\n")
                                else:
                                    output = gtm.cancel(int(apiArg1), int(apiArg2))
                                    for item in output:
                                        #writig output on file for all operations at cancellation and rebooking due to waitlist.
                                        out.write(item)
                                        out.write("\n")
                            
                            case "exitwaitlist":
                                apiArg = apiCall[1].split(")")[0].strip() #userID
                                if not apiArg.isdigit():
                                    out.write("Invalid input. Please provide a valid userID")
                                else: 
                                    out.write(gtm.exitWaitlist(int(apiArg)))      

                                out.write("\n")  

                            case "updatepriority":
                                apiCall = apiCall[1].split(")")[0].split(",")
                                apiArg1 = apiCall[0].strip() #userID
                                apiArg2 = apiCall[1].strip() #new priority
                                if(apiArg1.isdigit == False or apiArg2.isdigit == False):
                                    out.write("Invalid Input. Please provide a valid userID or userPriority")
                                else:
                                    out.write(gtm.updatePriority(int(apiArg1), int(apiArg2)))

                                out.write("\n")

                            case "addseats":
                                apiArg = apiCall[1].split(")")[0].strip() #count for seats to be added
                                if not apiArg.isdigit():
                                    out.write("Invalid input. Please provide a valid number of seats")
                                    out.write("\n")
                                
                                else:
                                    output = gtm.addSeats(int(apiArg))
                                    #adding all outputs after increasing the seats, i.e. booking user from waitlist a reservation.
                                    for line in output:
                                        out.write(line)
                                        out.write("\n")

                            case "printreservations":
                                output = gtm.printReservations()
                                for item in output:
                                    out.write(f"Seat {item[0]}, User {item[1]}")
                                    out.write("\n")

                            case "releaseseats":
                                apiCall = apiCall[1].split(")")[0].split(",")
                                apiArg1 = apiCall[0].strip() #userID1
                                apiArg2 = apiCall[1].strip() #userID2
                                #check for a valid range
                                if(apiArg1.isdigit() == False or apiArg2.isdigit() == False or (apiArg1.isdigit() == True and apiArg2.isdigit() == True and int(apiArg1) > int(apiArg2))):
                                    out.write("Invalid Input. Please provide a valid range of userIDs")
                                    out.write("\n")
                                else:
                                    output = gtm.releaseSeats(int(apiArg1), int(apiArg2))
                                    for line in output:
                                        out.write(line)
                                        out.write("\n")
                            
                            case "quit":
                                f.close()
                                out.write("Program Terminated!!")
                                out.close()
                                print("Application quiting")
                                print(f"File saved with output: {fileName[:-4]}_output_file.txt")
                                sys.exit()
                            
                            case "":
                                pass


    except Exception as e:
        print(e)


Threads & Semaphores

Source code File : code.cpp

To Compile:
			Type exactly as following, in the directory containing code.cpp file.
			g++ code.cpp -lpthread -o code


To run:

		./code

		Output Start Line : ************Post Office Simulation with 50 Customers and 3 Postal Workers**********

		Output End Line   : 		*******************Post office Simulation Ended****************



Post Office Simulation

A Post Office is simulated by using threads to model customer and employee behavior.  


Customer:
        - 50 customers visit the Post Office (1 thread per customer up to 50), all created initially.
        - Only 10 customers can be inside the Post Office at a time.
        - Each customer upon creation is randomly assigned one of the following tasks:
             buy stamps
             mail a letter
             mail a package
        - Times for each task are defined in the task table.


Postal Worker:
        - 3 created initially, one thread each.
        - Serves next customer in line.
        - Service time varies depending on customer task.


Scales:
        - Used by the postal worker when mailing a package.
        - There is only one, which can only be used one at a time. 
        - The scales are not a thread.  They are just a resource the postal worker threads use. 


Other rules:
        - A thread should sleep 1 second in the program for each 60 seconds listed in the table.  
        - All mutual exclusion and coordination must be achieved with semaphores.  
        - A thread may not use sleeping as a means of coordination.  
        - Busy waiting (polling) is not allowed. 
        - Mutual exclusion should be kept to a minimum to allow the most concurrency.
        - Each thread should print when it is created and when it is joined.
        - Each thread should only print its own activities.  The customer threads prints customer actions and the postal worker threads prints postal worker actions.  

Summary:

        Function:
		To simulate Post Office with 50 customers and 3 postal workers
		
		Working:
		Takes no input. The number of customers and postal workers are hard-coded in source code. Platform – C/C++ language using g++ compiler (not gcc)

		Functions and variables:
		The source file ‘code.cpp’ is well commented with information about the variables and the functions. The comments in the source file can be referred for understanding the working of various functions and variables declared.
		
		Simulation:
		The simulation is done exactly as described in the project specification. It takes about 34 seconds to finish.
		All the customer threads are joined in a serial order that is customer 23 thread cannot be joined before customer 22 thread.
		Although any customer can leave post office as soon as he finishes doing his task.
		
		Difficulties:
		The main difficult part of the project was writing the pseudo-code with lowest mutual exclusion and best possible concurrency. Next difficulty was debugging, which became easy after using the thread id to refer which thread is printing what. Overall the project was not difficult to implement but it required working understanding of semaphores and the concept of mutual exclusion.
		
		Learning:
		While doing this project, my understanding about semaphores and the mutual exclusion solidified. It was delighting to see the whole project working up to the specification using semaphores and threads. I never used threads in C/C++. This project was a great hands-on experience. Multithreading and synchronizing them with semaphores is the heart of this project and that’s what I think now I am good at after this project.
		
		Result:
		Well this is how simulation steps go –
		Create customer threads
		Assign random task out of three tasks to customer Create postal worker threads
		Customers enter post office
		Postal worker is serving some customer
		Customer asks postal worker to perform some task Postal worker finishes performing the task Customer finishes with the task
		Customer leaves post office
		Joined Customer
		All customers are referred by their thread numbers.
		All postal workers are referred by their thread numbers.
// Author : Nishant Garg
// Date   : 2-12-2013
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <stdio.h>
#include <string.h>

// Function prototypes
int memory_read(int address);
int memory_write(int address, int data) ;
int memory_init(int argn, char *args[]);
int file_prompt();
int file_save();

//Global Variables for virtual hardware of the machine

//Messages
char welcome_message[] = "\n\t\t Welcome to Machine 1000 \n\t\t--------------------------\n";
char path_error[] = "\n\tThe path or filename you enetered does not exist \n\t\t\tPlease enter it again\t  ~~~(Anytime type 'exit' to close program)~~~\n";
char enter_path[] = "Enter the file name or path containing instruction set to initialize the memory \n\t~~~~(Anytime type 'exit' to close program)~~~ \n";

//Buffer and file variables
int exx;                        // ex buffer
int j;                          // To keep track of number of instructions and operands loaded from text file
FILE *ptr_file;                 // Global Variable of File type
char filename[100];             // Global Variable to hold filename

int memory[1000];               // Memory with 1000 integer entries
int PC, SP, IR, AC, X, Y;       // CPU registers
int mem2cpu[2];                 // To store file descriptor for child to parent pipe same as cpfd
int cpu2mem[2];                 // To store file descriptor for parent to child pipe same as mpfd
// Global Variables End


// Note : For starting the Machine 1000 you can either provide filename with or without 
//        path as an argument or later after running it.

int main(int argc, char *argv[])
{
    char bufcpu[5], bufmem[5], buff[5];
    int result_m2c, result_c2m, result;
    pid_t ppid;                   // To store parent ID
    pid_t chpid;                  // To store child ID
    
    //Temporary variables
    int temp1, temp2, tadd, tval, last_operand;
    char k;
    int port = 0;

    result_m2c = pipe(mem2cpu);           // Pipe created
    result_c2m = pipe(cpu2mem);           // Pipe created

    // Pipe unsuccessful, end the program
    if ((result_m2c == -1) || (result_c2m == -1)) exit(1);

    // Forking into a child process (Memory)
    result = fork();   

    // Fork Failed                      
    if (result == -1) exit(1);                

    // Fork Succeeded. Memory running Process as child
    if (result == 0)                  
    {
        // Memory Initialized with the instructions from text file successfully
        memory_init(argc, argv); 

        printf("Child - Memory Initialized with number of Instructions: %d \n\n", j);
        printf("Output Started\n");
        printf("--------------\n");

        // Send data about number of instructions to CPU
        sprintf(bufmem, "%d", j);       
        write(mem2cpu[1], bufmem, 5);

        //1010 is sent by CPU to end this while loop thereby ending child process
        while (temp1 != 1010)
        {
            read(cpu2mem[0], bufmem, 5);
            temp1 = atoi(bufmem);

            
            if (temp1 != 1001) 
            {
                // Unless 1001 is received from CPU keep reading values and send it to CPU
                sprintf(bufmem, "%d", memory[temp1]);
                write(mem2cpu[1], bufmem, 5);
            }
            else          
            {
                // 1001 is sent by CPU to tell the memory process to write some value at some address
                read(cpu2mem[0], bufmem, 5);
                // Save memory address received from CPU
                tadd = atoi(bufmem); 
                read(cpu2mem[0], bufmem, 5);
                // Save value to be written at received memory address
                tval = atoi(bufmem); 
                // Write value at received address
                memory[tadd] = tval; 
            }
        }
    }// Child Process block End
    // CPU Process block start
    else 
    {
        // Program Counter initialized to 0
        PC = 0;             
        SP = 999;           
        // Stack pointer at end of memory 
        // Memory starts at 0
        // printf("CPU Running\n");
        // fflush(stdout);
        
        //  CPU Copy of J(number of instructions in text file) updated
        read(mem2cpu[0], bufcpu, 5); 
        j = atoi(bufcpu);      
        if (j == 2000)exit(1);

        while (PC < (j + 1))
        {
            // Load instruction in the Instruction resgister
            // Increment the program counter
            IR = memory_read(PC); 
            PC++;         

            //printf("instruction %d  - Ac value is %d\n",IR,AC);  //Trace to debug the CPU states

            fflush(stdout);
            switch (IR)
            {

            // Load value                   -> Load the value into the AC
            case 1:
                AC = memory_read(PC);
                PC++;
                break;

            // Load addr                    -> Load the value at the address into the AC
            case 2:
                temp1 = memory_read(PC);
                AC = memory_read(temp1);
                PC++;
                break;

            // Store addr                   -> Store the value in AC the into the address
            case 3:
                temp2 = memory_read(PC);
                memory_write(temp2, AC);
                PC++;
                break;

            // AddX                         -> Add the value in X to the AC
            case 4:
                AC = AC + X;
                break;

            // AddY                         -> Add the value in Y to the AC
            case 5:
                AC = AC + Y;
                break;

            // SubX                         -> Subtract the value in X from the AC    
            case 6:
                AC = AC - X;
                break;

            // SubY                         -> Subtract the value in Y from the AC
            case 7:
                AC = AC - Y;
                break;

            // Get port                     -> If port=1, reads an int or if port=2, reads a char from the keyboard, stores it in the AC
            case 8:
                port = memory_read(PC);
                PC++;
                printf("Please enter a value :\n");
                fflush(stdout);
                if (port == 1)
                {
                    scanf("%d", &AC);
                }
                else if (port == 2)
                {
                    scanf("%c", &k);
                    AC = k;
                }
                else
                {
                    puts("inappropriate port value \n");
                }
                break;

            // Put port                     -> If port=1, writes an int or if If port=2, writes a char to the screen
            case 9:
                port = memory_read(PC);
                PC++;
                if (port == 1)
                {
                    //printf("Port =1\n");
                    printf("%d", AC);
                    fflush(stdout);
                }
                if (port == 2)
                {
                    //printf("Port =2\n");
                    printf("%c", AC);
                    fflush(stdout);
                }
                /*if(port==2||1){
                printf("Inappropriate port Value\n");
                break;
                }*/
                break;

            // CopyToX                      -> Copy the value in the AC to X
            case 10:
                X = AC;
                break;

            // CopyToY                      -> Copy the value in the AC to Y
            case 11:
                Y = AC;
                break;

            // CopyFromX                    -> Copy the value in X to the AC
            case 12:
                AC = X;
                break;

            // CopyFromY                    -> Copy the value in Y to the AC
            case 13:
                AC = Y;
                break;

            // Jump addr                    -> Jump to the address
            case 14:
                PC = memory_read(PC);
                break;

            // JumpIfEqual addr             -> Jump to the address only if the value in the AC is zero
            case 15:
                if (AC == 0)
                {
                    PC = memory_read(PC);
                }
                else
                {
                    PC++;
                }
                break;

            // JumpIfNotEqual addr          -> Jump to the address only if the value in the AC is not zero
            case 16:
                if (AC != 0)
                {
                    PC = memory_read(PC); // Take PC to that address
                }
                else
                {
                    PC++;
                }
                break;

            // Call addr                    -> Push return address onto stack, jump to the address
            case 17:
                memory_write(SP, PC + 1);
                SP--;
                PC = memory_read(PC);
                break;

            // Ret                          -> Pop return address from the stack, jump to the address
            case 18:
                PC = memory_read(SP + 1);
                SP++;
                break;

            // IncX                         -> Increment the value in X
            case 19:
                X++;
                break;

            // DecX                         -> Decrement the value in X
            case 20:
                X--;
                break;

            // End                          -> End execution
            case 30:
                printf("\n--------------\n");
                printf("Output Ended\n");

                printf("Thanks for using Machine 1000 ! See you again.\n");
                fflush(stdout);
                exit(1);
                break;

            // Invalid instruction
            default:
                printf("Instruction <%d> not found,Please refer to the readme file for instructions which I can understand.\nIf <%d> was intended to be an operand then please check your previous instruction\n -Machin 1000\n", IR, IR);
                fflush(stdout);
                PC++;
                break;

            } // switch end


        } // While loop end


        if (IR != 30)
        {
            printf("\n--------------\n");
            printf("Output Ended\n");
            printf("[ ~ Either Last instruction was not 30\n  ~ Or if it was 30, I interpreted it as an operand due to a previous instruction requirement.\n -> Still I ended as there were no more instructions,\n  Please always check you instructions carefully fulfiling all operand requirements\n Always end your program with end instruction=30 ]\n");
            printf(" - Machine 1000\n");
            printf("Thanks for using Machine 1000 ! \nSee you again.\n");
            fflush(stdout);
        }
        char buf[5];                    // Code to end memory process
        int ex = 1010;                  // Code to end memory process
        sprintf(buf, "%d", ex);         // Code to end memory process
        write(cpu2mem[1], buf, 5);      // Code to end memory processs
        waitpid(-1, NULL, 0);           // Waitpid can only be used for when we need parent to wait for child to finish

        exit(1);





    }// CPU Process block End

return 0;
}  // Main Block End


// Memory operation Functions
/*
#memory_read(address) -  Takes the address as the argument, Passes it to Memory process(child) over the pipe.Then it fetches the value at that address and returns that value.
#memory_write(address,data)-returns 0. It takes the address and the value to be written as argument and sends it to memory process via pipe to write in the memory array.
#memory_init - Handles the arguements passed to the program and let users enter the name or path of the text file they want to process.
           After processing the file successfully it initialize the memory array with the instructions using file_save and file_prompt functions.

*/

// Function to read memory through pipe at address 0
int memory_read(int address)                
{
    char buf[5];
    sprintf(buf, "%d", address);
    write(cpu2mem[1], buf, 5);
    read(mem2cpu[0], buf, 5);
    int data = atoi(buf);
    return data;
}

// Function to write data at address in memory
int memory_write(int address, int data)             
{
    int mode = 1001;
    char buf[5];
    sprintf(buf, "%d", mode);
    write(cpu2mem[1], buf, 5);
    sprintf(buf, "%d", address);
    write(cpu2mem[1], buf, 5);
    sprintf(buf, "%d", data);
    write(cpu2mem[1], buf, 5);
    return 0;
}

// Check the number of arguments passed in main function
int memory_init(int argn, char *args[])
{
    printf("%s", welcome_message);
    if (argn == 1)    
    {
        printf("%s", enter_path);
        file_prompt();
    }
    else
    {
        ptr_file = fopen(args[1], "r");
        if (!ptr_file)
        {
            printf("%s", path_error);
            file_prompt();
        }
        else
        {
            file_save();
        }
    }
    return exx;
}

// Memory operation Functions end


/* File Input and Processing Functions
#file_save - Reads the loaded text file and save it into an array.
#file_prompt - Provides the user with a appealing prompt to enter filename or to exit the program

*/


int file_save()
{
    puts("\nLoading File...\n");
    char buf[10];
    j = 0;
    while (fgets(buf, 10, ptr_file) != NULL)
    {
        printf("%s", buf);  // test code
        memory[j] = atoi(buf); // String to integer casting and insertion into memory space
        j = j + 1;
    }
    j = j - 1;
    fclose(ptr_file);
    puts("\nFile Loaded !\n");
    return 0;
}


int file_prompt()
{
    int i = 0; // Counter to keep track of number of file read attempts
    char bufmem[5];
    do
    {
        if (i > 0) printf("%s", path_error);
        printf(">>");
        scanf("%s", filename); // Test Code File read value Print
        if (strcmp("exit", filename) == 0) // If user writes exit,the program exits
        {
            exx = 2000;
            sprintf(bufmem, "%d", exx);
            write(mem2cpu[1], bufmem, 5); // To tell parent to exit immediately
            exit(1); // Exit the child,although may be it will terminate if parent exits first
        }
        ptr_file = fopen(filename, "r");
        i++;
    }
    while (!ptr_file);
    file_save();
    return 0;
}

// File Input and Processing Functions END

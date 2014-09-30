/* Post Office Simulation
        Author : Nishant Garg
        Number of Customers = 50
        Number of Postal Workers = 3

        Kindly ignore Debug mode code. It is used only to debug and improve the assign_task() function.
*/
// Included Libraries and namespaces
#include <iostream>
using namespace std;
#include <string>
#include <stdio.h>
#include <cstdlib>
#include <sys/types.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>
#include <errno.h>

// constants
#define BUY_STAMPS 1
#define MAIL_LETTER 2
#define MAIL_PACKAGE 3
const int QSIZE = 50;   // Number of customers
//int bs,ml,mp;         // Debug Mode  // To maintain count of different tasks asked by customer

// Global Array Variables
int tasks[QSIZE];       // Global array to hold task against the custmer no as position in array
int relation[QSIZE];    // Global array to hold relation between customer no and postal worker no

// Global Queue Variables
int queue[QSIZE];
int rear = -1;
int front = -1;

//semaphores
sem_t max_capacity;         // To enforce capacity constraint. Capacity allowed in Post Office at any instant = 10
sem_t serving[50];          // Unique to each customer.Used as coordination between postal worker and customer
sem_t order[50];            // Unique to each customer. Used to alert postal worker that customer has ordered.
sem_t scale;                // Shared Resource,can be used by one postal worker at a time
sem_t mutex;                //  To create critical sections
sem_t customer_ready;       // To signal Customer is ready to be served by postal worker
//sem_t mutex1;             // Debug Mode

// Function Prototypes
void *customer(void *arg );
void *postal_worker(void *arg );
int assign_task();
int enqueue1(int n);
int dequeue1();


int main()
{

    pthread_t Cthread[QSIZE];           // Create QSIZE number of Customer Threads
    pthread_t PWthread[3];              // Create 3 postal worker threads

    // Semaphore Intializations
    sem_init(&max_capacity, 0, 10);
    sem_init(&mutex, 0, 1);
    sem_init(&customer_ready, 0, 0);
    sem_init(&serving[50], 0, 0);
    sem_init(&order[50], 0, 0);
    sem_init(&scale, 0, 1);
    //sem_init(&mutex1,0,1); // Debug Mode
    printf("\n\n\t************Post Office Simulation with 50 Customers and 3 Postal Workers**********\n");
    int i, p;
    // Customer Threads creation start
    for
    (i = 0; i < 50; i++)
    {
        if (pthread_create(&Cthread[i], NULL, customer, (void *)i) == -1) //thread calls the function customer
        {
            printf("Thread %d cannot create\n", i);
        }


    }
    // Customer Threads creation end
    // Postal Workers Threads creation start
    for (p = 0; p <= 2; p++)
    {
        pthread_create(&PWthread[p], NULL, postal_worker, (void *)p); //thread calls the function postal_worker

    }
    // Postal Workers Threads creation end
    void *result;
    // To join customer threads
    for (i = 0; i < 50; i++)
    {
        pthread_join(Cthread[i], &result);
        printf("Joined Customer %d \n", i);
        //printf("\n\t\t\t\t\tCustomer thread %d returned %ld",i,long(result));
    }
    printf("\n*******************Post office Simulation Ended****************\n\n");
    /* // Debug mode
    printf(" Buy stamp customers    : %d\n",bs );
    printf(" Mail Letter customers  : %d\n",ml );
    printf(" Mail Package customers : %d\n",mp );
    */ // Debug mode

}


void *customer(void *arg )
{
    int customer_no, task, pworker;                 // Local Variables unquie to each thread
    customer_no = long(arg);                         // Thread id as the customer number
    printf("Customer %d created\n", customer_no);
    task = assign_task();                           // Randomly Task assigned to local variable task
    tasks[customer_no] = task;

    sem_wait(&max_capacity);
    printf("Customer %d enters post office\n", customer_no);

    sem_wait(&mutex);                               // Push Customer Number to queue using critical section
    enqueue1(customer_no);
    sem_post(&customer_ready);
    sem_post(&mutex);

    sem_wait(&serving[customer_no]);                // Wait for assignment of Postal Worker
    pworker = relation[customer_no];                // Store Postal Worker no. in local variable

    // Order Task
    if (task == BUY_STAMPS)    printf("Customer %d asks Postal Worker %d to Buy Stamps\n", customer_no, pworker);
    if (task == MAIL_LETTER)   printf("Customer %d asks Postal Worker %d to Mail Letter\n", customer_no, pworker);
    if (task == MAIL_PACKAGE)  printf("Customer %d asks Postal Worker %d to Mail Package\n", customer_no, pworker);
    sem_post(&order[customer_no]);                  // Signal postal worker that customer has ordered

    sem_wait(&serving[customer_no]);                // Wait for Postal Worker to perfrom task

    if (task == BUY_STAMPS)    printf("Customer %d finished Buying Stamps\n", customer_no);
    if (task == MAIL_LETTER)   printf("Customer %d finished Mailing Letter\n", customer_no);
    if (task == MAIL_PACKAGE)  printf("Customer %d finished Mailing Package\n", customer_no);


    printf("Customer %d leaves post office\n", customer_no);
    sem_post(&max_capacity);                        //  Signal on max capacity semaphore
}



void *postal_worker(void *arg )
{
    int pworkerno = long(arg);               // Local variable unique to each thread
    printf("Postal Worker %d created\n", pworkerno);

    while (1)
    {
        int cust_no, ctask;                     // Local Variables unique to each execution in while loop
        sem_wait(&customer_ready);              // Waiting for a customer to get ready

        sem_wait(&mutex);                       // Critical Section Start
        cust_no = dequeue1();                       // To dequeue ready customer from queue
        relation[cust_no] = pworkerno;             // To store relation between customer and postal worker
        sem_post(&mutex);                       // End Critical Section

        printf("Postal Worker %d serving Customer %d\n", pworkerno, cust_no);
        sem_post(&serving[cust_no]);

        sem_wait(&order[cust_no]);              // Waiting for specific customer to order task
        ctask = tasks[cust_no];                 // Store task from global register into local variable

        // Perform Tasks
        if (ctask == BUY_STAMPS)
        {
            sleep(1);
            /* // Debug mode
            sem_wait(&mutex1);
            bs++;                   // To Determine the number of Buy Stamp Customers
            sem_post(&mutex1);
            */ // Debug mode
        }
        if (ctask == MAIL_LETTER)
        {
            sleep(1.5);
            /* // Debug mode
            sem_wait(&mutex1);
            ml++;                   // To Determine the number of Mail Letter Customers
            sem_post(&mutex1);
            */ // Debug mode
        }
        if (ctask == MAIL_PACKAGE)
        {
            /* // Debug mode
            sem_wait(&mutex1);
            mp++;                   // To Determine the number of Mail Package Cusotmers
            sem_post(&mutex1);
            */ // Debug mode
            sem_wait(&scale);
            printf("Scale in use by Postal Worker %d\n", pworkerno);
            sleep(2);
            printf("Scale released by Postal Worker %d\n", pworkerno);
            sem_post(&scale);
        }
        printf("Postal Worker %d finished serving Customer %d\n", pworkerno, cust_no);
        sem_post(&serving[cust_no]);            // To signal specific customer about completion of tasks

        // Payment process can be inserted here. Not in the project specification
    }
}



// Function to assign random task to customers
int assign_task()
{
    int r, max, min;
    max = 3;
    min = 1;
    r = (rand() % (max + 1 - min)) + min;
    return r;
}

// Funtion for Inserting element in the queue at n position
int enqueue1(int n)
{
    if (rear == QSIZE - 1)return 1 ;
    rear++ ;
    queue[rear] = n;
    if (front == -1)front++ ;
}

// this function provides dequeue operations
int dequeue1()
{
    int dqval;
    if (front == -1)return 1;
    dqval = queue[front];
    if (front == rear)
        front = rear = -1 ;
    else
        front++ ;

    return dqval ;
}

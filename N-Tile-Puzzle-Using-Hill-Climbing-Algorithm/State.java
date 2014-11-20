import java.util.ArrayList;
import java.util.Arrays;


public class State
{

	private int Mdistance = 0;

        // Goal State
	private final int[] goalState = new int[]
	{ 1, 2, 3, 8, 0, 4, 7, 6, 5 };
        
        //To Store State Object Board
	private int[] currentBoard;

        // Initilize state with board array values
	public State(int[] board)
	{
		currentBoard = board;
		calcManhattandistance();
	}

        // Calculate Manhattan Distance for current Board with respect to goal State
	private void calcManhattandistance(){
		int index = -1;
		int goal[][] = {{0,0,0},{0,0,0},{0,0,0}};
		int ix=0;
		for(int g=0;g<3;g++){
			for(int m=0;m<3;m++){
			goal[g][m]=goalState[ix++];
                        }
		}
		for (int x = 0; x < 3; x++) {
			for (int y = 0; y < 3; y++) {
				index++;
				int val = currentBoard[index];
				for(int i=0;i<3;i++){
					for(int j=0;j<3;j++){
						if(goal[i][j]==val){
							if(val==0){								
								break;
							}														
							Mdistance+= Math.abs(x - i) + Math.abs(y - j);                                                       
							break;
						}
                                                  
					}

				}              

			}

		}
		
	}

	// Return location of empty slide
	private int calcHoleLoc()
	{
		int holeIndex = -1; // If could not find
		for (int i = 0; i < 9; i++){
			if (currentBoard[i] == 0)holeIndex = i;		
		}
		return holeIndex;
	}


        // Return Manhattan Distance
	public int getManDist()
	{
		return Mdistance;
	}

        // Copy Board
	private int[] copyBoard(int[] EightPuzzlestate)
	{
		int[] ret = new int[9];
            System.arraycopy(EightPuzzlestate, 0, ret, 0, 9);
		return ret;
	}


        // Generate Successor Nodes
	public ArrayList<State> genSiblings()
	{
		ArrayList<State> siblings = new ArrayList<>();
		int location = calcHoleLoc();

		if (location != 0 && location != 3 && location != 6)
		{
			createState(location - 1, location, siblings);
		}

		if (location != 6 && location != 7 && location != 8)
		{
			createState(location + 3, location, siblings);
		}
		if (location != 0 && location != 1 && location != 2)
		{
			createState(location - 3, location, siblings);
		}
		if (location != 2 && location != 5 && location != 8)
		{
			createState(location + 1, location, siblings);
		}

		return siblings;
	}

        // Create State Configuration
	private void createState(int L1, int L2, ArrayList<State> s)
	{
		int[] copy = copyBoard(currentBoard);
		int temp = copy[L1];
		copy[L1] = currentBoard[L2];
		copy[L2] = temp;
		s.add((new State(copy)));
	}

        // Check if current state is Goal State
	public boolean isGoal()
	{
		if (Arrays.equals(currentBoard, goalState))
		{
			return true;
		}
		return false;
	}

        // Print State Configuration
        public void printate()
	{       
		System.out.println(/*"Depth->"+n.depth+"  "+*/currentBoard[0] + "," + currentBoard[1] + ","
				+ currentBoard[2]+","+currentBoard[3] + "," + currentBoard[4] + ","
				+ currentBoard[5]+","+currentBoard[6] + "," + currentBoard[7] + ","
				+ currentBoard[8]);

	}

	public void printState()
	{
		System.out.println(currentBoard[0] + " | " + currentBoard[1] + " | "
				+ currentBoard[2]);
		System.out.println("---------");
		System.out.println(currentBoard[3] + " | " + currentBoard[4] + " | "
				+ currentBoard[5]);
		System.out.println("---------");
		System.out.println(currentBoard[6] + " | " + currentBoard[7] + " | "
				+ currentBoard[8]);

		System.out.println("\n\n");
	}



        // Check if State object have equal Configuration to the State object in Parameter
	public boolean ifEqual(State s)
	{
		if (Arrays.equals(currentBoard, ((State) s).getcurrentBoard()))
		{
			return true;
		}
		else
			return false;

	}

        //Return Current Board Values
	public int[] getcurrentBoard()
	{
		return currentBoard;
	}

}
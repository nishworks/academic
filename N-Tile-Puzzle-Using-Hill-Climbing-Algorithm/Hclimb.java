import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Stack;


public class Hclimb
{

        public static void main(String[] args) throws FileNotFoundException, IOException
	{   
            
                // Code to process input arguments into Integer array
		if (args.length < 1)
		{
                    System.out.println("Incorrect input Format");
                    System.exit(1);
		}
                             
                String input = args[0];
                String[] chars = input.split(",");
                
                int[] InitialState = new int[9];
                
                for(int i=0;i<chars.length;i++){
                InitialState[i] = Integer.parseInt(chars[i]);
                }
                // Input Processed
                
                Hclimb.Climb(InitialState);
                System.exit(-1);
	}
        
        
	public static void Climb(int[] board)
	{
		Snode root = new Snode(null,new State(board));
		Stack<Snode> stack = new Stack<>();
		stack.push(root);
                int nodeCount = 0;
		while (!stack.isEmpty()) // While there is a value in stack
		{                    

			Snode currentNode = (Snode) stack.pop();  // Pop one element    
                        //Check if current node is not goal state
			//System.out.println("dips: "+);
			//currentNode.getCurrentState.printate();

			if (!currentNode.getCurrentState().isGoal())
			{                            
                               // if(currentNode.depth==30) continue; // Check Depth
                                
                                   
                                
                                
				// generate currentNode's immediate successor states
				ArrayList<State> tempNodeSet = currentNode.getCurrentState().genSiblings();
				ArrayList<Snode> successorNodes = new ArrayList<>();
				
                                // put sucessor states in nodes
				for (int i = 0; i < tempNodeSet.size(); i++)
				{
                                        Snode RcheckNode;
					RcheckNode = new Snode(currentNode,tempNodeSet.get(i));
					
					// Check if nodesate is not repeat
					if (!ifRepeat(RcheckNode))
					{
                                            successorNodes.add(RcheckNode);
					}
				}

				// Check if nodeSuccessors is empty. 
				
				if (successorNodes.isEmpty())
					continue;

				Snode firstNode = successorNodes.get(0);

                                //get the node with the Minimum manhattan cost
				for (int i = 0; i < successorNodes.size(); i++)
				{
					if (firstNode.getCost() > successorNodes.get(i).getCost())
					{
						firstNode = successorNodes.get(i);
					}
				}

				int minValueManhattan = (int) firstNode.getCost();

				// Add nodes that have that same Minimum Value
				for (int i = 0; i < successorNodes.size(); i++)
				{
					if (successorNodes.get(i).getCost() == minValueManhattan)
					{
						stack.push(successorNodes.get(i));
					}
				}                                
                                nodeCount++;

			}
			else

			{
				// Stack to keep track of processed nodes
				Stack<Snode> solPath = new Stack<>();
				solPath.push(currentNode);
				currentNode = currentNode.getParent();
                                
                                //Extract All ancesor nodes up to root
				while (currentNode.getParent() != null)
				{
					solPath.push(currentNode); // Push Ancestors
					currentNode = currentNode.getParent();
				}
				solPath.push(currentNode);
				int loopSize = solPath.size();
				for (int i = 0; i < loopSize; i++)
				{
					currentNode = solPath.pop();
					currentNode.getCurrentState().printate(currentNode);
				}
				//System.out.println("Total nodes processed: "+ nodeCount);				
                                System.exit(0);
			}
		}

		
		System.out.println("No solution found!");

	}

        // Method to check if the state in the node has been visited before
	private static boolean ifRepeat(Snode s)
	{
		boolean value = false;
		Snode checkNode = s;
		while (s.getParent() != null)
		{
			if (s.getParent().getCurrentState().ifEqual(checkNode.getCurrentState()))
			{
				value = true;
			}
			s = s.getParent();
		}

		return value;
	}
        


}

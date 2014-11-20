

public class Snode
{

	private State currentState;
	private Snode parent;
	private double mCost; // Manhattan Cost
        public int depth;
	
        // Initialize Node object with Parent Node and State
	public Snode(Snode predecessor, State s)
	{
		parent = predecessor;
		currentState = s;
		mCost = s.getManDist();
                if(parent==null)depth=0;
                else depth=parent.depth+1;
	}
        
        // Return Current State Object
	public State getCurrentState()
	{
		return currentState;
	}

        // Return Parent Node Object
	public Snode getParent()
	{
		return parent;
	}

        //Return Manhattan Cost
	public double getCost()
	{
		return mCost;
	}
}
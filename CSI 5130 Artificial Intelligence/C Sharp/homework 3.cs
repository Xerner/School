using System;
using System.Collections.Generic;

static void Main(string[] args)
{
	List<string> startTiles = new List<string>
	{
		"1234",
		"5678",
		"9ABC",
		" DEF"
	};
	Console.Log(MoveTile(startTiles, Direction.Up))
}
/*
static void Main(string[] args)
{
	List<string> startTiles = new List<string>
	{
		"1234",
		"5678",
		"9ABC",
		" DEF"
	};

	List<string> target = new List<string>
	{
		"1234",
		"5678",
		"9ABC",
		"DEF "
	};

	var start = new Board();
	start.Tiles = startTiles

	var finish = new Board();
	finish.Tiles = target

	start.SetMisplacedTiles(finish);

	var activeBoards = new List<Board>();
	activeBoards.Add(start);
	var visitedBoards = new List<Board>();

	while (activeBoards.Any())
	{
		// retrieve the state with the lowest f cost
		var checkState = activeBoards.OrderBy(x => x.CostMisplacedTiles).First();

		if (checkState.X == finish.X && checkState.Y == finish.Y)
		{
			Console.Log(We are at the destination!);
			// TODO: We can actually loop through the parents of each tile to find our exact path which we will show shortly. 
			return;
		}

		visitedBoards.Add(checkState);
		activeBoards.Remove(checkState);

		var possibleBoards = GetPossibleStates(checkState, finish);

		foreach (var possibleBoard in possibleBoards)
		{
			//We have already visited this tile so we don't need to do so again!
			if (visitedBoards.Any(x => x.X == possibleBoard.X && x.Y == possibleBoard.Y))
				continue;

			//It's already in the active list, but that's OK, maybe this new tile has a better value (e.g. We might zigzag earlier but this is now straighter). 
			if (activeBoards.Any(x => x.X == possibleBoard.X && x.Y == possibleBoard.Y))
			{
				var existingBoard = activeBoards.First(x => x.X == possibleBoard.X && x.Y == possibleBoard.Y);
				if (existingBoard.CostMisplacedTiles > checkState.CostMisplacedTiles)
				{
					activeBoards.Remove(existingBoard);
					activeBoards.Add(possibleBoard);
				}
			}
			else
			{
				//We've never seen this tile before so add it to the list. 
				activeBoards.Add(possibleBoard);
			}
		}
	}

	Console.WriteLine("No Path Found!");
}
*/
class Board
{
	public List<string> Tiles;
	public int Cost { get; set; } // g cost - initialized in GetPossibleStates()
	public int MisplacedTiles { get; set; } // h cost
	public int CostMisplacedTiles => Cost + MisplacedTiles; // f cost
	public Board Parent { get; set; }

	// Hamming distance between this state and our target state
	public void SetMisplacedTiles(Board target)
	{
		this.MisplacedTiles = GetHammingDistance(Tiles, target.Tiles);
	}

	// Hamming distance is number of substitutions needed to make the strings match
	public static int GetHammingDistance(string s, string t)
	{
		if (s.Length != t.Length)
		{
			throw new Exception("Strings must be equal length");
		}

		int distance =
			s.ToCharArray()
			.Zip(t.ToCharArray(), (c1, c2) => new { c1, c2 })
			.Count(m => m.c1 != m.c2);

		return distance;
	}
}


private static List<Board> GetPossibleStates(Board currentBoard, Board targetBoard)
{
	var possibleStates = new List<Board>();

	int index = state.tiles.Find(x => x == ' ')
	// add to possibleStates if the tile move is in-bounds
	if (index > 0) possibleStates.Add(new Board { Tiles = MoveTile(currentBoard, Direction.Left), Parent = currentBoard, Cost = currentBoard.Cost + 1 },)
	if (index < 16) possibleStates.Add(new Board { Tiles = MoveTile(currentBoard, Direction.Right), Parent = currentBoard, Cost = currentBoard.Cost + 1 },)
	if (index > 4) possibleStates.Add(new Board { Tiles = MoveTile(currentBoard, Direction.Up), Parent = currentBoard, Cost = currentBoard.Cost + 1 },)
	if (index < 16-4) possibleStates.Add(new Board { Tiles = MoveTile(currentBoard, Direction.Down), Parent = currentBoard, Cost = currentBoard.Cost + 1 },)

	possibleStates.ForEach(board => board.SetMisplacedTiles(targetBoard));

	return possibleStates;
}

private static List<string> MoveTile(List<string> tiles, Direction direction)
{
	List<string> newTiles = new List<string>(tiles); // copies the tiles list
	int index, newIndex;
	index = tiles.Find(x => x == ' ')
	switch direction {
		case Direction.Up:
			newIndex -= 4; // 4 is total number of rows in our puzzle
			break;
		case Direction.Down:
			newIndex += 4; // 4 is total number of rows in our puzzle
			break;
		case Direction.Left:
			newIndex--;
			break;
		case Direction.Right:
			newIndex++;
			break;
	}
	// Move the tile
	newTiles[index] = newTiles[newIndex];
	// Set the tiles old position to ' '
	newTiles[newIndex] = ' ';
	return newTiles;
}

enum Direction
{
	Up,
	Down,
	Left,
	Right
}
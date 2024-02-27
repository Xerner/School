namespace Homework_3
{
	using System;
	using System.Collections.Generic;
    using System.Linq;

    class Program { 
		static void Main()
		{
			Console.WriteLine("================================================");
			Console.WriteLine("Homework 3 - A* with 15 puzzle problem");
			Console.WriteLine("Heuristic used is # of misplaced tiles, counted with Hamming distance");
			Console.WriteLine("================================================");
			Console.WriteLine();
			var start = Board.RandomBoard(20);
			var finish = new Board();
			Board.SolveWithAStar(start, finish);
		}

		public static int Factorial(int number)
		{
			int fact = number;
			for (int i = number - 1; i >= 1; i--)
			{
				fact = fact * i;
			}
			return fact;
		}
	}

	class Board
	{
		public static List<char> targetTiles = "123456789ABCDEF ".ToCharArray().ToList<char>();

		public List<char> Tiles;
		public int Cost { get; set; } // g cost - initialized in GetPossibleBoards()
		public int MisplacedTiles { get; set; } // h cost
		public int CostMisplacedTiles => Cost + MisplacedTiles; // f cost
		public Board Parent { get; set; }

		public Board()
		{
			Tiles = targetTiles;
		}

		public Board(List<char> tiles)
        {
			Tiles = tiles;
        }

		public static void SolveWithAStar(Board start, Board finish)
        {
			Console.WriteLine("Starting board");
			//List<char> startTiles = " 23415689A7CDEBF".ToCharArray().ToList<char>();
			PrintList(start.Tiles);
			Console.WriteLine();
			Console.WriteLine("Target board");
			PrintList(finish.Tiles);
			Console.WriteLine();
			Console.WriteLine();

			start.SetMisplacedTiles(finish);

			var activeBoards = new List<Board>();
			activeBoards.Add(start);
			var visitedBoards = new List<Board>();

			Console.WriteLine("Searching...\n");
			int boardLimit = Program.Factorial(start.Tiles.Count) / 2;
			DateTime time = DateTime.Now;
			while (activeBoards.Any())
			{
				// retrieve the board with the lowest f cost
				var checkBoard = activeBoards.OrderBy(x => x.CostMisplacedTiles).First();

				// TODO: Plot the number of objects in each list

				if (checkBoard.MisplacedTiles == 0)
				{
					Console.WriteLine("\nSolution found!");
					Console.WriteLine("Optimal moveset:\n");
					List<Board> optimalMoveset = new List<Board>();
					// Find optimal moveset
					while (checkBoard.Parent != null)
					{
						optimalMoveset.Add(checkBoard);
						checkBoard = checkBoard.Parent;
					}
					// Print optimal moves
					int counter = 0;
					Console.WriteLine("Start");
					PrintList(start.Tiles);
					Console.WriteLine();
					for (int i = optimalMoveset.Count - 1; i >= 0; i--)
					{
						Board board = optimalMoveset[i];
						counter++;
						Console.WriteLine("Move " + counter);
						PrintList(board.Tiles);
						Console.WriteLine();
					}
					//
					Console.WriteLine("Runtime: " + (time - DateTime.Now).ToString("FFF") + " ms");
					Console.WriteLine("Number of moves: " + optimalMoveset.Count);
					Console.WriteLine("Visited Boards: " + visitedBoards.Count);
					Console.WriteLine("Active Boards: " + activeBoards.Count);

					return;
				}

				visitedBoards.Add(checkBoard);
				activeBoards.Remove(checkBoard);

				Console.SetCursorPosition(0, Console.CursorTop-3);
				Console.WriteLine("Visited Boards: " + visitedBoards.Count);
				Console.WriteLine("Active Boards: " + activeBoards.Count);
				Console.WriteLine("Solution limit: " + visitedBoards.Count + " / " + boardLimit + " = " + ((int)visitedBoards.Count/boardLimit) + "%");

				var possibleBoards = Board.GetPossibleBoards(checkBoard, finish);

				foreach (var possibleBoard in possibleBoards)
				{
					//We have already visited this tile so we don't need to do so again!
					if (visitedBoards.Any(tempBoard => tempBoard.Tiles == possibleBoard.Tiles))
						continue;

					//It's already in the active list, but that's OK, maybe this new tile has a better value (e.g. We might zigzag earlier but this is now straighter). 
					if (activeBoards.Any(tempBoard => tempBoard.Tiles == possibleBoard.Tiles))
					{
						var existingBoard = activeBoards.First(tempBoard => tempBoard.Tiles == possibleBoard.Tiles);
						if (existingBoard.CostMisplacedTiles > checkBoard.CostMisplacedTiles)
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

		// Hamming distance between this board and our target board
		public void SetMisplacedTiles(Board target)
		{
			this.MisplacedTiles = GetHammingDistance(new string(Tiles.ToArray()), new string(target.Tiles.ToArray())); ;
		}

		// Hamming distance is number of substitutions needed to make the strings match
		public static int GetHammingDistance(string checkString, string targetString)
		{
			if (checkString.Length != targetString.Length)
			{
				throw new Exception("Strings must be equal length");
			}

			int distance =
				checkString.ToCharArray()
				.Zip(targetString.ToCharArray(), (c1, c2) => new { c1, c2 })
				.Count(m => m.c1 != m.c2);

			return distance;
		}

		public static List<Board> GetPossibleBoards(Board currentBoard, Board targetBoard)
		{
			var possibleBoards = new List<Board>();

			int index = currentBoard.Tiles.IndexOf(' ');
			// add to possibleBoards
			possibleBoards.Add(new Board { Tiles = MoveTile(currentBoard, Direction.Up),	Parent = currentBoard,	Cost = currentBoard.Cost + 1 });
			possibleBoards.Add(new Board { Tiles = MoveTile(currentBoard, Direction.Down),	Parent = currentBoard,	Cost = currentBoard.Cost + 1 });
			possibleBoards.Add(new Board { Tiles = MoveTile(currentBoard, Direction.Left),	Parent = currentBoard,	Cost = currentBoard.Cost + 1 });
			possibleBoards.Add(new Board { Tiles = MoveTile(currentBoard, Direction.Right),	Parent = currentBoard,	Cost = currentBoard.Cost + 1 });

			possibleBoards.ForEach(board => board.SetMisplacedTiles(targetBoard));

			return possibleBoards;
		}
		
		private static List<char> MoveTile(Board board, Direction direction)
		{
			List<char> newTiles = new List<char>(board.Tiles); // copies the tiles list
			int index = board.Tiles.IndexOf(' ');
			int newIndex = index;
			switch (direction)
			{
				case Direction.Up:
					if (index > 4) newIndex = index - 4; // 4 is total number of rows in our puzzle
					break;
				case Direction.Down:
					if (index < 16 - 4) newIndex = index + 4; // 4 is total number of rows in our puzzle
					break;
				case Direction.Left:
					if (index % 4 != 0) newIndex = index - 1;
					break;
				case Direction.Right:
					if ((index - 3) % 4 != 0) newIndex = index + 1;
					break;
			}
			// Move the tile
			newTiles[index] = newTiles[newIndex];
			// Set the tiles old position to ' '
			newTiles[newIndex] = ' ';
			return newTiles;
		}

        public static Board RandomBoard(int numberOfMoves)
        {
            Board board = new Board();
			Random rnd = new Random();
			for (int i = 0; i < numberOfMoves; i++)
            {
				board.Tiles = MoveTile(board, (Direction)rnd.Next(0, 4));
            }
			return board;
        }

		private static void PrintList(List<char> list)
		{
			for (int i = 0; i < list.Count; i++)
			{
				if ((i - 4) % 4 == 0) Console.Write('\n');
				Console.Write(list[i]);
			}
			Console.WriteLine();
		}
	}


	enum Direction
	{
		Up,
		Down,
		Left,
		Right
	}
}

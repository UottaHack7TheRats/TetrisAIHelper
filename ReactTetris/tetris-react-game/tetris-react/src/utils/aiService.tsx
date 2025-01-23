import axios from 'axios';
import { Block } from '../types';  // Import the necessary types

// Define the types for the parameters
export async function fetchAIMove(board: Number[][], upcomingBlocks: Block): Promise<string | null> {
  try {
    const response = await axios.post('http://127.0.0.1:5000/get-move', {
      board,
      upcomingBlocks,
    });
    return response.data.move; // Example move: "left", "right", "rotate", "drop"
  } catch (error) {
    console.error("Error fetching AI move:", error);
    return null;
  }
}

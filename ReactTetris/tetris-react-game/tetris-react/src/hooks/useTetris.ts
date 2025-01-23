import { useCallback, useEffect, useState } from 'react';
import { Block, BlockShape, BoardShape, EmptyCell, SHAPES } from '../types';
import { useInterval } from './useInterval';
import {
  useTetrisBoard,
  hasCollisions,
  BOARD_HEIGHT,
  getEmptyBoard,
  getRandomBlock,
} from './useTetrisBoard';

import { fetchAIMove } from '../utils/aiService';

enum TickSpeed {
  Normal = 800,
  Sliding = 100,
  Fast = 50,
}

let aiRecomendationX=0
let aiRecomendationY=0
let aiRecomendationBlock = Block.shadow
let aiRecomendationBlockMatrix =      [[false, false, false, false],
[false, false, false, false],
[false, false, false, false],
[false, false, false, false],]

let currentBlock = Block.shadow


function calculateLandingRow(
  board: BoardShape,
  droppingShape: BlockShape,
  droppingRow: number,
  droppingColumn: number
): number {
  let landingRow = droppingRow;
  while (
    !hasCollisions(board, droppingShape, landingRow + 1, droppingColumn)
  ) {
    landingRow++;
  }


  
  return landingRow;
}


async function callAI(board: any[][]){
  const transformedBoard = board.map((row: any[]) =>
    row.map(cell => (cell === "Empty" ? 0 : 1))
  );
  
  //console.log('Board state before new piece drop:');
  //console.log(JSON.stringify(transformedBoard, null, 2));

  const aiMove = await fetchAIMove(transformedBoard, currentBlock);

  if (aiMove) {

    aiRecomendationX = Number(aiMove[0])
    aiRecomendationY = Number(aiMove[1])
    let currentPiece = Block.shadow
    switch (Number(aiMove[2])) {
      case 0: currentPiece = Block.O; break;
      case 1: currentPiece = Block.I; break;
      case 2: currentPiece = Block.S; break;
      case 3: currentPiece = Block.Z; break;
      case 4: currentPiece = Block.T; break;
      case 5: currentPiece = Block.J; break;
      case 6: currentPiece = Block.L; break;
    }
    aiRecomendationBlock = currentPiece

    //   0    1    2    3
    //   4    5    6    7
    //   8    9    10   11
    //   12   13   14   15

    aiRecomendationBlockMatrix = [[false, false, false, false],
    [false, false, false, false],
    [false, false, false, false],
    [false, false, false, false],]
   
    for (let i = 0; i <4;i++){
        aiRecomendationBlockMatrix[Math.floor((Number)(aiMove[3][i])/4)][(Number)(aiMove[3][i])%4] = true
      
    }
    if(check3x3(aiRecomendationBlockMatrix)){
       
      let aiRecomendationBlockMatrix2 = [[false, false, false],
      [false, false, false],
      [false, false, false],
      ]
      for (let i = 0; i <3;i++)
        for (let j = 0; j <3;j++){
        aiRecomendationBlockMatrix2[i][j] = aiRecomendationBlockMatrix[i][j]
      }
      aiRecomendationBlockMatrix = [[false, false, false],
      [false, false, false],
      [false, false, false]]
      aiRecomendationBlockMatrix = aiRecomendationBlockMatrix2
    }

    if(areMatricesEqual([[false, false, false, false],
[true, true, true, true],
 [false, false, false, false],
[false, false, false, false],],
    (aiRecomendationBlockMatrix))){
      aiRecomendationY +=1
      
    }
    if(areMatricesEqual(
    [[false, false, false],
    [true, true, true],
[true, false, false],],
aiRecomendationBlockMatrix
)){
  aiRecomendationY +=1
}

if(areMatricesEqual(
  [[false, false, false],
[true, true, true],
[false, true, false]],
aiRecomendationBlockMatrix
)){
aiRecomendationY +=1
}

if(areMatricesEqual(
  [[false, false, false],
  [true, true, true],
  [false, false, true]],
aiRecomendationBlockMatrix
)){
aiRecomendationY +=1
}




    console.log(aiRecomendationBlockMatrix)
    //aiRecomendationBlockMatrix =aiRecommendationBlockMatrix2
    //aiRecomendationY
  }
}

function check3x3(matrix: boolean[][]){
  for (let i = 0; i <4;i++){
    if (matrix[i][3] === true)
      return false;
  }
  for (let i = 0; i <4;i++){
    if (matrix[3][i] === true)
      return false;
  }
  return true
}

function areMatricesEqual(matrix1: boolean[][], matrix2: boolean[][]) {
  if (matrix1.length !== matrix2.length) return false; // Check if the number of rows is different

  for (let i = 0; i < matrix1.length; i++) {
      if (matrix1[i].length !== matrix2[i].length) return false; // Check if the number of columns is different

      for (let j = 0; j < matrix1[i].length; j++) {
          if (matrix1[i][j] !== matrix2[i][j]) return false; // Compare each element
      }
  }

  return true;
}
  
export function useTetris() {
  const [score, setScore] = useState(0);
  const [level, setLevel] = useState(0);
  const [lines, setLines] = useState(0);

  const [upcomingBlocks, setUpcomingBlocks] = useState<Block[]>([]);
  const [isCommitting, setIsCommitting] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [tickSpeed, setTickSpeed] = useState<TickSpeed | null>(null);

  const [
    { board, droppingRow, droppingColumn, droppingBlock, droppingShape },
    dispatchBoardState, boardStateRef
  ] = useTetrisBoard();

  const startGame = useCallback(() => {
    const startingBlocks = [
      getRandomBlock(),
      getRandomBlock(),
      getRandomBlock(),
    ];
    setScore(0);
    setLevel(1);
    setLines(0);
    setUpcomingBlocks(startingBlocks);

    setIsCommitting(false);
    setIsPlaying(true);
    setTickSpeed(TickSpeed.Normal);
    dispatchBoardState({ type: 'start' });

  }, [dispatchBoardState]);

  useEffect(() => {
    if (isPlaying && boardStateRef.current.droppingBlock) {
      currentBlock = boardStateRef.current.droppingBlock;
      console.log("First Block:", currentBlock); // Debugging: log the first block
    }
  }, [boardStateRef, boardStateRef.current.droppingBlock, isPlaying]);

  const commitPosition = useCallback(async () => {
    if (!hasCollisions(board, droppingShape, droppingRow + 1, droppingColumn)) {
      setIsCommitting(false);
      setTickSpeed(TickSpeed.Normal);
      return;
    }

    const newBoard = structuredClone(board) as BoardShape;

    addShapeToBoard(
      newBoard,
      droppingBlock,
      droppingShape,
      droppingRow,
      droppingColumn,
      droppingBlock
    );

    let numCleared = 0;
    for (let row = BOARD_HEIGHT - 1; row >= 0; row--) {
      if (newBoard[row].every((entry) => entry !== EmptyCell.Empty)) {
        numCleared++;
        newBoard.splice(row, 1);
      }
    }



    const newUpcomingBlocks = structuredClone(upcomingBlocks) as Block[];
    const newBlock = newUpcomingBlocks.pop() as Block;
    currentBlock = newBlock
    newUpcomingBlocks.unshift(getRandomBlock());

    if (hasCollisions(board, SHAPES[newBlock].shape, 0, 3)) {
      setIsPlaying(false);
      setTickSpeed(null);
    } else {
      setTickSpeed(TickSpeed.Normal);
    }
    setUpcomingBlocks(newUpcomingBlocks);
    setScore((prevScore) => prevScore + getPoints(numCleared));
    setLines((prevLines) => prevLines + (numCleared % 10));
    setLevel(() => lines < 10 ? 1 : (Math.floor((lines % 100) / 10)) + 1)

    dispatchBoardState({
      type: 'commit',
      newBoard: [...getEmptyBoard(BOARD_HEIGHT - newBoard.length), ...newBoard],
      newBlock,
    });
    setIsCommitting(false);
    
    //console.log(aiMove)
    //console.log(upcomingBlocks)
  }, [
    board,
    dispatchBoardState,
    droppingBlock,
    droppingColumn,
    droppingRow,
    droppingShape,
    upcomingBlocks,
    lines
  ]);


  const gameTick = useCallback(async () => {
    if (isCommitting) {
      commitPosition();
    } else if (
      hasCollisions(board, droppingShape, droppingRow + 1, droppingColumn)
    ) {
      setTickSpeed(TickSpeed.Sliding);
      setIsCommitting(true);
    } else {
      dispatchBoardState({ type: 'drop' });
    }


    callAI(board)

    
  }, [
    board,
    commitPosition,
    dispatchBoardState,
    droppingColumn,
    droppingRow,
    droppingShape,
    isCommitting,
  ]);

  useInterval(() => {
    if (!isPlaying) {
      return;
    }
    gameTick();
  }, tickSpeed);

  

  useEffect(() => {
    if (!isPlaying) {
      return;
    }

    let isPressingLeft = false;
    let isPressingRight = false;
    let moveIntervalID: number | undefined;

    const updateMovementInterval = () => {
      clearInterval(moveIntervalID);
      dispatchBoardState({
        type: 'move',
        isPressingLeft,
        isPressingRight,
      });
      moveIntervalID = setInterval(() => {
        dispatchBoardState({
          type: 'move',
          isPressingLeft,
          isPressingRight,
        });
      }, 300);
    };

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.repeat) {
        return;
      }

      if (event.key === 'ArrowDown') {
        setTickSpeed(TickSpeed.Fast);
      }

      if (event.key === 'ArrowUp') {
        dispatchBoardState({
          type: 'move',
          isRotating: true,
        });
      }

      if (event.key === 'ArrowLeft') {
        isPressingLeft = true;
        updateMovementInterval();
      }

      if (event.key === 'ArrowRight') {
        isPressingRight = true;
        updateMovementInterval();
      }

      if (event.key === ' ') {
        console.log('in')
        if (aiRecomendationX !== 0 && aiRecomendationY !== 0) {  // Ensure AI recommended a valid spot
          // Move the block to the AI-suggested position
          dispatchBoardState({
            type: 'moveToPosition',  // Add the moveToPosition handler in your board state logic
            x: aiRecomendationY,
            y: aiRecomendationX,
          });

          addShapeToBoard(
            board,
            aiRecomendationBlock, // Use a unique value to represent the outline
            aiRecomendationBlockMatrix, // Use a unique value to represent the outline
            aiRecomendationY,
            aiRecomendationX,
            aiRecomendationBlock
          );

          // Commit the position immediately to finalize the drop
          commitPosition();
        }
      }
    };

    const handleKeyUp = (event: KeyboardEvent) => {
      if (event.key === 'ArrowDown') {
        setTickSpeed(TickSpeed.Normal);
      }

      if (event.key === 'ArrowLeft') {
        isPressingLeft = false;
        updateMovementInterval();
      }

      if (event.key === 'ArrowRight') {
        isPressingRight = false;
        updateMovementInterval();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('keyup', handleKeyUp);
      clearInterval(moveIntervalID);
    };
  }, [dispatchBoardState, isPlaying, commitPosition, board]);


  const renderedBoard = structuredClone(board) as BoardShape;
  if (isPlaying) {
    // Calculate the landing row
    const landingRow = calculateLandingRow(
      board,
      droppingShape,
      droppingRow,
      droppingColumn
    );

    // Add the outline to the rendered board
    //console.log(aiRecomendationBlockMatrix)
    addShapeToBoard(//THIS IS FOR SHAODWW TRUSTTTTT
      renderedBoard,
      droppingBlock, // Use a unique value to represent the outline
      droppingShape,
      landingRow,
      droppingColumn,
      Block.shadow
    );

    //console.log(aiRecomendationBlock, aiRecomendationX, aiRecomendationY)
    addShapeToBoard(//THIS IS AI
      renderedBoard,
      aiRecomendationBlock, // Use a unique value to represent the outline
      aiRecomendationBlockMatrix, // Use a unique value to represent the outline
      aiRecomendationY,
      aiRecomendationX,
      Block.gold
    );

    // Add the actual block to the rendered board
    addShapeToBoard(
      renderedBoard,
      droppingBlock,
      droppingShape,
      droppingRow,
      droppingColumn,
      droppingBlock
    );
  }
  // if (isPlaying) {
  //   addShapeToBoard(
  //     renderedBoard,
  //     droppingBlock,
  //     droppingShape,
  //     droppingRow,
  //     droppingColumn,
  //     droppingBlock
  //   );
  // }

  return {
    board: renderedBoard,
    startGame,
    isPlaying,
    score,
    lines,
    level,
    upcomingBlocks,
  };

}

function getPoints(numCleared: number): number {
  switch (numCleared) {
    case 0:
      return 0;
    case 1:
      return 40;
    case 2:
      return 100;
    case 3:
      return 300;
    case 4:
      return 1200;
    default:
      throw new Error('Unexpected number of rows cleared');
  }
}

function addShapeToBoard(
  board: BoardShape,
  droppingBlock: Block,
  droppingShape: BlockShape,
  droppingRow: number,
  droppingColumn: number,
  color: Block,
) {
  if(board !== null) {
    droppingShape
      .filter((row) => row.some((isSet) => isSet))
      .forEach((row: boolean[], rowIndex: number) => {
        row.forEach((isSet: boolean, colIndex: number) => {
          if (isSet && board[droppingRow + rowIndex] &&
            board[droppingRow + rowIndex][droppingColumn + colIndex] !== undefined) {
            board[droppingRow + rowIndex][droppingColumn + colIndex] =
              color;
          }
        });
      });
    }
}

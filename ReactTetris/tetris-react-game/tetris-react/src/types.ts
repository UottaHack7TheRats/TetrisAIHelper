export enum Block {
  I = 'I',
  J = 'J',
  L = 'L',
  O = 'O',
  S = 'S',
  T = 'T',
  Z = 'Z',
  shadow = "shadow",
  gold = "gold"

}

export enum EmptyCell {
  Empty = 'Empty',
}

// export enum OutlineCell {
//   Outline = 'Outline',
// }

export type CellOptions = Block | EmptyCell;

export type BoardShape = CellOptions[][];

export type BlockShape = boolean[][];

type ShapesObj = {
  [key in Block]: {
    shape: BlockShape;
  };
};

export const SHAPES: ShapesObj = {
  I: {
    shape: [
      [false, true, false, false],
      [false, true, false, false],
      [false, true, false, false],
      [false, true, false, false],

    ],
  },
  J: {
    shape: [
      
      [false, false, false],
      [true, false, false],
      [true, true, true],
      
    ],
  },
  L: {
    shape: [
      
     
      [false, false, true],
      [true, true, true],
      [false, false, false],
    ],
  },
  O: {
    shape: [
      [false, true, true],
      [false, true, true],
      [false, false, false],
      
    ],
  },
  S: {
    shape: [
      [true, true, false],
      [false, true, true],
      [false, false, false],
      
    ],
  },
  T: {
    shape: [
      
      
      [false, true, false],
      [true, true, true],
      [false, false, false],
    ],
  },
  Z: {
    shape: [
      [false, true, true],
      [true, true, false],
      [false, false, false],

    ],
  },
  shadow: {
    shape: [

    ],
  },
  gold: {
    shape: [

    ],
  },

};

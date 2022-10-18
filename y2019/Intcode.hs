module Intcode (interp) where

import Debug.Trace
import Data.Char

data Mode = Pos | Imm deriving (Eq, Ord, Enum, Show)
data Call = Op { o :: Int, aTypes :: [Mode] } deriving (Eq, Show)

upd :: [a] -> Int -> a -> [a]
upd l pos n = take pos l ++ [n] ++ drop (pos + 1) l

argNum :: Int -> Int
argNum op
    | op `elem` [7, 8] = 3
    | op `elem` [3, 4] = 1
    | op `elem` [1, 2, 5, 6] = 2
    | op == 99 = 0

parseArg :: Int -> Call
parseArg op =
    let
        o = op `mod` 100
        aNum = argNum o
        given = show (op `div` 100)
        numToMode x
            | x == 0 = Pos
            | x == 1 = Imm

        hid :: [Mode] = replicate (aNum - length given) Pos

        args = hid ++ map (numToMode . digitToInt) given
    in Op o (reverse args)

get :: [Int] -> Int -> Mode -> Int
get code arg Pos = code !! (code !! arg)
get code arg Imm = code !! arg

interp :: [Int] -> Int -> IO([Int], Int)
interp code at =
    let Op opType argTypes = parseArg (code !! at)
        nextInd = at + argNum opType + 1
        args = [get code (at + i) (argTypes !! (i - 1)) | i <- [1..length argTypes]]
    in case opType of
        1 -> let
                val1 = args !! 0
                val2 = args !! 1
                ind = code !! (at + 3)
            in interp (upd code ind (val1 + val2)) nextInd
        
        2 -> let
                val1 = args !! 0
                val2 = args !! 1
                ind = code !! (at + 3)
            in interp (upd code ind (val1 * val2)) nextInd
        
        3 -> do
            val <- readLn
            let ind = code !! (at + 1)
            interp (upd code ind val) nextInd
        
        4 -> do
            print (args !! 0)
            interp code nextInd
        
        5 -> let
                jump = args !! 0 /= 0
                goTo = args !! 1
            in interp code (if jump then goTo else nextInd)
        
        6 -> let
                jump = args !! 0 == 0
                goTo = args !! 1
            in interp code (if jump then goTo else nextInd)
        
        7 -> let
                store = if args !! 0 < args !! 1 then 1 else 0
                ind = code !! (at + 3)
            in interp (upd code ind store) nextInd
        
        8 -> let
                store = if args !! 0 == args !! 1 then 1 else 0
                ind = code !! (at + 3)
            in interp (upd code ind store) nextInd
        
        99 -> pure (code, at)
        
        _ -> do pure ([], -1)

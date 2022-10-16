
module Intcode (interp) where

import System.Exit
import Debug.Trace

upd :: [a] -> Int -> a -> [a]
upd l pos n = take pos l ++ [n] ++ drop (pos + 1) l

get :: [Int] -> Int -> Int
get code arg = code !! (code !! arg)

interp :: [Int] -> Int -> ([Int], Int)
interp code at =
    case code !! at of
        1 -> let
                res = get code (at + 1) + get code (at + 2)
                ind = code !! (at + 3)
            in
                interp (upd code ind res) (at + 4)
        2 -> let
                res = get code (at + 1) * get code (at + 2)
                ind = code !! (at + 3)
            in
                interp (upd code ind res) (at + 4)
        99 -> (code, at)
        _ -> do
            ([], -1)

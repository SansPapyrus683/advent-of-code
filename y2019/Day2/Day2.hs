import Text.Printf
import Control.Monad (filterM)

import Intcode (interp)
import Utils (split)

main = do
    file <- readFile "day2/day2.txt"

    let code :: [Int] = map read (split file ',')

    let
        replacedEval :: Int -> Int -> IO [Int]
        replacedEval noun verb = do
            (res, _) <-
                    interp ([head code] ++ [noun, verb] ++ drop 3 code) 0
            pure res

    res <- replacedEval 12 2
    printf "first element after running: %d\n" (head res)

    let target :: Int = 19690720
    let
        foundTarget :: (Int, Int) -> IO Bool
        foundTarget (noun, verb) = do
            res <- replacedEval noun verb
            pure (head res == target)

    let range = [0..99]
    let allPairs :: [(Int, Int)] = [(x, y) | x <- range, y <- range]
    validPairs <- filterM foundTarget allPairs

    let x = head validPairs
    printf "id of pair that gives %d: %d\n" target (fst x * 100 + snd x)

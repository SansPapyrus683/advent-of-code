import Intcode (interp)
import Utils (split)

import Text.Printf

main = do
    file <- readFile "day2/day2.txt"

    let code :: [Int] = map read (split file ',')

    let
        replacedEval :: Int -> Int -> [Int]
        replacedEval noun verb = res
            where (res, _) =
                    interp ([head code] ++ [noun, verb] ++ drop 3 code) 0

    printf "first element after running: %d\n" (head (replacedEval 12 2))

    let target :: Int = 19690720
    let
        foundTarget :: (Int, Int) -> Bool
        foundTarget (noun, verb) =  head (replacedEval noun verb) == target

    let range = [0..99]
    let
        allPairs :: [(Int, Int)] = [(x, y) | x <- range, y <- range]
        x :: (Int, Int) = head (filter foundTarget allPairs)
    printf "id of pair that gives %d: %d\n" target (fst x * 100 + snd x)

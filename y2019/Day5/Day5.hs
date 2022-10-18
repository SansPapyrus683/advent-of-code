import Intcode (interp)
import Utils (split)

import Text.Printf
import Control.Monad (filterM)

main = do
    file <- readFile "day5/day5.txt"

    let code :: [Int] = map read (split file ',')

    interp code 0 -- provide 1 for p1, provide 5 for p2

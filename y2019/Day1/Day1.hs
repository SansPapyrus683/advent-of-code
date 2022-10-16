import System.IO
import Data.Char
import Text.Printf

main = do
    file <- readFile "day1/day1.txt"
    let masses :: [Integer] = map read (lines file)

    let needed m = max (m `div` 3 - 2) 0;
    let fuelSum1 = sum (map needed masses);

    printf "amt of fuel needed for modules (p1): %d\n" fuelSum1

    let totalNeeded m = if m == 0 then 0
                        else (let f = needed m in f + totalNeeded f)
    let fuelSum2 = sum (map totalNeeded masses);
    printf "amt of fuel needed for modules (p2): %d\n" fuelSum2

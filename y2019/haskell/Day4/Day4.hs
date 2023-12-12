import Data.Char
import Data.List
import Text.Printf
import Debug.Trace

twoAdj :: (Eq a) => [a] -> Bool
twoAdj [x] = False
twoAdj l = head l == (l !! 1) || twoAdj (drop 1 l)

isValidP1 :: Int -> Bool
isValidP1 pw = 
    let
        str = show pw
        digits :: [Int] = map digitToInt str
    in length str == 6 && sort digits == digits && twoAdj digits

justTwoAdj :: (Eq a) => [a] -> Maybe a -> Bool
justTwoAdj [x] _ = False
justTwoAdj l prev = 
    let
        curr = head l
        next = l !! 1
        isPrev = case prev of
            Just v -> curr == v
            Nothing -> False
        notNext = (length l <= 2 || next /= l !! 2)
    in (not isPrev && curr == next && notNext) || justTwoAdj (drop 1 l) (Just curr)

isValidP2 :: Int -> Bool
isValidP2 pw = 
    let
        str = show pw
        digits :: [Int] = map digitToInt str
    in length str == 6 && sort digits == digits && justTwoAdj digits Nothing

main = do
    let range = [273025..767253]  -- change this to be your input

    let validNum1 = filter isValidP1 range
    printf "# of valid pws (p1): %d\n" (length validNum1)

    let validNum2 = filter isValidP2 range
    printf "# of valid pws (p1): %d\n" (length validNum2)

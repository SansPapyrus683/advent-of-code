import qualified Data.Set as Set
import Text.Printf
import Utils

data Direction = DUp | DDown | DLeft | DRight deriving (Eq, Enum, Show)

parseDirection :: Char -> Direction
parseDirection d
    | d == 'U' = DUp
    | d == 'D' = DDown
    | d == 'L' = DLeft
    | d == 'R' = DRight

dirChange :: Direction -> (Int, Int)
dirChange d
    | d == DUp = (0, 1)
    | d == DDown = (0, -1)
    | d == DLeft = (-1, 0)
    | d == DRight = (1, 0)

parseWire :: String -> (Direction, Int)
parseWire w = (parseDirection (head (take 1 w)), read (drop 1 w))

allPoints :: (Int, Int) -> [(Direction, Int)] -> [(Int, Int)]
allPoints _ [] = []
allPoints (x, y) directions =
    let
        i = head directions
        (dirX, dirY) = dirChange (fst i)
        next = [(x + dirX * d, y + dirY * d) | d <- [1..snd i]]
    in (x, y) : init next ++ allPoints (last next) (tail directions)

taxiDist :: (Int, Int) -> Int
taxiDist (x, y) = abs x + abs y

smallestSum :: [(Int, Int)] -> Int
smallestSum pts = minimum (map taxiDist pts)

main = do
    file <- readFile "day3/day3.txt"
    let fileLines = lines file

    let wire1 = map parseWire (split (fileLines !! 0) ',')
    let wire2 = map parseWire (split (fileLines !! 1) ',')

    let start = (0, 0)
    let wire1Pts = allPoints start wire1
    let wire2Pts = allPoints start wire2

    let crossings = Set.toList
            (Set.delete start
            (Set.intersection (Set.fromList wire1Pts) (Set.fromList wire2Pts)))

    printf "closest crossing: %d\n" (smallestSum crossings)

    let dist1 = map (`position` wire1Pts) crossings
    let dist2 = map (`position` wire2Pts) crossings
    let combinedDist = zipWith(+) dist1 dist2

    printf "closest crossing by wire distance: %d\n" (minimum combinedDist)

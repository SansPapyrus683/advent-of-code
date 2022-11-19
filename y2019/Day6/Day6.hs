import System.IO
import Data.Map.Strict (Map)
import qualified Data.Map.Strict as M
import Data.Maybe (fromMaybe, fromJust)
import Text.Printf

import Utils (split)

orbitNum :: Map String [String] -> String -> Maybe Int -> Int
orbitNum orbitTree at depth =
    let
        actualD = fromMaybe 0 depth
        newDepth = actualD + 1
        orbitees :: [String] = fromMaybe [] (orbitTree M.!? at)
        childDepths = [orbitNum orbitTree p (Just newDepth) | p <- orbitees]
    in actualD + sum childDepths

pathToRoot :: Map String String -> String -> String -> Maybe [String] -> [String]
pathToRoot tree at target path = 
    let
        actualP = fromMaybe [] path ++ [at]
        parent = fromJust (tree M.!? at)
    in if at == target
        then actualP
        else actualP ++ pathToRoot tree parent target path

removeSuffixes :: (Eq a) => [a] -> [a] -> ([a], [a])
removeSuffixes l1 l2 =
    if last l1 == last l2
        then removeSuffixes (init l1) (init l2)
        else (l1, l2)

main = do
    file <- readFile "day6/day6.txt"
    -- haskell you're so stupid istg
    let parseOrbit :: String -> (String, [String])
        parseOrbit o = let so = split o ')' in (so !! 0, [so !! 1])
        orbits = map parseOrbit (lines file)
        reverseOrbits = map (\(a, b) -> (head b, a)) orbits

    let combine a b = [head a, head b]
    let orbitTree = M.fromListWith combine orbits
    let orbitParents = M.fromList reverseOrbits

    let root = "COM"
        you = "YOU"
        santa = "SAN"

    printf "total # of orbits: %d\n" (orbitNum orbitTree root Nothing)

    let youPath = pathToRoot orbitParents you root Nothing
        santaPath = pathToRoot orbitParents santa root Nothing

    let (youUnique, santaUnique) = removeSuffixes youPath santaPath
    printf "# of orbital transfers needed: %d\n"
        (length youUnique + length santaUnique - 2)

module Utils where

import Data.Char ( isSpace )
import Data.List ( dropWhileEnd, elemIndex )

-- THEY TOOK MY SPLIT FUNCTION, CAN'T HAVE CRAP IN DETROIT
split :: String -> Char -> [String]
split str delim =
        case break (== delim) str of
            (a, _:b) -> a : split b delim
            (a, _)   -> [a]

position :: Eq a => a -> [a] -> Int
position i l =
    case i `elemIndex` l of
       Just n  -> n
       Nothing -> -1

trim = dropWhileEnd isSpace . dropWhile isSpace

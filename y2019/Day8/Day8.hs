import Utils (trim)

getLayers :: String -> (Int, Int) -> []

main = do
    file <- readFile "day8/day8.txt"
    let img = trim file

    let dim = (2, 3)

    let layers = length img `div` uncurry (*) dim

    pure 69

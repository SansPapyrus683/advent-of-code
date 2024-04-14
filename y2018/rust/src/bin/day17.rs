use regex::Regex;
use std::collections::HashSet;
use std::fs;

const WATER: (usize, usize) = (0, 500);

#[derive(Copy, Clone, Eq, PartialEq)]
enum Tile {
    Clay,
    Sand,
    Still,
    Flow,
}

fn main() {
    let xy_fmt = Regex::new(r"x=(\d+),\s+y=(\d+)\.\.(\d+)").unwrap();
    let yx_fmt = Regex::new(r"y=(\d+),\s+x=(\d+)\.\.(\d+)").unwrap();
    let mut clay = HashSet::new();
    for line in fs::read_to_string("../input/day17.txt").unwrap().lines() {
        if let Some(m) = xy_fmt.captures(line) {
            let (x, ys, ye) = (
                m[1].parse::<usize>().unwrap(),
                m[2].parse::<usize>().unwrap(),
                m[3].parse::<usize>().unwrap(),
            );
            for y in ys..=ye {
                clay.insert((y, x));
            }
        } else if let Some(m) = yx_fmt.captures(line) {
            let (y, xs, xe) = (
                m[1].parse::<usize>().unwrap(),
                m[2].parse::<usize>().unwrap(),
                m[3].parse::<usize>().unwrap(),
            );
            for x in xs..=xe {
                clay.insert((y, x));
            }
        }
    }

    // all of this is from the python version, i'm just redoing it in rust here
    let mut max_r = WATER.0;
    let mut min_c = WATER.1;
    let mut max_c = WATER.1;
    clay.iter().for_each(|(y, x)| {
        max_r = max_r.max(*y);
        min_c = min_c.min(*x);
        max_c = max_c.max(*x);
    });

    let mut grid = vec![vec![Tile::Sand; max_c - min_c + 3]; max_r + 2];
    clay.iter()
        .for_each(|c| grid[c.0][c.1 - min_c + 1] = Tile::Clay);

    let blocking = vec![Tile::Clay, Tile::Still];
    let mut todo = vec![(WATER.0, WATER.1 - min_c + 1, true)];
    let mut seen = HashSet::new();
    while !todo.is_empty() {
        let curr = todo.pop().unwrap();
        if seen.contains(&curr) {
            continue;
        }
        seen.insert(curr);
        let (mut r, c, type_) = curr;
        if type_ {
            while r <= max_r && !blocking.contains(&grid[r + 1][c]) {
                grid[r][c] = Tile::Flow;
                r += 1;
            }
            if r <= max_r {
                grid[r][c] = Tile::Flow;
                todo.push((r, c, false));
            }
        } else {
            let mut c_left = c;
            while blocking.contains(&grid[r + 1][c_left]) && grid[r][c_left - 1] != Tile::Clay {
                c_left -= 1;
            }

            let mut c_right = c;
            while blocking.contains(&grid[r + 1][c_right]) && grid[r][c_right + 1] != Tile::Clay {
                c_right += 1;
            }

            let left_wall = c_left > 0 && grid[r][c_left - 1] == Tile::Clay;
            let right_wall = c_right + 1 < grid[r].len() && grid[r][c_right + 1] == Tile::Clay;
            if left_wall && right_wall {
                for fill_c in c_left..=c_right {
                    grid[r][fill_c] = Tile::Still;
                }
                if r != 0 {
                    todo.push((r - 1, c, false));
                }
            } else {
                for fill_c in c_left..=c_right {
                    grid[r][fill_c] = Tile::Flow;
                }
                if !left_wall {
                    todo.push((r, c_left, true));
                }
                if !right_wall {
                    todo.push((r, c_right, true));
                }
            }
        }
    }

    let highest_clay = clay.iter().min_by_key(|c| c.0).unwrap().0 as u32;
    let flowing = grid
        .iter()
        .flat_map(|r| r)
        .map(|t| (*t == Tile::Flow) as u32)
        .sum::<u32>()
        - highest_clay;
    let still = grid
        .iter()
        .flat_map(|r| r)
        .map(|t| (*t == Tile::Still) as u32)
        .sum::<u32>();

    println!("total water (while flowing): {}", flowing + still);
    println!("total water (while still): {still}");
}

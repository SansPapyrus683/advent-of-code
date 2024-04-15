use std::collections::HashMap;
use std::fs;

const P1_TIME: usize = 10;
const P2_TIME: usize = 1e9 as usize;

#[derive(Debug, Eq, PartialEq, Hash, Copy, Clone)]
enum Cell {
    Open,
    Trees,
    Yard,
}

fn neighbors(r: i32, c: i32) -> Vec<(i32, i32)> {
    vec![
        (r + 1, c),
        (r - 1, c),
        (r, c + 1),
        (r, c - 1),
        (r + 1, c + 1),
        (r + 1, c - 1),
        (r - 1, c + 1),
        (r - 1, c - 1),
    ]
}

fn resource_value(grid: &Vec<Vec<Cell>>) -> u32 {
    let mut tree_num = 0;
    let mut yard_num = 0;
    for c in grid.iter().flatten() {
        match c {
            Cell::Trees => tree_num += 1,
            Cell::Yard => yard_num += 1,
            _ => ()
        }
    }
    tree_num * yard_num
}

fn main() {
    let mut grid: Vec<Vec<_>> = fs::read_to_string("../input/day18.txt")
        .unwrap()
        .lines()
        .map(|r| {
            r.chars()
                .map(|c| match c {
                    '#' => Cell::Yard,
                    '|' => Cell::Trees,
                    _ => Cell::Open,
                })
                .collect()
        })
        .collect();

    let mut time = 0;
    let cyc_start;
    let mut seen = HashMap::from([(grid.clone(), time)]);
    let mut order = vec![grid.clone()];
    loop {
        let mut new_grid = vec![vec![Cell::Open; grid[0].len()]; grid.len()];
        for r in 0..grid.len() {
            for c in 0..grid[r].len() {
                let mut tree_amt = 0;
                let mut yard_amt = 0;
                for (nr, nc) in neighbors(r as i32, c as i32) {
                    if 0 <= nr
                        && nr < grid.len() as i32
                        && 0 <= nc
                        && nc < grid[nr as usize].len() as i32
                    {
                        match grid[nr as usize][nc as usize] {
                            Cell::Trees => tree_amt += 1,
                            Cell::Yard => yard_amt += 1,
                            _ => ()
                        }
                    }
                }

                new_grid[r][c] = grid[r][c];
                match grid[r][c] {
                    Cell::Open => {
                        if tree_amt >= 3 {
                            new_grid[r][c] = Cell::Trees;
                        }
                    }
                    Cell::Trees => {
                        if yard_amt >= 3 {
                            new_grid[r][c] = Cell::Yard;
                        }
                    }
                    Cell::Yard => {
                        if !(tree_amt > 0 && yard_amt > 0) {
                            new_grid[r][c] = Cell::Open;
                        }
                    }
                }
            }
        }

        time += 1;
        grid = new_grid;

        if time == P1_TIME {
            println!("resource value after {P1_TIME} mins: {}", resource_value(&grid));
        }

        if seen.contains_key(&grid) {
            cyc_start = seen[&grid];
            break;
        }
        order.push(grid.clone());
        seen.insert(grid.clone(), time);
    }

    let cyc_len = seen.len() - cyc_start;
    let equal_to = cyc_start + ((P2_TIME - cyc_start) % cyc_len);
    let p2_result = &order[equal_to];
    println!("resource value after {P2_TIME} mins: {}", resource_value(p2_result));
}

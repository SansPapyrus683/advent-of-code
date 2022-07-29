use std::fs;

const LIT: char = '#';
const UNLIT: char = '.';
const STEPS: u32 = 100;

fn neighbors(r: i32, c: i32) -> Vec<(i32, i32)> {
    return vec![
        (r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1),
        (r + 1, c + 1), (r + 1, c - 1), (r - 1, c + 1), (r - 1, c - 1)
    ];
}

fn main() {
    let read = fs::read_to_string("src/input.txt").expect("you done messed up");
    let mut lights = Vec::new();
    let mut cols = 0;
    for r in read.lines() {
        let mut row = Vec::new();
        for c in r.chars() {
            assert!(c == LIT || c == UNLIT);
            row.push(c == LIT);
        }
        
        assert!(cols == 0 || cols == row.len());
        if cols == 0 {
            cols = row.len();
        }
        lights.push(row);
    }
    let rows = lights.len();

    let mut lights1 = lights.clone();
    let mut lights2 = lights.clone();

    // the corners in p2 are always lit
    lights2[0][0] = true;
    lights2[0][cols - 1] = true;
    lights2[rows - 1][0] = true;
    lights2[rows - 1][cols - 1] = true;
    
    for _ in 0..STEPS {
        let prev_l1 = lights1.clone();
        let prev_l2 = lights2.clone();
        for r in 0..rows {
            for c in 0..cols {
                let mut lit1 = 0;
                let mut lit2 = 0;
                for (nr, nc) in neighbors(r as i32, c as i32) {
                    if nr < 0 || nr >= rows as i32
                        || nc < 0 || nc >= cols as i32 {
                        continue;
                    }
                    let (nnr, nnc) = (nr as usize, nc as usize);
                    lit1 += prev_l1[nnr][nnc] as u32;
                    lit2 += prev_l2[nnr][nnc] as u32;
                }

                // calculate the stuff for p1
                if lights1[r][c] {
                    lights1[r][c] = lit1 == 2 || lit1 == 3;
                } else {
                    lights1[r][c] = lit1 == 3;
                }

                // and do basically the same stuff for p2
                let corner = (r == 0 || r == rows - 1) && (c == 0 || c == cols - 1);
                if !lights2[r][c] {
                    lights2[r][c] = lit2 == 3;
                } else if !corner {
                    lights2[r][c] = lit2 == 2 || lit2 == 3;
                }
            }
        }
    }

    let mut total_lit1 = 0;
    let mut total_lit2 = 0;
    for r in 0..rows {
        for c in 0..cols {
            total_lit1 += lights1[r][c] as u32;
            total_lit2 += lights2[r][c] as u32;
        }
    }
    
    println!("number of lit lights (p1): {total_lit1}");
    println!("number of lit lights (p2): {total_lit2}");
}

use std::cmp::min;

const SERIAL_NUM: i32 = 9005;
const WIDTH: usize = 300;
const P1_SUB_WIDTH: usize = 3;

// no clue if the arguments this takes are appropriate, but who cares
fn power_level(x: usize, y: usize) -> i32 {
    let rack_id = x + 10;
    ((rack_id * y + SERIAL_NUM as usize) * rack_id / 100 % 10) as i32 - 5
}

fn main() {
    let mut pref_grid = vec![vec![0; (WIDTH + 1) as usize]; (WIDTH + 1) as usize];
    for y in 1..=WIDTH {
        for x in 1..=WIDTH {
            pref_grid[y][x] = pref_grid[y - 1][x] + pref_grid[y][x - 1] - pref_grid[y - 1][x - 1]
                + power_level(x, y);
        }
    }

    let mut p1_most_power = ((0, 0), i32::MIN);
    let mut p2_most_power = ((0, 0, 0), i32::MIN);
    for sx in 1..=WIDTH {
        for sy in 1..=WIDTH {
            let max_width = min(WIDTH - sx + 1, WIDTH - sy + 1);
            for width in 1..=max_width {
                let power = pref_grid[sy + width - 1][sx + width - 1]
                    - pref_grid[sy - 1][sx + width - 1]
                    - pref_grid[sy + width - 1][sx - 1]
                    + pref_grid[sy - 1][sx - 1];

                if width == P1_SUB_WIDTH && power > p1_most_power.1 {
                    p1_most_power = ((sx, sy), power);
                }
                if power > p2_most_power.1 {
                    p2_most_power = ((sx, sy, width), power);
                }
            }
        }
    }

    println!("identifier for p1: {:?}", p1_most_power.0);
    println!("identifier for p2: {:?}", p2_most_power.0);
}

use std::fs;

fn main() {
    let read = fs::read_to_string("input/day1.txt").expect("you done messed up");
    // let lines: Vec<&str> = fstr.split_whitespace().collect();

    let mut floor = 0;
    let mut entered_basement = false;
    for (i, c) in read.chars().enumerate() {
        match c {
            '(' => floor += 1,
            ')' => floor -= 1,
            _ => ()
        }
        if floor < 0 && !entered_basement {
            println!("we first enter the basement at pos {}", i + 1);
            entered_basement = true;
        }
    }
    println!("final floor: {floor}");
}

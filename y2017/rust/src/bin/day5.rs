use std::fs;

fn main() {
    let prog: Vec<_> = fs::read_to_string("../input/day5.txt")
        .expect("bruh")
        .lines()
        .map(|i| i.parse::<i32>().unwrap())
        .collect();

    let mut prog1 = prog.to_vec();
    let mut at = 0;
    let mut steps = 0;
    while 0 <= at && at < prog1.len() as i32 {
        let prev = at;
        at += prog1[at as usize];
        prog1[prev as usize] += 1;
        steps += 1;
    }
    println!("# of steps to complete (p1): {steps}");

    let mut prog2 = prog.to_vec();
    at = 0;
    steps = 0;
    while 0 <= at && at < prog2.len() as i32 {
        let prev = at;
        let offset = prog2[at as usize];
        at += offset;
        prog2[prev as usize] += if offset >= 3 { -1 } else { 1 };
        steps += 1;
    }
    println!("# of steps to complete (p2): {steps}");
}

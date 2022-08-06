const POS: (u32, u32) = (3010, 3019);
const START: i32 = 20151125;

fn next_val(curr: i32) -> i32 {
    // just change these numbers as you see
    (curr as i64 * 252533 % 33554393) as i32
}

fn next_pos(pos: &(u32, u32)) -> (u32, u32) {
    if pos.0 == 1 {
        (pos.1 + 1, 1)
    } else {
        (pos.0 - 1, pos.1 + 1)
    }
}

fn main() {
    let mut at = (1, 1);
    // this should be big enough
    let mut paper = vec![vec![-1; POS.1 as usize * 3]; POS.0 as usize * 3];

    paper[at.0 as usize][at.1 as usize] = START;
    let mut prev = at;
    at = next_pos(&at);
    while paper[POS.0 as usize][POS.1 as usize] == -1 {
        paper[at.0 as usize][at.1 as usize] = next_val(
            paper[prev.0 as usize][prev.1 as usize]
        );
        prev = at;
        at = next_pos(&at);
    }

    println!("machine code: {}", paper[POS.0 as usize][POS.1 as usize])
}

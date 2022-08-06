use ndarray::prelude::*;

const POS: (usize, usize) = (3010, 3019);
const START: i32 = 20151125;

fn next_val(curr: i32) -> i32 {
    // just change these numbers as you see
    (curr as i64 * 252533 % 33554393) as i32
}

fn next_pos(pos: &(usize, usize)) -> (usize, usize) {
    if pos.0 == 1 {
        (pos.1 + 1, 1)
    } else {
        (pos.0 - 1, pos.1 + 1)
    }
}

fn main() {
    // this should be big enough
    let mut paper = Array::<i32, _>::zeros((POS.0 * 3, POS.1 * 3));

    let mut at = (1, 1);
    paper[[at.0, at.1]] = START;
    while at != POS {
        let next = next_pos(&at);
        paper[[next.0, next.1]] = next_val(paper[[at.0, at.1]]);
        at = next;
    }

    println!("machine code: {}", paper[[POS.0, POS.1]])
}

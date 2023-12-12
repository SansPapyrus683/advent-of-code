const A_START: u64 = 116;
const B_START: u64 = 299;
const BITS_TAKEN: u8 = 16;

const P1_SIM_NUM: u32 = 40e6 as u32;
const P2_SIM_NUM: u32 = 5e6 as u32;

enum GenMode { P1, P2 }

fn a_next(mut a: u64, mode: &GenMode) -> u64 {
    fn single_next(a: u64) -> u64 { a * 16807 % 2147483647 }
    match mode {
        GenMode::P1 => { },
        GenMode::P2 => while single_next(a) % 4 != 0 { a = single_next(a); }
    };
    single_next(a)
}

fn b_next(mut b: u64, mode: &GenMode) -> u64 {
    fn single_next(b: u64) -> u64 { b * 48271 % 2147483647 }
    match mode {
        GenMode::P1 => { },
        GenMode::P2 => while single_next(b) % 8 != 0 { b = single_next(b); }
    };
    single_next(b)
}

fn main() {
    let mut a = A_START;
    let mut b = B_START;
    let mut total = 0;
    for _ in 0..P1_SIM_NUM {
        a = a_next(a, &GenMode::P1);
        b = b_next(b, &GenMode::P1);
        if a & ((1 << BITS_TAKEN) - 1) == b & ((1 << BITS_TAKEN) - 1) {
            total += 1;
        }
    }
    println!("# of matching pairs (p1): {total}");

    let mut a = A_START;
    let mut b = B_START;
    let mut total = 0;
    for _ in 0..P2_SIM_NUM {
        a = a_next(a, &GenMode::P2);
        b = b_next(b, &GenMode::P2);
        if a & ((1 << BITS_TAKEN) - 1) == b & ((1 << BITS_TAKEN) - 1) {
            total += 1;
        }
    }
    println!("# of matching pairs (p2): {total}");
}

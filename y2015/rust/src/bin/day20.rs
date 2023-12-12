const PRESENT_NUM: u32 = 34000000;
const P1_AMT: u32 = 10;
const P2_AMT: u32 = 11;
const P2_CAP: u32 = 50;

fn elf_numbers(n: u32, cap: u32) -> Vec<u32> {
    assert!(n > 0);
    let sqrt = (n as f64).sqrt() as u32;
    let ccap = if cap == 0 { u32::MAX } else { cap };

    let mut ret = Vec::new();
    for i in 1..=sqrt {
        if n % i == 0 {
            let div_res = n / i;
            if div_res <= ccap {
                ret.push(i);
            }
            if div_res != i && i <= ccap {
                ret.push(div_res);
            }
        }
    }
    ret
}

fn main() {
    let mut p1_min = 0;
    let mut p2_min = 0;
    let mut at = 1;
    loop {
        if elf_numbers(at, 0).iter().sum::<u32>() * P1_AMT >= PRESENT_NUM
            && p1_min == 0 {
            p1_min = at;
        }
        if elf_numbers(at, P2_CAP).iter().sum::<u32>() * P2_AMT >= PRESENT_NUM
            && p2_min == 0 {
            p2_min = at;
        }
        if p1_min != 0 && p2_min != 0 {
            break;
        }
        at += 1;
    }

    println!("closest house to get {PRESENT_NUM} presents (p1): {p1_min}");
    println!("closest house to get {PRESENT_NUM} presents (p2): {p2_min}");
}

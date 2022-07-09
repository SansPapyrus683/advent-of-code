use std::collections::HashSet;

const PW: &str = "vzbxkghb";

fn inc(num: &mut Vec<i32>, base: u32) {
    let cmp_base = base as i32;
    let len = num.len();
    num[len - 1] += 1;
    for i in (0..len).rev() {
        if num[i] >= cmp_base {
            num[i - 1] += num[i] / cmp_base;
            num[i] %= cmp_base;
        }
    }
}

fn to_pw(num: &Vec<i32>) -> String {
    let mut res = "".to_string();
    for n in num {
        res.push((b'a' + *n as u8) as char);
    }
    res
}

fn valid(pw: String) -> bool {
    let invalid = ['i', 'o', 'l'];

    let mut consec3 = false;
    let mut seen_pairs = HashSet::new();
    let mut prev = '█';  // won't be used
    let mut pprev = prev;
    for (i, c) in pw.chars().enumerate() {
        if invalid.iter().any(|i| *i == c) {
            return false;
        }
        if i > 2 && pprev as u8 + 1 == prev as u8 && prev as u8 + 1 == c as u8 {
            consec3 = true;
        }
        if i > 0 && c == prev {
            seen_pairs.insert(c);
        }
        pprev = prev;
        prev = c;
    }
    consec3 && seen_pairs.len() >= 2
}

fn main() {
    let mut pw_num = Vec::new();
    for c in PW.chars() {
        pw_num.push(c as i32 - 'a' as i32);
    }

    while !valid(to_pw(&pw_num)) {
        inc(&mut pw_num, 26);
    }
    println!("first valid pw after initial state: {}", to_pw(&pw_num));

    inc(&mut pw_num, 26);
    while !valid(to_pw(&pw_num)) {
        inc(&mut pw_num, 26);
    }
    println!("second valid pw after initial state: {}", to_pw(&pw_num));
}

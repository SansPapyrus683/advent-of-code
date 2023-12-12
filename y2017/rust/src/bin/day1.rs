use std::fs;

fn main() {
    let mut digits = fs::read_to_string("input/day1.txt").expect("bruh");
    digits = digits.trim().parse().unwrap();

    let digit_vec: Vec<char> = digits.chars().collect();

    let mut p1_total = 0;
    let mut p2_total = 0;
    for i in 0..digits.len() {
        let next1 = (i + 1) % digits.len();
        if digit_vec[i] == digit_vec[next1] {
            p1_total += digit_vec[i].to_digit(10).unwrap_or(0);
        }

        let next2 = (i + digits.len() / 2) % digits.len();
        if digit_vec[i] == digit_vec[next2] {
            p2_total += digit_vec[i].to_digit(10).unwrap_or(0);
        }
    }

    println!("solution to p1 captcha: {p1_total}");
    println!("solution to p2 captcha: {p2_total}");
}

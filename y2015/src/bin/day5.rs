use std::fs;
use std::collections::HashSet;

const VOWELS: &str = "aeiou";
const INVALID: [&str; 4] = ["ab", "cd", "pq", "xy"];

fn p1_nice(s: &str) -> bool {
    let mut vowel_count = 0;
    let mut has_double = false;
    let mut prev = '█';
    for (i, c) in s.chars().enumerate() {
        vowel_count += if VOWELS.contains(c) { 1 } else { 0 };
        if i > 0 && c == prev {
            has_double = true;
        }
        prev = c;
    }

    if vowel_count < 3 || !has_double {
        return false;
    }

    for bad in INVALID {
        if s.contains(bad) {
            return false;
        }
    }
    true
}

fn p2_nice(s: &str) -> bool {
    let mut dbl_dbl = false;
    let mut sandwich = false;

    let mut seen_doubles = HashSet::new();
    let mut prev = ('█', '█');

    for (i, c) in s.chars().enumerate() {
        if i >= 2 && prev.0 == c {
            sandwich = true;
        }
        if i > 2 && seen_doubles.contains(&(prev.1, c)) {
            dbl_dbl = true;
        }

        if i >= 2 {
            seen_doubles.insert(prev);
        }
        prev.0 = prev.1;
        prev.1 = c;
    }

    return dbl_dbl && sandwich;
}

fn main() {
    let read = fs::read_to_string("input/day5.txt").expect("bruh");
    let str_list: Vec<&str> = read.lines().into_iter().collect();

    let mut p1_nice_num = 0;
    let mut p2_nice_num = 0;
    for s in &str_list {
        p1_nice_num += p1_nice(s) as i32;
        p2_nice_num += p2_nice(s) as i32;
    }

    println!("p1 nice string number: {p1_nice_num}");
    println!("p2 nice string number: {p2_nice_num}");
}

use std::fs;
use std::collections::{HashSet, HashMap};

fn valid_phrases1<S: AsRef<str>>(phrase: S) -> bool {
    let mut seen = HashSet::new();
    for p in phrase.as_ref().split_whitespace() {
        if seen.contains(p) {
            return false;
        }
        seen.insert(p);
    }
    true
}

fn valid_phrases2<S: AsRef<str>>(phrase: S) -> bool {
    let phrase = phrase.as_ref().to_lowercase();
    assert!(phrase.chars().all(|c| c.is_alphabetic() || c.is_whitespace()));

    fn str_occ_num(s: &str) -> [u32; 26] {
        let mut occs = [0; 26];
        for c in s.chars() {
            occs[c as usize - 'a' as usize] += 1;
        }
        occs
    }

    let mut seen = HashSet::new();
    for p in phrase.split_whitespace() {
        if !seen.insert(str_occ_num(p)) {
            return false;
        }
    }
    true
}

fn main() {
    let lines = fs::read_to_string("../input/day4.txt").expect("bruh");

    let mut valid1 = 0;
    let mut valid2 = 0;
    for p in lines.lines() {
        valid1 += if valid_phrases1(p) { 1 } else { 0 };
        valid2 += if valid_phrases2(p) { 1 } else { 0 };
    }

    println!("# of valid passphrases (p1): {valid1}");
    println!("# of valid passphrases (p2): {valid2}");
}

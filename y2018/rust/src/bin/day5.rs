use std::fs;

fn react(polymer: &String) -> String {
    let mut new_poly = Vec::new();
    let can_react = |poly: &Vec<u8>| {
        if poly.len() <= 1 {
            return false;
        }
        let curr = poly[poly.len() - 1];
        let prev = poly[poly.len() - 2];
        return curr.to_ascii_uppercase() == prev.to_ascii_uppercase() && curr != prev;
    };
    for c in polymer.bytes() {
        new_poly.push(c);
        while can_react(&new_poly) {
            new_poly.pop();
            new_poly.pop();
        }
    }
    return String::from_utf8(new_poly).unwrap();
}

fn main() {
    let polymer = fs::read_to_string("../input/day5.txt")
        .unwrap()
        .trim()
        .to_owned();

    let reacted = react(&polymer);
    println!("length of polymer after reaction: {}", reacted.len());

    let mut min_len = usize::MAX;
    for i in 'a'..='z' {
        let stripped_poly = polymer
            .chars()
            .filter(|c| !c.eq_ignore_ascii_case(&i))
            .collect::<String>();
        min_len = min_len.min(react(&stripped_poly).len());
    }

    println!("min length of remaining polymer: {min_len}");
}

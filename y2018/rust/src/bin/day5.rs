use std::fs;

fn react(polymer: &String) -> String {
    let mut poly = polymer.as_bytes().to_vec();
    let mut react_done = false;
    while !react_done {
        react_done = true;
        let mut new_poly = Vec::new();
        let mut at = 0;
        while at < poly.len() - 1 {
            let curr = poly[at];
            let next = poly[at + 1];
            if curr.to_ascii_uppercase() == next.to_ascii_uppercase() && curr != next {
                at += 1;
                react_done = false;
            } else {
                new_poly.push(curr);
            }
            at += 1;
        }
        if at == poly.len() - 1 {
            new_poly.push(poly[at]);
        }
        poly = new_poly;
    }
    return String::from_utf8(poly).unwrap();
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

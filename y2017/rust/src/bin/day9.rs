use std::collections::HashSet;
use std::fs;

fn main() {
    let stream = fs::read_to_string("../input/day9.txt")
        .expect("bruh")
        .trim().to_string();

    let chars: Vec<char> = stream.chars().collect();  // stupid
    let mut at = 0;
    let mut invalid = HashSet::new();
    while at < stream.len() {
        if chars[at] == '!' {
            invalid.insert(at);
            invalid.insert(at + 1);
            at += 1;
        }
        at += 1;
    }

    let mut no_ignored = String::new();
    for i in 0..stream.len() {
        if !invalid.contains(&i) {
            no_ignored.push(chars[i]);
        }
    }

    let chars: Vec<char> = no_ignored.chars().collect();
    let mut no_trash = String::new();
    let mut trash_amt = 0;
    at = 0;
    while at < no_ignored.len() {
        if chars[at] == '<' {
            while chars[at] != '>' {
                trash_amt += 1;
                at += 1;
            }
            trash_amt -= 1;  // the opening char doesn't count
            at += 1;
        }
        if at >= no_ignored.len() {  // if we end on a trash block
            break;
        }
        no_trash.push(chars[at]);
        at += 1;
    }

    let mut score = 0;
    let mut depth = 0;
    for c in no_trash.chars() {
        match c {
            '{' => depth += 1,
            '}' => {
                score += depth;
                depth -= 1;
            }
            _ => {}
        }
    }

    println!("score: {score}");
    println!("# of trash chars: {trash_amt}");
}

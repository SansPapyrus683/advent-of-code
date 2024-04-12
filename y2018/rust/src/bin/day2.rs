use std::collections::HashMap;
use std::fs;

fn main() {
    let box_ids: Vec<_> = fs::read_to_string("../input/day2.txt")
        .unwrap()
        .split_whitespace()
        .map(|s| s.to_string())
        .collect();

    let char_freq: Vec<HashMap<char, u32>> = box_ids
        .iter()
        .map(|s| {
            s.chars().fold(HashMap::new(), |mut map, val| {
                map.entry(val).and_modify(|frq| *frq += 1).or_insert(1);
                return map;
            })
        })
        .collect();

    let three_letters = char_freq
        .iter()
        .filter(|cf| cf.values().any(|v| *v == 3))
        .count();
    let two_letters = char_freq
        .iter()
        .filter(|cf| cf.values().any(|v| *v == 2))
        .count();
    println!("checksum: {}", three_letters * two_letters);

    'search:
    for s1 in &box_ids {
        for s2 in &box_ids {
            if s1 == s2 {
                continue;
            }
            let diff_num = s1
                .chars()
                .zip(s2.chars())
                .filter(|(c1, c2)| c1 != c2)
                .count();
            if diff_num == 1 {
                let mut res = "".to_string();
                s1.chars()
                    .zip(s2.chars())
                    .filter(|(c1, c2)| c1 == c2)
                    .for_each(|(c, _)| res.push(c));
                println!("common letters: {res}");
                break 'search;
            }
        }
    }
}

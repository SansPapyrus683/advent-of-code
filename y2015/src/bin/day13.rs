use std::fs;
use std::collections::{HashSet, HashMap};
use regex::Regex;
use itertools::Itertools;

fn most_happy(
    happiness: &HashMap<String, HashMap<String, i32>>, ppl: &Vec<String>
) -> i32 {
    let len = ppl.len() as i32;
    let mut most_happy = i32::MIN;
    for order in ppl.iter().permutations(ppl.len()) {
        let mut total_change = 0;
        for i in 0..len {
            let curr = order[i as usize];
            let prev = order[((i - 1 + len) % len) as usize];
            let next = order[((i + 1) % len) as usize];
            total_change += happiness[curr][prev] + happiness[curr][next];
        }
        most_happy = most_happy.max(total_change);
    }
    most_happy
}

fn main() {
    let sit_fmt = Regex::new(
        r"([a-z]+) would (lose|gain) (\d+) happiness units by sitting next to ([a-z]+)"
    ).unwrap();

    let read = fs::read_to_string("input/day13.txt").expect("bruh");
    let mut happiness: HashMap<String, HashMap<String, i32>> = HashMap::new();
    let mut people = HashSet::new();
    for p in read.lines() {
        let lp = p.to_lowercase();
        if let Some(m) = sit_fmt.captures(&lp) {
            let sgn = if &m[2] == "lose" { -1 } else { 1 };

            people.insert(m[1].to_string());
            happiness.entry(m[1].to_string()).or_default()
                .insert(m[4].to_string(), m[3].parse::<i32>().unwrap() * sgn);
        }
    }

    let mut ppl: Vec<String> = people.into_iter().collect();
    println!("best arrangement w/o mc: {}", most_happy(&happiness, &ppl));

    let me = "me".to_string();
    happiness.insert(me.clone(), HashMap::new());
    for p in &ppl {
        happiness.get_mut(p).unwrap().insert(me.clone(), 0);
        happiness.get_mut(&me).unwrap().insert(p.to_string(), 0);
    }
    ppl.push(me);
    // for some reason this part takes way too long
    println!("best arrangement w/ mc: {}", most_happy(&happiness, &ppl));
}

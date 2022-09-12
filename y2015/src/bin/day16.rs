use std::fs;
use std::collections::HashMap;
use regex::Regex;

fn main() {
    let p2_gt = vec!["cats".to_string(), "trees".to_string()];
    let p2_lt = vec!["pomeranians".to_string(), "goldfish".to_string()];

    let my_aunt = HashMap::from([
        ("children".to_string(), 3),
        ("cats".to_string(), 7),
        ("samoyeds".to_string(), 2),
        ("pomeranians".to_string(), 3),
        ("akitas".to_string(), 0),
        ("vizslas".to_string(), 0),
        ("goldfish".to_string(), 5),
        ("trees".to_string(), 3),
        ("cars".to_string(), 2),
        ("perfumes".to_string(), 1)
    ]);

    let aunt_fmt = Regex::new(r"sue (\d+): (.*)").unwrap();

    let read = fs::read_to_string("input/day16.txt").expect("bruh");

    let mut aunts: HashMap<u32, HashMap<String, u32>> = HashMap::new();
    for a in read.lines() {
        if let Some(m) = aunt_fmt.captures(&a.to_lowercase()) {
            let raw_info = m[2].split(",");
            let mut info = HashMap::new();
            for i in raw_info.into_iter() {
                let iinfo: Vec<&str> = i.trim().split(":").collect();
                let name = iinfo[0].trim();
                let amt = iinfo[1].trim().parse::<u32>().unwrap();
                info.insert(name.to_string(), amt);
            }

            let id = m[1].parse::<u32>().unwrap();
            aunts.insert(id, info);
        }
    }

    for (id, info) in &aunts {
        let mut valid = true;
        for (name, amt) in info {
            if !my_aunt.contains_key(name) || my_aunt[name] != *amt {
                valid = false;
                break;
            }
        }
        if valid {
            println!("valid aunt (part 1): {id}");
        }
    }

    for (id, info) in &aunts {
        let mut valid = true;
        for (name, amt) in info {
            if !my_aunt.contains_key(name) {
                valid = false;
            } else if p2_gt.contains(name) {
                if my_aunt[name] >= *amt {
                    valid = false;
                }
            } else if p2_lt.contains(name) {
                if my_aunt[name] <= *amt {
                    valid = false;
                }
            } else if my_aunt[name] != *amt {
                valid = false;
            }
            if !valid {
                break;
            }
        }
        if valid {
            println!("valid aunt (part 2): {id}");
            break;
        }
    }
}

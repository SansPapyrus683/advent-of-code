use std::fs;
use std::collections::{HashMap, HashSet};
use regex::Regex;

/** returns a vector of the individual atoms (i.e. HCa -> [H, Ca]) */
fn split_atoms(chem: &String) -> Vec<String> {
    let mut ret = Vec::new();
    let mut curr = "".to_string();
    for c in chem.chars() {
        if !curr.is_empty() && c.is_uppercase() {
            ret.push(curr);
            curr = "".to_string();
        }
        curr.push(c);
    }
    ret.push(curr);
    return ret;
}

fn main() {
    let rep_fmt = Regex::new("([A-Za-z]*) => ([A-Za-z]*)").unwrap();
    
    let read = fs::read_to_string("input/day19.txt").expect("you done messed up");
    let mut read_rep = true;
    let mut reps: HashMap<String, Vec<Vec<String>>> = HashMap::new();
    let mut chem = Vec::new();
    for i in read.lines() {
        if i.is_empty() {
            assert!(read_rep);
            read_rep = false;
        }
        if read_rep {
            if let Some(m) = rep_fmt.captures(i) {
                let start = m[1].to_string();
                assert!(split_atoms(&start).len() == 1);
                let res = split_atoms(&m[2].to_string());
                reps.entry(start).or_default().push(res);
            }
        } else {
            chem = split_atoms(&i.to_string());
        }
    }

    let mut possible = HashSet::new();
    for (i, c) in chem.iter().enumerate() {
        for rep_with in reps.entry(c.to_string()).or_default() {
            let left = chem.get(..i).unwrap();
            let right = chem.get((i + 1)..).unwrap_or(&[]);
            
            let mut new = Vec::new();
            new.extend_from_slice(left);
            new.append(&mut rep_with.clone());
            new.extend_from_slice(right);

            if !possible.contains(&new) {
                possible.insert(new);
            }
        }
    }

    println!("total possible replacements (pt 1): {}", possible.len());

    /*
     * followed u/askalski's sol on Reddit:
     * https://www.reddit.com/r/adventofcode/comments/3xflz8
     * (don't really understand it lmao)
     */
    let rn_amt = chem.iter().filter(|&e| *e == "Rn").count();
    let ar_amt = chem.iter().filter(|&e| *e == "Ar").count();
    let y_amt = chem.iter().filter(|&e| *e == "Y").count();
    let min_steps = chem.len() - (rn_amt + ar_amt) - 2 * y_amt - 1;
    println!("min steps to get to the element: {}", min_steps);
}

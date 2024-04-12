use std::fs;

fn metadata_sum(tree: &Vec<u32>, at: usize) -> (u32, usize) {
    let mut pointer = at + 2;
    let mut meta_total = 0;
    for _ in 0..tree[at] {
        let res = metadata_sum(tree, pointer);
        meta_total += res.0;
        pointer = res.1;
    }

    meta_total += (0..tree[at + 1])
        .map(|ind| tree[pointer + ind as usize])
        .sum::<u32>();
    (meta_total, pointer + tree[at + 1] as usize)
}

fn node_value(tree: &Vec<u32>, at: usize) -> (u32, usize) {
    let mut pointer = at + 2;
    let mut kid_values = Vec::new();
    for _ in 0..tree[at] {
        let res = node_value(tree, pointer);
        kid_values.push(res.0);
        pointer = res.1;
    }

    let node_val;
    if tree[at] == 0 {
        node_val = (0..tree[at + 1])
            .map(|ind| tree[pointer + ind as usize])
            .sum();
    } else {
        node_val = (0..tree[at + 1])
            .map(|ind| {
                let ind = tree[pointer + ind as usize] as usize;
                if ind == 0 || ind > kid_values.len() {
                    0
                } else {
                    kid_values[ind - 1]
                }
            })
            .sum();
    }

    (node_val, pointer + tree[at + 1] as usize)
}

fn main() {
    let tree: Vec<_> = fs::read_to_string("../input/day8.txt")
        .unwrap()
        .split_whitespace()
        .map(|s| s.parse::<u32>().unwrap())
        .collect();

    println!("metadata sum: {}", metadata_sum(&tree, 0).0);
    println!("root node val: {}", node_value(&tree, 0).0);
}

use std::fs;

const LEN: usize = 256;
const END: [usize; 5] = [17, 31, 73, 47, 23];
const ROUND_NUM: u32 = 64;
const BLOCK_SIZE: usize = 16;

fn main() {
    let raw_lens = fs::read_to_string("../input/day10.txt")
        .expect("bruh");

    let lens: Vec<usize> = raw_lens.split(',')
        .map(|l| l.trim().parse().unwrap() )
        .collect();

    let mut list: Vec<u32> = (0..LEN as u32).collect();
    let mut at = 0usize;
    let mut skip = 0;
    for l in &lens {
        let seq: Vec<usize> = (at..at + *l).map(|i| i % LEN).collect();
        for i in 0..seq.len() / 2 {
            let temp = list[seq[i]];
            list[seq[i]] = list[seq[seq.len() - 1 - i]];
            list[seq[seq.len() - 1 - i]] = temp;
        }
        at += l + skip;
        skip += 1;
    }

    println!("product of first 2 elements: {}", list[0] * list[1]);

    let mut lens: Vec<usize> = raw_lens.trim()
        .chars()
        .map(|c| c as usize)
        .collect();
    for i in END {
        lens.push(i);
    }

    let mut list: Vec<u32> = (0..LEN as u32).collect();
    let mut at = 0usize;
    let mut skip = 0;
    for _ in 0..ROUND_NUM {
        for l in &lens {
            let seq: Vec<usize> = (at..at + *l).map(|i| i % LEN).collect();
            for i in 0..seq.len() / 2 {
                let temp = list[seq[i]];
                list[seq[i]] = list[seq[seq.len() - 1 - i]];
                list[seq[seq.len() - 1 - i]] = temp;
            }
            at += l + skip;
            skip += 1;
        }
    }

    let mut blocks = Vec::new();
    for i in 0..list.len() / BLOCK_SIZE {
        let xor = list.get(i * BLOCK_SIZE..((i + 1) * BLOCK_SIZE))
            .unwrap()
            .iter()
            .fold(0, |acc, &x| acc ^ x);
        blocks.push(xor)
    }

    let mut hash = String::new();
    for b in blocks {
        hash.push_str(&format!("{:02x?}", b));
    }
    println!("final hash: {hash}");
}

use num::PrimInt;
use regex::Regex;
use std::collections::HashMap;
use std::fs;

#[derive(Debug)]
struct Claim {
    id: u32,
    sc: u32,
    sr: u32,
    width: u32,
    height: u32,
}

fn block_int_merge<T: PrimInt>(i1: (T, T), i2: (T, T)) -> Option<(T, T)> {
    let lo = i1.0.max(i2.0);
    let hi = i1.1.min(i2.1);
    return if hi < lo { None } else { Some((lo, hi)) };
}

impl Claim {
    fn overlaps(&self, other: &Claim) -> bool {
        let row_merge = block_int_merge(
            (self.sr, self.sr + self.height - 1),
            (other.sr, other.sr + other.height - 1),
        );
        let col_merge = block_int_merge(
            (self.sc, self.sc + self.width - 1),
            (other.sc, other.sc + other.width - 1),
        );
        return row_merge.is_some() && col_merge.is_some();
    }
}

fn main() {
    let claim_fmt = Regex::new(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)").unwrap();
    let read = fs::read_to_string("../input/day3.txt").unwrap();
    let mut claims = Vec::new();
    for c in read.lines() {
        if let Some(m) = claim_fmt.captures(c) {
            claims.push(Claim {
                id: m[1].parse().unwrap(),
                sc: m[2].parse().unwrap(),
                sr: m[3].parse().unwrap(),
                width: m[4].parse().unwrap(),
                height: m[5].parse().unwrap(),
            });
        }
    }

    let mut claimed_num = HashMap::new();
    for c in &claims {
        for row in c.sr..c.sr + c.height {
            for col in c.sc..c.sc + c.width {
                claimed_num
                    .entry((row, col))
                    .and_modify(|frq| *frq += 1)
                    .or_insert(1);
            }
        }
    }
    let mul_claims = claimed_num.values().filter(|freq| **freq > 1).count();

    let nonoverlapping = claims
        .iter()
        .find(|c1| claims.iter().all(|c2| c2.id == c1.id || !c2.overlaps(c1)))
        .unwrap()
        .id;

    println!("# of spots w/ >1 claims: {mul_claims}");
    println!("id of spot without any overlaps: {nonoverlapping}");
}

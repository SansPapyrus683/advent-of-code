use std::fs;
use regex::Regex;

struct Comp { a: u32, b: u32 }

fn strongest(comps: &Vec<Comp>) -> (u32, (u32, u32)) {
    let mut visited = vec![false; comps.len()];

    // side = true -> b is the end, false -> a is the end
    fn strongest(
        co: &Vec<Comp>, v: &mut Vec<bool>, curr: usize, side: bool
    ) -> (u32, (u32, u32)) {
        let end = if side { co[curr].b } else { co[curr].a };
        v[curr] = true;

        let mut best = 0;
        let mut longest_best = (0, 0);
        for (i, c) in co.iter().enumerate() {
            if v[i] {
                continue;
            }
            if c.a == end || c.b == end {
                let res = strongest(co, v, i, c.a == end);
                best = best.max(res.0);
                longest_best = longest_best.max(res.1);
            }
        }

        v[curr] = false;
        let weight = co[curr].a + co[curr].b;
        (best + weight, (longest_best.0 + 1, longest_best.1 + weight))
    }

    let mut best = 0;
    let mut longest_best = (0, 0);
    for (i, c) in comps.iter().enumerate() {
        if c.a == 0 || c.b == 0 {
            let res = strongest(comps, &mut visited, i, c.a == 0);
            best = best.max(res.0);
            longest_best = longest_best.max(res.1);
        }
    }
    (best, longest_best)
}

fn main() {
    let read = fs::read_to_string("input/day24.txt").expect("bruh");
    let comp_fmt = Regex::new(r"(\d+)/(\d+)").unwrap();

    let mut comps = Vec::new();
    for c in read.lines() {
        if let Some(m) = comp_fmt.captures(c) {
            comps.push(Comp {
                a: m[1].parse().unwrap(), b: m[2].parse().unwrap()
            });
        }
    }

    let (best, (_, longest_best)) = strongest(&comps);
    println!("strongest bridge: {best}");
    println!("strongest bridge out of the longest ones: {longest_best}");
}

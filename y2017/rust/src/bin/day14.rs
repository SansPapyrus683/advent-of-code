const KEY: &str = "jzgqcdpd";

const ROW_NUM: u32 = 128;
const D_POS: [(i32, i32); 4] = [(0, 1), (0, -1), (1, 0), (-1, 0)];

fn knot_hash<S: AsRef<str>>(s: S) -> String {
    const LEN: usize = 256;
    const END: [usize; 5] = [17, 31, 73, 47, 23];
    const BLOCK_SIZE: usize = 16;

    // copied right from day10.rs
    let mut lens: Vec<usize> = s.as_ref()
        .chars()
        .map(|c| c as usize)
        .collect();
    for i in END {
        lens.push(i);
    }

    let mut list: Vec<u32> = (0..LEN as u32).collect();
    let mut at = 0usize;
    let mut skip = 0;
    for _ in 0..64 {
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
    hash
}

fn main() {
    let mut total = 0;
    let mut grid = Vec::new();
    for r in 0..ROW_NUM {
        let to_hash = format!("{KEY}-{r}");
        let hash = knot_hash(&to_hash);
        let mut row = String::new();
        for c in hash.chars() {
            let val = u32::from_str_radix(&c.to_string(), 16).unwrap();
            row.push_str(&format!("{:04b}", val));
        }
        grid.push(row.chars()
            .map(|c| {
                total += if c == '1' { 1 } else { 0 };
                c == '1'
            })
            .collect::<Vec<bool>>());
    }

    println!("# of occupied values in the grid: {total}");

    let mut region_num = 0;
    let dims = (grid.len() as i32, grid[0].len() as i32);
    let mut visited = vec![vec![false; dims.1 as usize]; dims.0 as usize];
    for r in 0..dims.0 as usize {
        for c in 0..dims.1 as usize {
            if !grid[r][c] || visited[r][c] {
                continue;
            }
            visited[r][c] = true;
            let mut frontier = vec![(r as i32, c as i32)];
            while !frontier.is_empty() {
                let curr = frontier.pop().unwrap();
                for d in D_POS {
                    let n = (curr.0 + d.0, curr.1 + d.1);
                    if 0 <= n.0 && n.0 < dims.0 && 0 <= n.1 && n.1 < dims.1
                        && !visited[n.0 as usize][n.1 as usize]
                        && grid[n.0 as usize][n.1 as usize] {
                        frontier.push(n);
                        visited[n.0 as usize][n.1 as usize] = true;
                    }
                }
            }
            region_num += 1;
        }
    }

    println!("# of regions: {region_num}");
}

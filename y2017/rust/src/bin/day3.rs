use std::collections::HashMap;

const INPUT: u32 = 347991;
const DIRS: [(i32, i32); 8] = [
    (0, 1), (-1, 0), (0, -1), (1, 0),
    (1, 1), (-1, 1), (-1, -1), (1, -1),
];

fn cell_val(n: u32) -> (i32, i32) {
    // https://math.stackexchange.com/a/163101/713952
    let n = n as i32;
    let k = (((n as f64).sqrt() - 1.0) / 2.0).ceil() as i32;
    let mut t = 2 * k + 1;
    let mut m = t * t;
    t -= 1;

    if n >= m - t {
        return (k - (m - n), -k);
    } else {
        m -= t;
    }

    if n >= m - t {
        return (-k, -k + (m - n));
    } else {
        m -= t;
    }

    return if n >= m - t {
        (-k + (m - n), k)
    } else {
        (k, k - (m - n - t))
    };
}

fn main() {
    let cell_pos = cell_val(INPUT);
    let dist = cell_pos.0.abs() + cell_pos.1.abs();
    println!("manhattan distance of cell #{INPUT}: {dist}");

    let mut seen = HashMap::from([((0, 0), 1)]);
    let mut at = 2;
    loop {
        let pos = cell_val(at);
        let mut pos_total = 0;
        for d in DIRS {
            let n = (pos.0 + d.0, pos.1 + d.1);
            if seen.contains_key(&n) {
                pos_total += seen[&n];
            }
        }

        if pos_total > INPUT {
            println!("first value greater than {INPUT}: {pos_total}");
            break;
        }

        seen.insert(pos, pos_total);
        at += 1;
    }
}

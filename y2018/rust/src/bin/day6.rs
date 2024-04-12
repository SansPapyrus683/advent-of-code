use std::collections::{HashMap, HashSet};
use std::fs;
use num::abs;

const P2_MAX_DIST: u32 = 1e4 as u32;

fn main() {
    let mut min_x = i32::MAX;
    let mut max_x = i32::MIN;
    let mut min_y = i32::MAX;
    let mut max_y = i32::MIN;
    // yk this definitely takes more lines than a normal for loop
    let points: HashSet<(i32, i32)> = fs::read_to_string("../input/day6.txt")
        .unwrap()
        .lines()
        .map(|p| {
            let split: Vec<&str> = p.split(',').map(|s| s.trim()).collect();
            let x = split[0].parse::<i32>().unwrap();
            let y = split[1].parse::<i32>().unwrap();
            min_x = min_x.min(x);
            max_x = max_x.max(x);
            min_y = min_y.min(y);
            max_y = max_y.max(y);
            (x, y)
        })
        .collect();

    let mut inf_pts = HashSet::new();
    let mut point_areas: HashMap<(i32, i32), u32> = points.iter().map(|p| (*p, 0u32)).collect();
    for x in min_x..=max_x {
        for y in min_y..=max_y {
            let mut smallest_dist = u32::MAX;
            let mut valid_pts = Vec::new();
            for p in &points {
                let dist = (abs(p.0 - x) + abs(p.1 - y)) as u32;
                if dist < smallest_dist {
                    smallest_dist = dist;
                    valid_pts = vec![p];
                } else if dist == smallest_dist {
                    valid_pts.push(p);
                }
            }

            if valid_pts.len() == 1 {
                let pt = valid_pts[0];
                *point_areas.get_mut(&pt).unwrap() += 1;
                if x == min_x || x == max_x || y == min_y || y == max_y {
                    inf_pts.insert(pt.clone());
                }
            }
        }
    }

    let largest_area = point_areas
        .iter()
        .filter(|(p, _)| !inf_pts.contains(p))
        .max_by(|(_, a1), (_, a2)| a1.cmp(a2))
        .unwrap()
        .1;

    println!("largest non-infinite area: {largest_area}");

    let mut close_enough_amt = 0;
    let check_dist = (P2_MAX_DIST / points.len() as u32 + 1) as i32;
    for x in (min_x - check_dist)..=(max_x + check_dist) {
        for y in (min_y - check_dist)..=(max_y + check_dist) {
            let total_dist: u32 = points
                .iter()
                .map(|p| (abs(p.0 - x) + abs(p.1 - y)) as u32)
                .sum();
            close_enough_amt += (total_dist <  P2_MAX_DIST) as u32;
        }
    }

    println!("area of \"close enough\" region: {close_enough_amt}");
}

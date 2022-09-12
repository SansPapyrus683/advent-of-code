use std::fs;
use regex::Regex;

const TIME: u32 = 2503;

struct Reindeer {
    speed: i32, time: i32, rest: i32,
    dist: u32, state_time: i32, flying: bool
}

fn main() {
    let reindeer_fmt = Regex::new(
        r"[a-z]+ can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds"
    ).unwrap();

    let read = fs::read_to_string("input/day14.txt").expect("bruh");
    let mut reindeer = Vec::new();
    for r in read.lines() {
        if let Some(m) = reindeer_fmt.captures(r) {
            reindeer.push(Reindeer {
                speed: m[1].parse().unwrap(),
                time: m[2].parse().unwrap(),
                rest: m[3].parse().unwrap(),
                dist: 0, state_time: 0, flying: true
            });
        }
    }

    let mut points = vec![0; reindeer.len()];
    for _ in 0..TIME {
        for r in reindeer.iter_mut() {
            r.state_time += 1;
            let threshold;
            if r.flying {
                r.dist += r.speed as u32;
                threshold = r.time;
            } else {
                threshold = r.rest;
            }

            if r.state_time == threshold {
                r.flying = !r.flying;
                r.state_time = 0;
            }
        }

        let farthest = reindeer.iter().max_by(
            |r1, r2| r1.dist.cmp(&r2.dist)
        ).unwrap().dist;
        for i in 0..reindeer.len() {
            // assuming no ties i think
            if reindeer[i].dist == farthest {
                points[i] += 1;
            }
        }
    }

    let final_farthest = reindeer.iter().max_by(
        |r1, r2| r1.dist.cmp(&r2.dist)
    ).unwrap().dist;
    let most_pts = points.iter().max().unwrap();

    println!("winning reindeer distance (p1): {final_farthest}");
    println!("winning reindeer SCORE (p2): {most_pts}");
}

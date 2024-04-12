use regex::Regex;
use std::fs;

const EMPTY: char = ' ';
const FILLED: char = '█';
const THRESHOLD: i32 = 80; // results may vary

#[derive(Debug)]
struct Light {
    pos: (i32, i32),
    vel: (i32, i32),
}

fn main() {
    let light_fmt = Regex::new(r"position=<(-?\d+),(-?\d+)>velocity=<(-?\d+),(-?\d+)>").unwrap();
    let mut lights: Vec<_> = fs::read_to_string("../input/day10.txt")
        .unwrap()
        .lines()
        .map(|l| {
            if let Some(m) = light_fmt.captures(&*l.replace(' ', "")) {
                Some(Light {
                    pos: (m[1].parse().unwrap(), m[2].parse().unwrap()),
                    vel: (m[3].parse().unwrap(), m[4].parse().unwrap()),
                })
            } else {
                None
            }
        })
        .filter(|l| l.is_some())
        .map(|l| l.unwrap())
        .collect();

    let mut time = 0u32;
    loop {
        for l in &mut lights {
            l.pos = (l.pos.0 + l.vel.0, l.pos.1 + l.vel.1);
        }

        let mut min_x = i32::MAX;
        let mut max_x = i32::MIN;
        let mut min_y = i32::MAX;
        let mut max_y = i32::MIN;
        lights.iter().for_each(|l| {
            min_x = min_x.min(l.pos.0);
            max_x = max_x.max(l.pos.0);
            min_y = min_y.min(l.pos.1);
            max_y = max_y.max(l.pos.1);
        });

        time += 1;
        if max_x - min_x < THRESHOLD && max_y - min_y < THRESHOLD {
            let mut grid =
                vec![vec![EMPTY; (max_x - min_x + 1) as usize]; (max_y - min_y + 1) as usize];
            lights.iter().for_each(|l| {
                grid[(l.pos.1 - min_y) as usize][(l.pos.0 - min_x) as usize] = FILLED
            });

            println!("curr time: {time}");
            grid.iter()
                .for_each(|row| println!("{}", String::from_iter(row)));
        }
    }
}

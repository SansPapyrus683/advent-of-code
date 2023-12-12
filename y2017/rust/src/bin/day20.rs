use std::fs;
use std::collections::HashMap;
use regex::Regex;

#[derive(Debug, Clone)]
struct Particle {
    p: (i32, i32, i32),
    v: (i32, i32, i32),
    a: (i32, i32, i32)
}

impl Particle {
    fn sim(&mut self) {
        self.v = (self.v.0 + self.a.0, self.v.1 + self.a.1, self.v.2 + self.a.2);
        self.p = (self.p.0 + self.v.0, self.p.1 + self.v.1, self.p.2 + self.v.2);
    }
}

fn main() {
    let read = fs::read_to_string("input/day20.txt").expect("bruh");

    let mut particles = Vec::new();
    let particle_fmt = Regex::new(concat!(
        r"p=<(-?\d+),(-?\d+),(-?\d+)>,",
        r"v=<(-?\d+),(-?\d+),(-?\d+)>,",
        r"a=<(-?\d+),(-?\d+),(-?\d+)>"
    )).unwrap();
    for p in read.lines() {
        let p: String = p.chars().filter(|&c| !c.is_whitespace()).collect();
        if let Some(m) = particle_fmt.captures(&p) {
            particles.push(Particle {
                p: (m[1].parse().unwrap(), m[2].parse().unwrap(), m[3].parse().unwrap()),
                v: (m[4].parse().unwrap(), m[5].parse().unwrap(), m[6].parse().unwrap()),
                a: (m[7].parse().unwrap(), m[8].parse().unwrap(), m[9].parse().unwrap())
            });
        }
    }

    let mut min_accel = (i32::MAX, None);
    for (i, p) in particles.iter().enumerate() {
        let accel = p.a.0.abs() + p.a.1.abs() + p.a.2.abs();
        if accel < min_accel.0 {
            min_accel = (accel, Some(i));
        }
    }
    println!("{} will stay the closest in the long run", min_accel.1.unwrap());

    let mut sim = particles.to_vec();
    let sim_amt = 100;
    for _ in 0..sim_amt {
        for p in &mut sim {
            p.sim();
        }

        let mut occs: HashMap<(i32, i32, i32), Vec<Particle>> = HashMap::new();
        for p in &sim {
            occs.entry(p.p).or_default().push(p.clone());
        }

        sim.clear();
        for (_, o) in &occs {
            if o.len() == 1 {
                sim.push(o[0].clone());
            }
        }
    }
    println!("{} particles left after {sim_amt} steps, should be enough", sim.len());
}

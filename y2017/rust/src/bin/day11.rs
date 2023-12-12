use std::fs;

#[derive(Copy, Clone)]
struct Point { x: i32, y: i32 }

impl std::ops::Add<Point> for Point {
    type Output = Self;
    fn add(self, rhs: Point) -> Self::Output {
        Point { x: self.x + rhs.x, y: self.y + rhs.y }
    }
}

// https://stackoverflow.com/questions/11373122 again
enum HexDir { N, NE, SE, S, SW, NW }

impl HexDir {
    fn rel_point(&self) -> Point {
        match self {
            HexDir::N => Point { x: 0, y: 1 },
            HexDir::NE => Point { x: 1, y: 0 },
            HexDir::SE => Point { x: 1, y: -1 },
            HexDir::S => Point { x: 0, y: -1 },
            HexDir::SW => Point { x: -1, y: 0 },
            HexDir::NW => Point { x: -1, y: 1 }
        }
    }

    fn from_str(s: &str) -> Option<Self> {
        match s {
            "n" => Some(Self::N),
            "ne" => Some(Self::NE),
            "se" => Some(Self::SE),
            "s" => Some(Self::S),
            "sw" => Some(Self::SW),
            "nw" => Some(Self::NW),
            _ => None
        }
    }
}

fn hex_dist(p1: &Point, p2: &Point) -> u32 {
    // https://stackoverflow.com/questions/5084801 nice
    let dx = p1.x - p2.x;
    let dy = p1.y - p2.y;
    if dx.signum() == dy.signum() {
        (dx + dy).abs() as u32
    } else {
        dx.abs().max(dy.abs()) as u32
    }
}

fn main() {
    let steps: Vec<HexDir> = fs::read_to_string("../input/day11.txt")
        .expect("bruh")
        .trim()
        .split(',')
        .map(|d| HexDir::from_str(d).unwrap())
        .collect();

    let start = Point { x: 0, y: 0 };
    let mut farthest = 0;
    let end: Point = steps.iter()
        .map(|hd| hd.rel_point())
        .fold(start.clone(), |acc, p| {
            farthest = farthest.max(hex_dist(&acc, &start));
            acc + p
        });

    let end_dist = hex_dist(&end, &start);
    farthest = farthest.max(end_dist);

    println!("ending distance: {end_dist}");
    println!("farthest distance ever: {farthest}");
}

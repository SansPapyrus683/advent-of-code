use std::fs;
use std::collections::HashSet;

enum Direction { Up, Down, Left, Right }

impl Direction {
    fn dpos(&self) -> (i32, i32) {
        match self {
            Direction::Up => (0, 1),
            Direction::Down => (0, -1),
            Direction::Left => (-1, 0),
            Direction::Right => (1, 0)
        }
    }

    fn from_char(c: &char) -> Option<Direction> {
        match c {
            '^' => Some(Direction::Up),
            'v' => Some(Direction::Down),
            '<' => Some(Direction::Left),
            '>' => Some(Direction::Right),
            _ => None
        }
    }
}

fn main() {
    let directions = fs::read_to_string("input/day3.txt").expect("you done messed up");

    let mut dirs = Vec::new();
    for c in directions.chars() {
        if let Some(raw_dir) = Direction::from_char(&c) {
            dirs.push(raw_dir.dpos());
        }
    }

    let mut at = (0, 0);
    let mut visited = HashSet::new();
    visited.insert(at);
    for d in &dirs {
        at.0 += d.0;
        at.1 += d.1;
        visited.insert(at);
    }

    println!("# of houses: {}", visited.len());

    visited = HashSet::new();
    let mut at = [(0, 0), (0, 0)];
    for p in at {
        visited.insert(p);
    }
    for (i, d) in dirs.iter().enumerate() {
        let mut p = &mut at[i % at.len()];
        p.0 += d.0;
        p.1 += d.1;
        // rust you're high, go home
        visited.insert((p.0, p.1));
    }

    println!("# of houses w/ bot: {}", visited.len());

}

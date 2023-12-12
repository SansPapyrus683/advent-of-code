use std::fs;
use std::collections::{HashMap, HashSet};

const P1_AMT: u32 = 10000;
const P2_AMT: u32 = 10000000;

#[derive(Debug, Clone)]
enum Dir { Up, Down, Left, Right }

impl Dir {
    fn pos_change(&self) -> (i32, i32)  {
        match self {
            Self::Up => (-1, 0),
            Self::Down => (1, 0),
            Self::Left => (0, -1),
            Self::Right => (0, 1)
        }
    }

    fn left(&self) -> Self {
        match self {
            Self::Up => Self::Left,
            Self::Down => Self::Right,
            Self::Left => Self::Down,
            Self::Right => Self::Up
        }
    }

    fn right(&self) -> Self {
        self.left().left().left()  // LMAO
    }
}

#[derive(Debug, Default, PartialEq)]
enum Node { #[default] Clean, Weakened, Infected, Flagged }

impl Node {
    fn change(&self) -> Self {
        match self {
            Self::Clean => Self::Weakened,
            Self::Weakened => Self::Infected,
            Self::Infected => Self::Flagged,
            Self::Flagged => Self::Clean,
        }
    }
}

fn main() {
    let read = fs::read_to_string("input/day22.txt").expect("bruh");

    let mut infected = HashSet::new();
    let mut row_num = 0;
    let mut col_num = -1;
    for (r, row) in read.lines().enumerate() {
        for (c, col) in row.chars().enumerate() {
            if col == '#' {
                infected.insert((r as i32, c as i32));
            }
        }

        col_num = if col_num == -1 { row.len() as i32 } else {
            assert_eq!(col_num, row.len() as i32);
            col_num
        };
        row_num += 1;
    }

    let mut p1_infected = infected.clone();
    let mut at = (row_num / 2, col_num / 2);
    let mut dir = Dir::Up;
    let mut p1_caused = 0;
    for _ in 0..P1_AMT {
        dir = if p1_infected.contains(&at) { dir.right() } else { dir.left() };
        if p1_infected.contains(&at) {
            p1_infected.remove(&at);
        } else {
            p1_caused += 1;
            p1_infected.insert(at);
        }

        let change = dir.pos_change();
        at = (at.0 + change.0, at.1 + change.1);
    }
    println!("the simple virus has {p1_caused} infection bursts in {P1_AMT} steps");

    let mut p2_tiles = HashMap::new();
    for i in &infected {
        p2_tiles.insert(i.clone(), Node::Infected);
    }
    at = (row_num / 2, col_num / 2);
    dir = Dir::Up;
    let mut p2_caused = 0;
    for _ in 0..P2_AMT {
        dir = match p2_tiles.entry(at).or_default() {
            Node::Clean => dir.left(),
            Node::Weakened => dir,
            Node::Infected => dir.right(),
            Node::Flagged => dir.left().left()
        };
        let next = p2_tiles.entry(at).or_default().change();
        p2_tiles.insert(at, next);
        p2_caused += if p2_tiles[&at] == Node::Infected { 1 } else { 0 };

        let change = dir.pos_change();
        at = (at.0 + change.0, at.1 + change.1);
    }
    println!("the advanced virus has {p2_caused} infection bursts in {P2_AMT} steps");
}

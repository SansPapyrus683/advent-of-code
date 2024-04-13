use std::collections::HashMap;
use std::fs;

#[derive(Debug, Copy, Clone)]
enum Dir {
    Up,
    Down,
    Left,
    Right,
}

impl Dir {
    fn delta(&self) -> (i32, i32) {
        match self {
            Dir::Up => (-1, 0),
            Dir::Down => (1, 0),
            Dir::Left => (0, -1),
            Dir::Right => (0, 1),
        }
    }

    fn turn(&self, turn: char) -> Self {
        match turn {
            '/' => match self {
                Dir::Up => Dir::Right,
                Dir::Down => Dir::Left,
                Dir::Left => Dir::Down,
                Dir::Right => Dir::Up,
            },
            '\\' => match self {
                Dir::Up => Dir::Left,
                Dir::Down => Dir::Right,
                Dir::Left => Dir::Up,
                Dir::Right => Dir::Down,
            },
            _ => *self,
        }
    }

    fn turn_left(&self) -> Self {
        match self {
            Dir::Up => Dir::Left,
            Dir::Down => Dir::Right,
            Dir::Left => Dir::Down,
            Dir::Right => Dir::Up,
        }
    }

    fn turn_right(&self) -> Self {
        match self {
            Dir::Up => Dir::Right,
            Dir::Down => Dir::Left,
            Dir::Left => Dir::Up,
            Dir::Right => Dir::Down,
        }
    }
}

fn main() {
    let read = fs::read_to_string("../input/day13.txt").unwrap();
    let mut turns = Vec::new();
    let mut carts = Vec::new();
    for (y, r) in read.lines().enumerate() {
        let mut row_turns = vec![' '; r.len()];
        for (x, c) in r.chars().enumerate() {
            match c {
                '/' | '\\' | '+' => row_turns[x] = c,
                'v' => carts.push((Dir::Down, (y, x), 0)),
                '>' => carts.push((Dir::Right, (y, x), 0)),
                '<' => carts.push((Dir::Left, (y, x), 0)),
                '^' => carts.push((Dir::Up, (y, x), 0)),
                _ => (),
            }
        }
        turns.push(row_turns);
    }

    let mut first_crash = true;
    while carts.len() > 1 {
        carts.sort_by_key(|c| c.1);

        let mut occupied: HashMap<(usize, usize), usize> =
            carts.iter().enumerate().map(|(i, c)| (c.1, i)).collect();

        for i in 0..carts.len() {
            let (mut dir, (r, c), mut turn_num) = carts[i];
            let delta = dir.delta();
            let next = ((r as i32 + delta.0) as usize, (c as i32 + delta.1) as usize);
            let curr_ind = occupied.remove(&(r, c));
            if curr_ind.is_none() {
                continue;
            }
            let curr_ind = curr_ind.unwrap();

            if occupied.contains_key(&next) {
                occupied.remove(&next);
                if first_crash {
                    println!("loc of first crash: {},{}", next.1, next.0);
                    first_crash = false;
                }
                continue;
            }

            dir = dir.turn(turns[next.0][next.1]);
            if turns[next.0][next.1] == '+' {
                match turn_num % 3 {
                    0 => dir = dir.turn_left(),
                    2 => dir = dir.turn_right(),
                    _ => (),
                }
                turn_num += 1;
            }
            occupied.insert(next, curr_ind);
            carts[i] = (dir, next, turn_num);
        }

        carts = occupied.iter().map(|(_, ind)| carts[*ind]).collect();
    }

    if carts.is_empty() {
        println!("uh all the carts are dead,, what?");
    } else {
        let (_, left_pos, _) = carts[0];
        println!("loc of final cart: {},{}", left_pos.1, left_pos.0);
    }
}

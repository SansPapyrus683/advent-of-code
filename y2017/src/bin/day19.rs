use std::fs;

#[derive(Clone)]
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
    
    fn turn(&self) -> Vec<Dir> {
        match self {
            Self::Up | Self::Down => vec![Self::Left, Self::Right],
            Self::Left | Self::Right => vec![Self::Up, Self::Down],
        }
    }
}

fn main() {
    let read = fs::read_to_string("input/day19.txt").expect("bruh");
    let mut grid = Vec::new();
    for r in read.lines() {
        let mut row = Vec::new();
        for c in r.chars() {
            if c.is_alphabetic() {
                row.push(Some(Some(c)));
                continue;
            }
            match c {
                '|' | '-' | '+' => row.push(Some(None)),
                _ => row.push(None)
            };
        }
        grid.push(row);
    }

    let mut at = (0, -1);
    for (i, c) in grid[0].iter().enumerate() {
        if c.is_some() {
            at.1 = i as i32;
            break;
        }
    }

    let mut dir = Dir::Down;
    let mut seen_chars = String::new();
    let mut steps = 0;
    loop {
        let mut all = vec![dir.clone()];
        all.append(&mut dir.turn());

        let mut moved = false;
        for d in all {
            let n = d.pos_change();
            let n = (at.0 + n.0, at.1 + n.1);
            // just realized this errors for negative indices...oh well
            let res = grid.get(n.0 as usize).map(|r| r.get(n.1 as usize));
            if res.is_none()
                || res.unwrap().is_none()
                || res.unwrap().unwrap().is_none() {
                continue;
            }
            let res = res.unwrap().unwrap();
            if let Some(Some(c)) = res {
                seen_chars.push(*c);
            }
            at = n;
            dir = d;
            moved = true;
            steps += 1;
            break;
        }

        if !moved {
            break;
        }
    }

    println!("sequence of seen characters: {seen_chars}");
    println!("total # of steps traversed: {}", steps + 1);
}

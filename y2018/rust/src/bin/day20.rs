use std::collections::HashMap;
use std::fs;

const P2_DIST_REQ: u32 = 1000;

fn room_dists(re: &str) -> HashMap<(i32, i32), u32> {
    let dir_dict = HashMap::from([
        (
            'N',
            // have the most cursed lambda ever
            Box::new(|(r, c): (i32, i32)| (r - 1, c)) as Box<dyn Fn((i32, i32)) -> (i32, i32)>,
        ),
        ('S', Box::new(|(r, c): (i32, i32)| (r + 1, c))),
        ('E', Box::new(|(r, c): (i32, i32)| (r, c + 1))),
        ('W', Box::new(|(r, c): (i32, i32)| (r, c - 1))),
    ]);

    let start = (0, 0);
    let mut dist = HashMap::from([(start, 0)]);
    let mut stack = vec![start];
    let mut at = start;
    for i in re.to_uppercase().chars() {
        if dir_dict.contains_key(&i) {
            let prev = at;
            at = dir_dict[&i](at);
            dist.insert(
                at,
                *dist.get(&at).unwrap_or(&u32::MAX).min(&(dist[&prev] + 1)),
            );
        } else if i == '(' {
            stack.push(at);
        } else if i == ')' {
            at = stack.pop().unwrap();
        } else if i == '|' {
            at = *stack.last().unwrap();
        }
    }
    dist
}

fn main() {
    let mut vec: Vec<Box<dyn Fn()>> = Vec::new();
    vec.push(Box::new(|| println!("test")));
    vec.push(Box::new(|| println!("test2")));
    let raw_regex = fs::read_to_string("../input/day20.txt")
        .unwrap()
        .trim()
        .to_owned();

    let regex = &raw_regex[1..(raw_regex.len() - 1)];
    let rooms = room_dists(regex);
    println!("farthest room distance: {}", rooms.values().max().unwrap());

    println!(
        "# of rooms at least {P2_DIST_REQ} doors away: {}",
        rooms.values().filter(|d| d >= &&P2_DIST_REQ).count()
    );
}
